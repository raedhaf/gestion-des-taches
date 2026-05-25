from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    team = models.ForeignKey('tasks.Team', null=True, blank=True, on_delete=models.SET_NULL, related_name='user_team')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.name or self.email

class Team(models.Model):
    name = models.CharField(max_length=150, unique=True)
    members = models.ManyToManyField('tasks.User', related_name='teams', blank=True)
    created_by = models.ForeignKey('tasks.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_teams')

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'À faire'),
        ('done', 'Accomplie'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey('tasks.User', on_delete=models.CASCADE, related_name='created_tasks')
    assigned_users = models.ManyToManyField('tasks.User', related_name='tasks', blank=True)
    assigned_teams = models.ManyToManyField('tasks.Team', related_name='tasks', blank=True)
    parent_task = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.title

    def is_visible_by(self, user):
        if not self.is_private:
            return True
        if self.created_by == user:
            return True
        if user in self.assigned_users.all():
            return True
        user_teams = user.teams.all()
        print("itititi" + str(user_teams))
        if self.assigned_teams.filter(id__in=user_teams).exists():
            return True
        return False
