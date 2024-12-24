
from django.db import models
from django.conf import settings
from ..models.pg import PG
from django.contrib.auth import get_user_model

User = get_user_model()



class TenantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL here
    pg = models.ForeignKey('pgmanage.PG', on_delete=models.SET_NULL, null=True, blank=True)  # Use string reference here
    moveInDate = models.DateField(null=True, blank=True)
    moveOutDate = models.DateField(null=True, blank=True)
    roomNumber = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return f"{self.user.firstName} {self.user.lastName} - {self.pg.name if self.pg else 'No PG'}"