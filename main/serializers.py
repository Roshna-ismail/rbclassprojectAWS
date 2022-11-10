from dataclasses import fields
from pyexpat import model
from tkinter.ttk import Style
from rest_framework import serializers
from .import models
from main.models import User,Student,Teacher

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','mobile_no','is_student']

class StudentSignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type:password"},write_only=True)
    class Meta:
        model=User
        fields=['username','mobile_no','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def save(self,**kwargs):
        user=User(
            username=self.validated_data['username'],
            mobile_no=self.validated_data['mobile_no']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_student=True
        user.save()
        Student.objects.create(user=user)
        return user

class TeacherSignupSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={"input_type:password"},write_only=True)
    class Meta:
        model=User
        fields=['username','mobile_no','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def save(self,**kwargs):
        user=User(
            username=self.validated_data['username'],
            mobile_no=self.validated_data['mobile_no']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_teacher=True
        user.save()
        Teacher.objects.create(user=user)
        return user


class CourseSerializer(serializers.ModelSerializer):
   class Meta:
       model=models.Course
       fields=['id','category','teacher','title','description','featured_img','techs','total_enrolled_students','course_rating','course_hours','no_lecture','skill_level','duration','enrolled_courses','price']
       # depth=1
   def __init__(self, *args, **kwargs):
       super(CourseSerializer, self).__init__(*args, **kwargs)
       request = self.context.get('request')
       self.Meta.depth=0
       if request and request.method == 'GET':
           self.Meta.depth=1
   #
   # def __init__(self, *args, **kwargs):
   #     super(CourseSerializer, self).__init__(*args, **kwargs)
   #     request = self.context.get('request')
   #     self.Meta.depth=0
   #     if request and request.method == 'GET':
           # self.Meta.depth=1


class TeacherSerializer(serializers.ModelSerializer):
   class Meta:
       model=models.Teacher
       fields=['id','qualification','skills']

class StudentSerializer(serializers.ModelSerializer):
   class Meta:
       model=models.Student
       fields=['id','qualification','start_date']
       extra_kwargs = {
           'password':{'write_only':True}
       }


class CategorySerializer(serializers.ModelSerializer):
   class Meta:
       model=models.CourseCategory
       fields=['id','title','description','Catagory_icon','total_courses']


       def __init__(self, *args, **kwargs):
        super(CourseRatingSerializer,self).__init__(*args, **kwargs)
        request = self.context.get('request')
        self.Meta.depth=0
        if request and request.method == 'GET':
            self.Meta.depth=1


class SectionSerializer(serializers.ModelSerializer):
   class Meta:
       model=models.Section
       fields=['id','course','chapter','title','description','video','remarks','is_active','imageURL']

class ChapterSerializer(serializers.ModelSerializer):
   section = SectionSerializer(many=True)

   class Meta:
       model=models.Chapter
       fields=['id','category','course','title','section']
       # depth=1



class StudentCourseEnrollSerializer(serializers.ModelSerializer):
   class Meta:
       model=models.StudentCourseEnrollment
       fields=['id','course','student','enrolled_time','is_active']
   def __init__(self, *args, **kwargs):
       super(StudentCourseEnrollSerializer, self).__init__(*args, **kwargs)
       request = self.context.get('request')
       self.Meta.depth=0
       if request and request.method == 'GET':
           self.Meta.depth=1

class CourseRatingSerializer(serializers.ModelSerializer):
    class Meta:
       model=models.CourseRating
       fields=['id','course','student','rating','reviews','review_time']
       depth=1
       #
       # def __init__(self, *args, **kwargs):
       #  super(CourseRatingSerializer,self).__init__(*args, **kwargs)
       #  request = self.context.get('request')
       #  self.Meta.depth=0
       #  if request and request.method == 'GET':
       #      self.Meta.depth=1
