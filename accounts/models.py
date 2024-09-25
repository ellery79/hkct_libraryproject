from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Rule(models.Model):
    rule_name = models.CharField(max_length=200)
    fine_per_day = models.DecimalField(max_digits=3, decimal_places=1)
    reserve_limit = models.IntegerField()
    borrow_limit = models.IntegerField()
    borrow_period = models.IntegerField(default=14)
    reserve_period = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.rule_name


class CustomUser(AbstractUser):
    rule = models.ForeignKey(
        Rule, on_delete=models.DO_NOTHING, blank=True, null=True)
    card_id = models.CharField(max_length=200, blank=True, null=True)
    user_phone = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username
