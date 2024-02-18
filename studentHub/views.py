from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from .forms import MessageForm, ResourceForm
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from .forms import UserProfileForm
from django.contrib.auth.views import LogoutView
from django.views.generic import DeleteView


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
        try:
            userChk = User.objects.get(username=username)
            if ( userChk is not None and hasattr(userChk, 'profile') and userChk.profile.blocked):
                return render(request, 'studenthub/blocked.html')
        except:
            return render(request, 'studenthub/login.html')

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if ( user.is_staff) :
                return HttpResponseRedirect(reverse('admin:index'))
            else:                
                return redirect('home')
    return render(request, 'studenthub/login.html')

class logout(LogoutView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        redirect('home',{'search_query':''})

        return response



def ModeratorDeleteComment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('resource-detail', resource_id=comment.resource.id)

def ModeratorDeleteResource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    resource.delete()
    return redirect('home') 

def ModeratorDeleteAllComments(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    resource.comment_set.all().delete()
    return redirect('resource-detail', resource_id=resource_id)

def ModeratorBlockUser(request, resource_id):
    user_id = get_object_or_404(Resource, id=resource_id).uploader.id
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    if profile.blocked:
        profile.blocked = False
    else:
        profile.blocked = True
    profile.save()
    return redirect('resource-detail', resource_id=resource_id)

@login_required
def send_meszsage(request, recipient_username):
    users = User.objects.all()  # Fetch all users
    context = {'users': users}
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            recipient = User.objects.get(username=recipient_username)

            # Create and save the message
            Message.objects.create(sender=request.user, recipient=recipient, content=content)

            return redirect('view_messages')  # Redirect to the view_messages page after sending the message
    else:
        form = MessageForm()

    context = {'form': form, 'recipient_username': recipient_username}
    return render(request, 'studenthub/send_message.html', context)
@login_required
def view_messages(request):
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    # Ajoutez ici la logique pour afficher les messages dans le modèle de messagerie
    return render(request, 'studenthub/view_messages.html', {'received_messages': received_messages,'sent_messages': sent_messages})
def my_view(request):
    users = User.objects.all()  # Fetch all users
    context = {'users': users}
    return render(request, 'my_template.html', context)

def send_message(request):
    # If a recipient_username is provided, fetch the User object
    recipient = None


    # Handle POST request: sending a message
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Assuming the form saves the message to the database
            message = form.save(commit=False)
            message.sender = request.user  # Set the sender to the current user
            message.recipient = recipient  # Set the recipient
            message.save()
            # Redirect to a new URL, maybe a confirmation page or back to the form
            return redirect('view_messages')  # Replace 'success_page' with your actual success page's name
    else:
        form = MessageForm()

    # Fetch all users for the recipient dropdown, excluding the current user
    users = User.objects.exclude(username=request.user.username)

    context = {
        'form': form,
        'users': users,
        'recipient': recipient,
    }
    return render(request, 'studenthub/send_message.html', context)

def my_uploads(request):
    resources = Resource.objects.filter(uploader=request.user)
    return render(request, 'studenthub/myuploads.html', {'resources': resources})