from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ExpenseModel(models.Model):
    title=models.CharField(max_length=30)
    amount=models.IntegerField()

    category_choices=[('food','FOOD'),
                      ('travel','TRAVEL'),
                      ('bill','BILL'),
                      ('health','HEALTH'),
                      ('shopping','SHOPPING'),
                      ('entertainment','ENTERTAINMENT'),
                      ('others','OTHERS')]
    category=models.CharField(max_length=30,choices=category_choices)

    priority_choices=[("need",'NEED'),
                      ('want','WANT')]
    priority=models.CharField(max_length=30,choices=priority_choices)

    payment_choices=[("upi",'UPI'),
                     ('cash','CASH')]
    payment=models.CharField(max_length=30,choices=payment_choices)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    owner= models.ForeignKey(User,on_delete=models.CASCADE,related_name="expenses")
