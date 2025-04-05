from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(
            name='Test Category',
            user=self.user
        )
        
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'status': 'pending',
            'priority': 'high',
            'category': self.category.id
        }
        
    def test_create_task(self):
        response = self.client.post(
            reverse('api:task-list'),
            self.task_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Task')
        
    def test_complete_task(self):
        task = Task.objects.create(
            title='Test Task',
            user=self.user,
            status='pending'
        )
        response = self.client.put(
            reverse('api:task-complete', kwargs={'pk': task.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.status, 'completed')
