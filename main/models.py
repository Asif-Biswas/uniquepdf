from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    contact = models.CharField(max_length=10)
    student_id = models.CharField(max_length=200)
    graduationyear = models.IntegerField()
    certificate_id = models.CharField(max_length=10, default="000000")
    transcript_id = models.CharField(max_length=10, default="000000")
    
    def __str__(self):
        return self.username