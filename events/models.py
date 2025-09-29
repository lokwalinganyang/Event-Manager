from django.db import models
from django.core.validators import MinLengthValidator

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    max_participants = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def registered_count(self):
        return self.registrations.count()
    
    @property
    def is_full(self):
        return self.registered_count >= self.max_participants
    
    @property
    def progress_percentage(self):
        """Return registration progress as percentage"""
        if self.max_participants == 0:
            return 0
        return (self.registered_count / self.max_participants) * 100
    
    @property
    def spots_remaining(self):
        """Return number of spots remaining"""
        return max(0, self.max_participants - self.registered_count)

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    first_name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    last_name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'email']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.event.title}"