from django.db import models
from django.contrib.auth.models import AbstractUser

# Role model
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# User model with extended fields and role management
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    roles = models.ManyToManyField(Role, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)


    @property
    def is_admin(self):
        """Check if the user has admin privileges."""
        return self.is_superuser or self.roles.filter(name__iexact='Admin').exists()

    @property
    def is_taxpayer(self):
        """Check if the user has taxpayer privileges."""
        return self.roles.filter(name__iexact='Taxpayer').exists()

    @property
    def is_auditor(self):
        """Check if the user has auditor privileges."""
        return self.roles.filter(name__iexact='Auditor').exists()

    