from django.db import models
from django.contrib.auth.models import User

class Prepaid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prepaid_no = models.CharField(max_length=20)
    current_balance = models.IntegerField()
    expired_date = models.DateField()


class TopUp(models.Model):
    prepaid = models.ForeignKey(Prepaid, on_delete=models.CASCADE)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class History(models.Model):
    prepaid = models.ForeignKey(Prepaid, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)