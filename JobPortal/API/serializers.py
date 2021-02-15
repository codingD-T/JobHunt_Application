from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from rest_framework import serializers
import json
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from ..models import *
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
)

User = get_user_model()

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]


class UserCreateSerializer(ModelSerializer):
    password = CharField(label='Password')
    password2 = CharField(label='Confirm Password')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2'

        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This user has already registered.")
        return data

    # def validate_password(self, value):
    #     data = self.get_initial()
    #     password1 = data.get("password2")
    #     password2 = value
    #     if password1 != password2:
    #         raise ValidationError("Emails must match.")
    #
    #     user_qs = User.objects.filter(email=password2)
    #     if user_qs.exists():
    #         raise ValidationError("This user has already registered.")
    #
    #     return value

    def validate_password2(self, value):
        data = self.get_initial()
        password1 = data.get("password")
        password2 = value
        if password1 != password2:
            raise ValidationError("Passwords must match.")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username=username,
            email=email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',

        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate(self, data):
        # username = data['username']
        # user_qs = User.objects.filter(username=username)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")
        return data

class CompanyHomeSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields =['id',
            'name',
            'position',
            'salary',
            'experience',
            'Location',
            'description',

        ]

class ApplicantsSerializer(ModelSerializer):
    class Meta:
        model = Candidates
        exclude = ("user","company")

class ApplicantionSerializer(ModelSerializer):
    class Meta:
        model = Company
        exclude = ("profile",)

class GiveProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("user", "image")

class UpdateProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        exclude=("user","image")

    def create(self, validated_data):
        print(validated_data)
        # position = validated_data['image']
        description = validated_data['bio']
        salary = validated_data['dob']
        experience = validated_data['gender']
        Location = validated_data['mobile']
        resume = validated_data['resume']

        user_obj =Profile(
#            image=position,
            bio=description,
            dob=salary,
            gender=experience,
            mobile=Location,
            resume=resume
        )
        print(self.context['request'].user)
        user_obj.user = self.context['request'].user
        try:
            user_obj.save()
        except:
            print("Exception")
            pro = Profile.objects.get(user=self.context['request'].user)
            self.update(pro,validated_data)
        return validated_data

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio',instance.bio)
        instance.dob = validated_data.get('dob',instance.dob)
        instance.gender = validated_data.get('gender',instance.gender)
        instance.mobile = validated_data.get('mobile',instance.mobile)
        instance.resume = validated_data.get('resume',instance.resume)
        instance.save()
        return instance

class PostJobSerializer(ModelSerializer):
    class Meta:
        model = Company
        exclude = ("profile",)

    def create(self, validated_data):
        print(validated_data)
        name = validated_data['name']
        position = validated_data['position']
        description = validated_data['description']
        salary = validated_data['salary']
        experience = validated_data['experience']
        Location = validated_data['Location']

        user_obj = Company(
            name=name,
            position=position,
            description=description,
            salary=salary,
            experience=experience,
            Location=Location
        )
        print("Profile",self.context['request'].user.profile)
        user_obj.profile = self.context['request'].user.profile
        company = Company.objects.filter(profile=self.context['request'].user.profile )
        count=0
        for com in company:
            if com.position  == position:
                count +=1
        if count > 0:
            print(company[0])
            self.update(company[0],validated_data)
            print("1111",company[0],company)
            company = Company.objects.filter(profile=self.context['request'].user.profile)
            print("2222",company)
            company[0].delete()
        else:
            user_obj.save()
        return validated_data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.position = validated_data.get('position',instance.position)
        instance.description = validated_data.get('description',instance.description)
        instance.salary = validated_data.get('salary',instance.salary)
        print("new",validated_data)
        instance.experience = validated_data.get('experience',instance.experience)
        instance.Location = validated_data.get('Location', instance.Location)
        instance.save()
        return instance

class ApplyJobSerializer(ModelSerializer):
    class Meta:
        model = Candidates
        fields = ['dob', 'gender', 'mobile', 'resume']

    # def create(self, validated_data):
    #     dob = validated_data["dob"]
    #     gender = validated_data["gender"]
    #     mobile = validated_data["mobile"]
    #     resume = validated_data["resume"]
    #
    #     candidates = Candidates(
    #         dob=dob,
    #         gender=gender,
    #         mobile = mobile,
    #         resume=resume
    #     )
    #     candidates.user = self.context['request'].user
    #     candidates.name = self.context['request'].user.username
    #     candidates.email = self.context['request'].user.email
    #     com = self.get()
    #     candidates.save()
    #     return validated_data

