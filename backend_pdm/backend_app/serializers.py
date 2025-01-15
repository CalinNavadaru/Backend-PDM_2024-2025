import sys
from rest_framework import serializers
from .models import Employees
from django.contrib.auth import get_user_model
import base64

class EmployeesSerializer(serializers.HyperlinkedModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    class Meta:
        model = Employees
        fields = ['url', 'employee_id', 'first_name', 'last_name', 'salary', 'date_join', 'on_field', 'manager', 'profile_picture', 'latitude', 'longitude']
        extra_kwargs = {
                'url': {'view_name': 'employees-detail', 'lookup_field': 'employee_id'}
            }
        
    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        employee = super().create(validated_data)
        if profile_picture:
            employee.profile_picture = profile_picture
            employee.save()
        return employee

    def update(self, instance, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        instance = super().update(instance, validated_data)
        if profile_picture:
            instance.profile_picture = profile_picture
            instance.save()
        return instance
        