from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User,default='', on_delete=models.CASCADE)
#    company = models.(Company, default='', on_delete=models.CASCADE)
    category=(
        ('Male','male'),
        ('Female','female'),
        ('Other','other'),
    )
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio=models.CharField(max_length=200,default=' ',null=True,blank=True)
    dob=models.DateField(null=True)
    gender= models.CharField(max_length=200,null=True,choices=category)
    mobile= models.CharField(max_length=200,null=True)
    resume= models.FileField(null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# Create your models here.
class Company(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    #username=models.CharField(max_length=200,null=True)
    name=models.CharField(max_length=200,null=True)
    position=models.CharField(max_length=200,null=True)
    description=models.CharField(max_length=2000,null=True)
    salary=models.IntegerField(null=True)
    experience=models.IntegerField(null=True)
    Location=models.CharField(max_length=2000,null=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('job',kwargs={'pk':self.pk})

'''class user2(AbstractUser):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    category=(
        ('Male','male'),
        ('Female','female'),
        ('Other','other'),
    )
    name=models.CharField(max_length=200,null=True)
    dob=models.DateField(null=True)
    gender= models.CharField(max_length=200,null=True,choices=category)
    mobile= models.CharField(max_length=200,null=True)
    email= models.CharField(max_length=200,null=True)
    def __str__(self):
       
        return self.name'''

class Candidates(models.Model):
    user = models.ForeignKey(User,default='', on_delete=models.CASCADE)
    category=(
        ('Male','male'),
        ('Female','female'),
        ('Other','other'),
    )
    name=models.CharField(max_length=200,null=True)
    dob=models.DateField(null=True)
    gender= models.CharField(max_length=200,null=True,choices=category)
    mobile= models.CharField(max_length=200,null=True)
    email= models.CharField(max_length=200,null=True)
    resume=models.FileField(null=True)
    company=models.ManyToManyField(Company,blank=True)

    def __str__(self):
        return str(self.user_id)

    # def __iter__(self):
    #     return iter([self.user,
    #             self.dob,
    #             self.gender,
    #             self.mobile,
    #             self.email,
    #             self.resume,
    #             ])