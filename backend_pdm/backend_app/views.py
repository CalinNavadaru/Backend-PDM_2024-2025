# Create your views here.
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import sys
import json

from backend_app.models import Employees
from backend_app.serializers import EmployeesSerializer
from .constants import GROUP_NAME


class EmployeeList(APIView):
    def get(self, request: Request):
        employees = Employees.objects.all()
        serializer = EmployeesSerializer(employees, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = EmployeesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                GROUP_NAME, {"type": "add_notification", "message": serializer.data}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetails(APIView):
    def get(self, request: Request, employee_id: int):
        employee = get_object_or_404(Employees, pk=employee_id)
        serializer = EmployeesSerializer(employee, context={'request': request})
        return Response(serializer.data)

    def put(self, request: Request, employee_id: int):
        print(request.data, file=sys.stderr)
        employee = get_object_or_404(Employees, pk=employee_id)
        serializer = EmployeesSerializer(employee, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                GROUP_NAME, {"type": "update_notification", "message": serializer.data}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        print(serializer.error_messages)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)