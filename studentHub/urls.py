from django.urls import path
from .views import *

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('resource/<int:resource_id>/', views.resource_detail, name='resource-detail'),
    path('edit-resource/<int:resource_id>/', views.edit_resource, name='edit-resource'),
    path('delete-resource/<int:resource_id>/', views.delete_resource, name='delete-resource'),
    path('add_resource/', views.add_resource, name='add-resource'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('download/<str:download_link>/', DownloadResourceView.as_view(), name='download-resource'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('like/<int:resource_id>/', like_resource, name='like-resource'),
    path('comment/<int:resource_id>/', add_comment, name='add-comment'),
    path('logout/', logout.as_view(next_page='home'), name='logout'),
    path('<str:query>/', views.home, name='home'),


]
