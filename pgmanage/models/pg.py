# from django.db import models
# from ..models.pg import PG
# from ..models.pg import PG
# from django.conf import settings

# from django.contrib.auth import get_user_model

# User = get_user_model()

# def some_method():
#     from .pg import PG
# class PG(models.Model):
#     owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="pgs")
#     name=models.CharField(max_length=200)
#     address=models.CharField(max_length=200)
#     secret = models.CharField(max_length=12, blank=True, null=True)
   

#     def save(self, *args, **kwargs):
#         if not self.secret:  # Generate pin only if it doesn't already exist
#             self.secret = self.generate_unique_pin()
#         super().save(*args, **kwargs)

#     def generate_unique_pin(self):
#         contact = self.owner.contact  # Fetch owner's contact number
#         existing_pgs = self.owner.pgs.count()  # Count existing PGs owned by the user
#         suffix = chr(65 + existing_pgs)  # Generate suffix: A, B, C...
#         return f"{contact}{suffix}"

# class TenantProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     pg = models.ForeignKey(PG, on_delete=models.SET_NULL, null=True, blank=True)  # Fixed PG capitalization
#     moveInDate = models.DateField()
#     moveOutDate = models.DateField(null=True, blank=True)
#     roomNumber = models.CharField(max_length=50)
   

#     def __str__(self):
#         return f"{self.user.firstName} {self.user.lastName}"


# pg.py
from django.db import models
from django.conf import settings

class PG(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pgs")
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    secret = models.CharField(max_length=12, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.secret:  # Generate pin only if it doesn't already exist
            self.secret = self.generate_unique_pin()
        super().save(*args, **kwargs)

    def generate_unique_pin(self):
        contact = self.owner.contact  # Fetch owner's contact number
        existing_pgs = self.owner.pgs.count()  # Count existing PGs owned by the user
        suffix = chr(65 + existing_pgs)  # Generate suffix: A, B, C...
        return f"{contact}{suffix}"


