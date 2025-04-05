from rest_framework import serializers
from .models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TaskSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'priority', 
                  'due_date', 'category', 'category_name', 
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'category_name')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)