from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
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

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

class RegistrationCreateView(CreateView):
    model = Registration
    template_name = 'events/registration_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone']
    
    def get_success_url(self):
        # Option 1: Redirect to home page
        return reverse('events:home')
        
        # Option 2: Redirect to event detail page (uncomment if preferred)
        # return reverse('events:event_detail', kwargs={'pk': self.kwargs['event_id']})
    
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