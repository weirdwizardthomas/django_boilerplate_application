from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q
from django.db.models.signals import post_save
from django.dispatch import receiver


class Shift(models.Model):
    start = models.DateField()
    end = models.DateField()

    def clean(self):
        super().clean()
        if not self.start <= self.end:
            raise ValidationError('Invalid start and end datetime')

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(start__lte=F('end')), name='Start must be before end')
        ]


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shifts = models.ManyToManyField(Shift)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.employee.save()
