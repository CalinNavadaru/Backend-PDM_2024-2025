from rest_framework import serializers
from .models import Employees

class EmployeesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employees
        fields = ['url', 'employee_id', 'first_name', 'last_name', 'salary', 'date_join', 'on_field']
        extra_kwargs = {
                'url': {'view_name': 'employees-detail', 'lookup_field': 'employee_id'}
            }
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        