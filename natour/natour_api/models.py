from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator, RegexValidator

class User(models.Model):
    name = models.CharField(
        max_length=100, 
        null=False, 
        blank=False, 
        validators=[MinLengthValidator(3)]
    )
    email = models.EmailField(unique=True, null=False, blank=False)
    cpf = models.CharField(
        max_length=11, 
        null=False, 
        blank=False, 
        unique=True, 
        validators=[MinLengthValidator(11)]
    )
    date_of_birth = models.DateField(null=False, blank=False)
    phone_number = models.CharField(
        max_length=15, 
        null=False, 
        blank=False, 
        validators=[
            MinLengthValidator(10),
            RegexValidator(regex=r'^\+55\d{2}(?:9\d{8}|\d{8})$', message="O número de telefone deve estar no formato '+55DDXXXXXXXXX' ou '+55DDXXXXXXXX'.")
        ]
    )
    password = models.CharField(
        max_length=100, 
        null=False, 
        blank=False, 
        validators=[MinLengthValidator(8)]
    )
    passwordConfirm = models.CharField(
        max_length=100, 
        null=True, 
        blank=False, 
        validators=[MinLengthValidator(8)]
    )
    photo = models.ImageField(upload_to='Images/', default='Images/doc.jpg')
    ROLE_CHOICES = [
        ('master', 'Master'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='user')
    is_active = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['name', 'cpf', 'date_of_birth', 'phone_number']

    def save(self, *args, **kwargs):
        if not self.pk or 'password' in self.get_dirty_fields():
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-createdAt']
        verbose_name = 'User'
        verbose_name_plural = 'Users'