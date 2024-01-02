from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Resource

class UrlTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.resource = Resource.objects.create(
            title='Test Resource',
            description='This is a test resource.',
            file='./testfile.pdf',
            uploader=self.user,
            tags='test, django',
            subject='Test Subject',
            course='Test Course',
            school='Test School',
            department='Test Department',
            semester='Test Semester',
            year=2023,
            downloadLink= 'test-link'
        )

    def test_home_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_profile_url(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_add_resource_url(self):
        response = self.client.get(reverse('add-resource'))
        self.assertEqual(response.status_code, 200)
        
    def test_resource_detail_url(self):
        response = self.client.get(reverse('resource-detail', kwargs={'resource_id': self.resource.id}))
        self.assertEqual(response.status_code, 200)

    def test_edit_resource_url(self):
        response = self.client.get(reverse('edit-resource', kwargs={'resource_id': self.resource.id}))
        self.assertEqual(response.status_code, 200)
        
    def test_delete_resource_url(self):
        response = self.client.get(reverse('delete-resource', kwargs={'resource_id': self.resource.id}))
        self.assertEqual(response.status_code, 302)

    def test_register_url(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_url(self):
        response = self.client.get(reverse('edit-profile'))
        self.assertEqual(response.status_code, 200)

    def test_like_resource_url(self):
        response = self.client.get(reverse('like-resource', kwargs={'resource_id': self.resource.id}))
        self.assertEqual(response.status_code, 302)  
        
    def test_add_comment_url(self):
        response = self.client.get(reverse('add-comment', kwargs={'resource_id': self.resource.id}))
        self.assertEqual(response.status_code, 302)  

    def test_logout_url(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  
