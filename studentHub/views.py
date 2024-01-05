from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from .forms import ResourceForm
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import View
from .forms import UserProfileForm
from django.contrib.auth.views import LogoutView


def home(request):
    
    search_query = request.GET.get('search', '')
    if search_query:
        search_words = search_query.split()
        for word in search_words:
            resources = Resource.objects.filter(title__icontains=word)
    else:
        resources = Resource.objects.all()
        
    return render(request, 'studenthub/home.html', {'resources': resources, 'search_query': search_query})

@login_required
def profile(request):
    return render(request, 'studenthub/profile.html')

def resource_detail(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    return render(request, 'studenthub/resource-detail.html', {'resource': resource})

@login_required
def edit_resource(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploader = request.user
            if 'file' in request.FILES:
                resource.file = request.FILES['file']
            
            random_link = get_random_string(length=20)
            resource.downloadLink = reverse('download-resource', kwargs={'download_link': random_link})
            resource.save()
            messages.success(request, 'Resource updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating the resource. Please check the form.')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'studenthub/edit_resource.html', {'form': form, 'resource': resource})

def delete_resource(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    resource.delete()
    messages.success(request, 'Resource deleted successfully.')
    return redirect('profile')

@login_required
def like_resource(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)

    # Check if the user has already liked the resource
    if request.user in resource.likes.all():
        resource.likes.remove(request.user)
        messages.success(request, 'You unliked the resource.')
    else:
        resource.likes.add(request.user)
        messages.success(request, 'You liked the resource.')

    return redirect('resource-detail', resource_id=resource_id)

@login_required
def add_comment(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)

    if request.method == 'POST':
        content = request.POST.get('comment')
        Comment.objects.create(content=content, resource=resource, poster=request.user)
        messages.success(request, 'Comment added successfully.')

    return redirect('resource-detail', resource_id=resource_id)

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            pro = form.save(commit=False)
            if 'profile_pic' in request.FILES:
                pro.profile_pic = request.FILES['profile_pic']
            pro.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Error updating the profile. Please check the form.')
            print(form.errors)
            return render(request, 'studenthub/profile.html', {'form': form})
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'studenthub/profile.html', {'form': form})

@login_required
def add_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploader = request.user
            resource.file = request.FILES['file']
            random_link = get_random_string(length=20)
            resource.downloadLink = reverse('download-resource', kwargs={'download_link': random_link})
            resource.save()
            messages.success(request, 'Resource added successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Error adding the resource. Please check the form.')
    else:
        form = ResourceForm()

    return render(request, 'studenthub/add_resource.html', {'form': form})

class DownloadResourceView(View):
    def get(self, request, download_link):
        resource = get_object_or_404(Resource, downloadLink=f'/download/{download_link}/')
        file_path = resource.file.path
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename={resource.file.name}'
            return response

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'studenthub/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'studenthub/login.html')

class logout(LogoutView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        redirect('home',{'search_query':''})

        return response

