# Create a test owner
from ..pgmanage.models.pg import PG
from django.contrib.auth import get_user_model
User = get_user_model()




owner = User.objects.create_user(
    email="owner@example.com",
    password="password123",
    firstName="John",
    lastName="Doe",
    contact="8770262787",
    role="owner",
    secret='secret'
)

# Create PGs for the owner
pg1 = PG.objects.create(owner=owner, name="PG 1", address="Address 1")
print(pg1.secret)  # Should output: 8770262787A

pg2 = PG.objects.create(owner=owner, name="PG 2", address="Address 2")
print(pg2.secret)  # Should output: 8770262787B

pg3 = PG.objects.create(owner=owner, name="PG 3", address="Address 3")
print(pg3.secret)  # Should output: 8770262787C
