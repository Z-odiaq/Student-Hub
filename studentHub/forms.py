# studenthub/forms.py

from django import forms
from .models import *


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'file', 'tags', 'subject', 'course', 'school', 'department', 'semester', 'year']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'school',  'birthday', 'email', 'classroom', 'first_name', 'last_name'] 
        

    # Add first_name, last_name, and email fields from User model
    
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    email = forms.EmailField(max_length=100, required=False, label='Email')
    profile_pic = forms.ImageField(required=False, label='Profile Picture')
    school = forms.CharField(max_length=100, required=False, label='School')
    birthday = forms.DateField(required=False, label='Birthday')
    classroom = forms.CharField(max_length=100, required=False, label='Classroom')
    bio = forms.CharField(max_length=1000, required=False, label='Bio')
    

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        user = self.instance.user

        
        self.fields['school'].required = False
        self.fields['birthday'].required = False
        self.fields['classroom'].required = False
        self.fields['profile_pic'].required = False
        self.fields['bio'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        
        
    def save(self, commit=True):
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()

        return super(UserProfileForm, self).save(commit)
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
