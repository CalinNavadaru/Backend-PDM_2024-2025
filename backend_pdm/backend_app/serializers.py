from rest_framework import serializers
from .models import Employees

class EmployeesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employees
        fields = ['url', 'employee_id', 'first_name', 'last_name', 'salary', 'date_join', 'on_field']
