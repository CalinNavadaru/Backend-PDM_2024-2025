import datetime

from django.db import models

from backend_app.validators import validate_greater_than_zero


# Create your models here.
class Employees(models.Model):
    employee_id = models.BigAutoField(primary_key=True)    
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    salary = models.IntegerField(validators=[validate_greater_than_zero])
    date_join = models.DateField(default=datetime.date.today)
    on_field = models.BooleanField()

    class Meta:
        db_table = "employees"