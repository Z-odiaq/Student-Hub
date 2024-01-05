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
        fields = ['bio', 'profile_pic', 'school',  'birthday', 'email', 'classroom'] 

    # Add first_name, last_name, and email fields from User model
    first_name = forms.CharField(max_length=30, required=False, label='First Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last Name')
    email = forms.EmailField(max_length=100, required=False, label='Email')
    profile_pic = forms.ImageField(required=False, label='Profile Picture')
    school = forms.CharField(max_length=100, required=False, label='School')
    birthday = forms.DateField(required=False, label='Birthday')
    classroom = forms.CharField(max_length=100, required=False, label='Classroom')
    

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        user = self.instance.user
        print(self.instance)
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name
        self.fields['email'].initial = user.profile.email
        self.fields['bio'].initial = user.profile.bio
        self.fields['profile_pic'].initial = user.profile.profile_pic
        self.fields['school'].initial = user.profile.school
        self.fields['birthday'].initial = user.profile.birthday
        self.fields['classroom'].initial = user.profile.classroom
        
        self.fields['school'].required = False
        self.fields['birthday'].required = False
        self.fields['classroom'].required = False
        
    def save(self, commit=True):
        user = self.instance.user
        user.save()
        return super(UserProfileForm, self).save(commit)