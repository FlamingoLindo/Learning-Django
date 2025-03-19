import datetime
import secrets
import string

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        validators=[MinLengthValidator(3)]
    )
    email = models.EmailField(unique=True, null=False, blank=True)
    cpf = models.CharField(
        max_length=11,
        null=False,
        blank=True,
        unique=True,
        validators=[MinLengthValidator(11)]
    )
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=15,
        null=False,
        blank=True,
        validators=[
            MinLengthValidator(10),
            RegexValidator(regex=r'^\+55\d{2}(?:9\d{8}|\d{8})$', message="O número de telefone deve estar no formato '+55DDXXXXXXXXX' ou '+55DDXXXXXXXX'.")
        ]
    )
    password = models.CharField(
        max_length=128,
        null=False,
        blank=True
    )

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_expires = models.DateTimeField(blank=True, null=True)

    photo = models.ImageField(upload_to='Images/', blank=True, null=True, default='Images/doc.jpg')
    ROLE_CHOICES = [
        ('master', 'Master'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'cpf', 'date_of_birth', 'phone_number']

    def get_natural_key(self):
        return self.email

    def __str__(self):
        return self.name
    
    def set_verification_code(self):
        self.verification_code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6)).upper()
        self.verification_expires = timezone.now() + datetime.timedelta(minutes=10)
        self.save(update_fields=['verification_code', 'verification_expires'])

    class Meta:
        ordering = ['-createdAt']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Point(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    url = models.URLField(null=False, blank=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=False, blank=False)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=False, blank=False)
    view = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    score = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='Images/', blank=True, null=True, default='Images/doc.jpg')
    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='points'
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-createdAt']
        verbose_name = 'Point'
        verbose_name_plural = 'Points'

class Review(models.Model):
    point = models.ForeignKey(
        'Point',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    comment = models.TextField(null=False, blank=True)
    star = models.IntegerField(null=False, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.point.name}"

    class Meta:
        ordering = ['-createdAt']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

class Term(models.Model):
    use_terms = models.TextField(null=False, blank=False)
    politics = models.TextField(null=False, blank=False)

    class Meta:
        verbose_name = 'Term'
        verbose_name_plural = 'Terms'