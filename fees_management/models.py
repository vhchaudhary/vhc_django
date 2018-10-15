import pdb

from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, AbstractUser
from django_extensions.db.models import TimeStampedModel


class Institute(TimeStampedModel):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50, unique=True)
    logo = models.BinaryField()
    email = models.EmailField(max_length=35)
    contact_no = models.CharField(max_length=13)
    is_active = models.BooleanField(default=True)

    def delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.name


class Branch(TimeStampedModel):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=50, unique=True)
    brochure = models.FileField()
    email = models.EmailField(max_length=35)
    address = models.TextField(max_length=60)
    contact_no = models.CharField(max_length=13)
    is_active = models.BooleanField(default=True)

    # def delete(self):
    #     self.is_active = False
    #     self.save()

    def __str__(self):
        return self.name


class Fee(TimeStampedModel):
    fee_type = models.CharField(max_length=15)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    is_active = models.BooleanField(default=True)

    def delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.fee_type


class Course(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Student(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enr_no = models.CharField('Enrollment No', unique=True, max_length=10)
    branch = models.OneToOneField(Branch, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    address = models.TextField(max_length=60)
    contact_no = models.CharField(max_length=13)
    dob = models.DateField('Date Of Birth')
    is_active = models.BooleanField(default=True)

    def delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.user.username


STATUS = (('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'))


class Transaction(TimeStampedModel):
    uuid =  models.CharField(primary_key=True, max_length=50)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    paid_amount = models.FloatField()
    status = models.CharField(choices=STATUS, max_length=10)
    request_dump = models.CharField(max_length=200)

