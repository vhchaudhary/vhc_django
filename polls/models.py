from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    dob = models.DateField('Date of Birth')
    address = models.TextField(max_length=50)
    mobile = models.CharField(max_length=13)
    bld_group = models.CharField('Blood Group', max_length=3)
    gender = models.CharField(max_length=2)

    def __str__(self):
        return self.name