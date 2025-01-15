import datetime
from django.db import models
from backend_app.validators import validate_greater_than_zero
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model


class EmployeesManagerManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)
    

class EmployeesManager(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    objects = EmployeesManagerManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = "EmployeesManager"

class Employees(models.Model):
    employee_id = models.BigAutoField(primary_key=True)    
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    salary = models.IntegerField(validators=[validate_greater_than_zero])
    date_join = models.DateField(default=datetime.date.today)
    on_field = models.BooleanField()
    manager = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='employees')
    profile_picture = models.BinaryField(null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    class Meta:
        db_table = "Employees"
