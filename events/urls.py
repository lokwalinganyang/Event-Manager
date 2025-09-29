from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Web URLs
    path('', views.HomePageView.as_view(), name='home'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event/<int:event_id>/register/', views.RegistrationCreateView.as_view(), name='register'),
    
    # API URLs
    path('api/events/', views.EventListAPIView.as_view(), name='api_events'),
    path('api/events/<int:pk>/', views.EventDetailAPIView.as_view(), name='api_event_detail'),
    path('api/register/', views.RegistrationCreateAPIView.as_view(), name='api_register'),
]