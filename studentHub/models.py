from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Resource(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    file = models.FileField(upload_to='resources/')
    date_uploaded = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.CharField(max_length=1000)
    subject = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    year = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    downloadLink = models.CharField(max_length=1000, default='')
    likes = models.ManyToManyField(User, related_name='liked_resources')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('resource-detail', kwargs={'resource_id': self.id})
    
    def get_user_rating(self):
        user = self.request.user if hasattr(self, 'request') and hasattr(self.request, 'user') else None
        rating = self.rating_set.filter(rater=user).first()
        return rating.rating if rating else None  

class Comment(models.Model):
    content = models.CharField(max_length=1000)
    date_posted = models.DateTimeField(auto_now_add=True)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    def get_absolute_url(self):
        return reverse('resource-detail', kwargs={'resource_id': self.resource.id})
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username} - {self.timestamp}" 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000, default='')
    profile_pic = models.ImageField(upload_to='images/', blank=True, null=True)
    school = models.CharField(max_length=100, default='TekUp')
    birthday = models.DateField(default='2000-01-01')  
    email = models.CharField(max_length=1000, default='') 
    classroom = models.CharField(max_length=1000, default='')
    role = models.CharField(max_length=100, default='Student')
    blocked = models.BooleanField(default=False)

    
    def __str__(self):
        return self.user.first_name
    def get_absolute_url(self):
        return reverse('profile')
