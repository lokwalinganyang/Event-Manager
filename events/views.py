from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Event, Registration
from .serializers import EventSerializer, EventDetailSerializer, RegistrationCreateSerializer

# Template Views
class HomePageView(ListView):
    model = Event
    template_name = 'events/home.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        return Event.objects.filter(date__gte=timezone.now()).order_by('date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = context['events']
        
        # Categorize events
        context['open_events'] = [event for event in events if not event.is_full]
        context['sold_out_events'] = [event for event in events if event.is_full]
        context['featured_events'] = events[:3]  # First 3 events as featured
        
        return context

class AboutPageView(TemplateView):
    template_name = 'events/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any context data needed for the about page
        context['total_events'] = Event.objects.count()
        context['total_registrations'] = Registration.objects.count()
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

class RegistrationCreateView(CreateView):
    model = Registration
    template_name = 'events/registration_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone']
    
    def get_success_url(self):
        return reverse('events:home')
    
    def form_valid(self, form):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        if event.is_full:
            form.add_error(None, 'This event is already full.')
            return self.form_invalid(form)
        
        # Check if email is already registered for this event
        if Registration.objects.filter(event=event, email=form.cleaned_data['email']).exists():
            form.add_error('email', 'This email is already registered for this event.')
            return self.form_invalid(form)
        
        form.instance.event = event
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event'] = get_object_or_404(Event, pk=self.kwargs['event_id'])
        return context

class APIDocsView(TemplateView):
    template_name = 'events/api_docs.html'
# API Views
class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    serializer_class = EventSerializer

class EventDetailAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer

class RegistrationCreateAPIView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Registration successful!", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )