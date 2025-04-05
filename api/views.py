from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        category = self.get_object()
        tasks = Task.objects.filter(category=category)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category']
    ordering_fields = ['due_date', 'priority', 'created_at']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    @action(detail=True, methods=['put'])
    def complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'completed'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def filter(self, request):
        queryset = self.get_queryset()
        
        status = request.query_params.get('status')
        priority = request.query_params.get('priority')
        category = request.query_params.get('category')
        due_date_before = request.query_params.get('due_date_before')
        due_date_after = request.query_params.get('due_date_after')
        
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if category:
            queryset = queryset.filter(category__name=category)
        if due_date_before:
            queryset = queryset.filter(due_date__lte=due_date_before)
        if due_date_after:
            queryset = queryset.filter(due_date__gte=due_date_after)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
