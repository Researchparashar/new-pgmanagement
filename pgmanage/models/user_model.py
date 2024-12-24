# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models
# from django.core.exceptions import ValidationError
# import re
# from ..models.pg import PG


# # User Manager
# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field is required")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_superuser", True)
#         extra_fields.setdefault("is_staff", True)
#         return self.create_user(email, password, **extra_fields)

# # User Model
# class User(AbstractBaseUser, PermissionsMixin):
#     ROLE_CHOICES = [("owner", "Owner"), ("tenant", "Tenant")]
#     pg = models.ForeignKey(PG, null=True, blank=True, on_delete=models.SET_NULL, related_name="tenants")
#     email = models.EmailField(unique=True)
#     firstName = models.CharField(max_length=50)
#     lastName = models.CharField(max_length=50)
#     contact = models.CharField(max_length=15)
#     adharNumber = models.CharField(max_length=12)
#     adharImage = models.ImageField(upload_to='adhar_images/', null=True, blank=True)  # Image Field for Aadhar card
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     roomNumber=models.CharField(max_length=100)
#     objects = UserManager()

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["firstName", "lastName", "role"]

#     groups = models.ManyToManyField(
#         'auth.Group', 
#         related_name="pgmanage_user_groups", 
#         blank=True, 
#         help_text="The groups this user belongs to.",
#         verbose_name="groups"
#     )

#     user_permissions = models.ManyToManyField(
#         'auth.Permission', 
#         related_name="pgmanage_user_permissions", 
#         blank=True, 
#         help_text="Specific permissions for this user.",
#         verbose_name="user permissions"
#     )

#     def __str__(self):
#         return f"{self.email} - {self.role}"

#     # Aadhar card validator to ensure the format is valid
#     def clean(self):
#         super().clean()
#         if not re.match(r"^\d{12}$", self.adharNumber):
#             raise ValidationError("Aadhar card number must be a 12-digit number.")
# user_model.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
import re
from django.conf import settings
from ..models.pg import PG


# User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(email, password, **extra_fields)

# User Model
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [("owner", "Owner"), ("tenant", "Tenant")]
    # Use string reference here to avoid circular import
    # pg = models.ForeignKey('pgmanage.PG', null=True, blank=True, on_delete=models.SET_NULL, related_name="tenants")
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    adharNumber = models.CharField(max_length=12)
    adharImage = models.ImageField(upload_to='adhar_images/', null=True, blank=True)  # Image Field for Aadhar card
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    
    roomNumber = models.CharField(max_length=50)
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["firstName", "lastName", "role"]

    groups = models.ManyToManyField(
        'auth.Group', 
        related_name="pgmanage_user_groups", 
        blank=True, 
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name="pgmanage_user_permissions", 
        blank=True, 
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )

    def __str__(self):
        return f"{self.email} - {self.role}"

    # Aadhar card validator to ensure the format is valid
    def clean(self):
        super().clean()
        if not re.match(r"^\d{12}$", self.adharNumber):
            raise ValidationError("Aadhar card number must be a 12-digit number.")
        if self.adharImage:
            # You can also add further checks for image format and size if needed
            pass
