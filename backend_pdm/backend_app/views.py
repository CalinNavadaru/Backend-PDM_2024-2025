from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import sys
from rest_framework.permissions import IsAuthenticated

from backend_app.models import Employees
from backend_app.serializers import EmployeesSerializer
from .constants import GROUP_NAME
from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.contrib.auth import get_user_model

class Register(APIView):
    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username:
            return Response("Field username not provided!", status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response("Field password not provided!", status=status.HTTP_400_BAD_REQUEST)
        if get_user_model().objects.filter(username=username).exists():
            return Response({"detail": f"The user with the username {username} already exists! Please login."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_user_model().objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        refresh: Token
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    
class EmployeeList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request):
        employees = Employees.objects.filter(manager=request.user)
        serializer = EmployeesSerializer(employees, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request: Request):
        data = request.data
        data['manager'] = request.user.id
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
    permission_classes = [IsAuthenticated]
    def get(self, request: Request, employee_id: int):
        employee = get_object_or_404(Employees, pk=employee_id)
        if employee.manager != request.user:
            return Response("You don't have access to this employee's data!", status=status.HTTP_403_FORBIDDEN)
        serializer = EmployeesSerializer(employee, context={'request': request})
        return Response(serializer.data)

    def put(self, request: Request, employee_id: int):
        employee = get_object_or_404(Employees, pk=employee_id)
        if employee.manager != request.user:
            return Response("You don't have access to modify this employee's data!", status=status.HTTP_403_FORBIDDEN)
        serializer = EmployeesSerializer(employee, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                GROUP_NAME, {"type": "update_notification", "message": serializer.data}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)