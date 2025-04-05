from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .views import TaskViewSet, CategoryViewSet

# Create a custom API root view with AllowAny permission
@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response({
        'tasks': reverse('api:task-list', request=request, format=format),
        'categories': reverse('api:category-list', request=request, format=format),
    })

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')

app_name = 'api'

urlpatterns = [
    path('', api_root, name='api-root'),  # Custom root view
    path('', include(router.urls)),
]