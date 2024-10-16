from django.urls import path
from . import consumers
from backend_app.views import EmployeeList, EmployeeDetails
from .consumers import EmployeeConsumer

urlpatterns = [
    path('', EmployeeList.as_view(), name='employees-list'),
    path('<int:employee_id>/', EmployeeDetails.as_view(), name='employees-detail')
]

websocket_urlpatterns = [
    path('ws/employees/', EmployeeConsumer.as_asgi(), name="employee-consumer")
]