import uuid

from django.db import models


class Plan(models.TextChoices):
    HOBBY = 'Hobby'
    PRO = 'Pro'


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    plan = models.CharField(max_length=5, choices=Plan.choices, default=Plan.HOBBY)

    def __str__(self):
        return f'{self.username} ({self.plan})'


class DeployedApp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apps')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'App {self.id} - Active: {self.active}'
