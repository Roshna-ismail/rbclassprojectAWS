from distutils.command.upload import upload
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from tabnanny import verbose
from unicodedata import category
from django.core import serializers
from weakref import proxy
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin, BaseUserManager,AbstractUser



class User(AbstractUser):
    is_student=models.BooleanField(default=False)
    is_teacher=models.BooleanField(default=False)
    mobile_no=models.CharField(max_length=200,blank=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural="1.User"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)





   #Teacher Model
class Teacher(models.Model):
    user=models.OneToOneField(User,default='SOME STRING',on_delete=models.CASCADE,primary_key=True)
    qualification=models.CharField(max_length=200,null=True,blank=True)
    skills=models.TextField(null=True,blank=True)

    # def __str__(self):
    #     return self.qualification

    class Meta:
        verbose_name_plural="2.Teacher"



   #Student Model
class Student(models.Model):
    user=models.OneToOneField(User,default='SOME STRING',on_delete=models.CASCADE,primary_key=True)
    qualification=models.CharField(max_length=200,blank=True)
    start_date= models.DateTimeField(default=timezone.now,blank=True)


    def __str__(self) :
        return   self.user

    class Meta:
        verbose_name_plural="3.Students"





    #Course Category Model
class CourseCategory(models.Model):
    title=models.CharField(max_length=150)
    description=models.TextField()
    Catagory_icon=models.CharField(max_length=150,null=True)


    class Meta:
        verbose_name_plural="4.Course Categories"

    def total_courses(self):
        return Course.objects.filter(category=self).count()

    def __str__(self) :
        return   self.title

    #Course  Model
class Course(models.Model):
    category=models.ForeignKey(CourseCategory,on_delete=models.CASCADE)
    teacher=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    description=models.TextField()
    featured_img=models.CharField(max_length=150,null=True)
    techs=models.TextField(null=True)
    course_hours=models.CharField(max_length=150,null=True)
    no_lecture=models.CharField(max_length=150,null=True)
    skill_level=models.CharField(max_length=150,null=True)
    duration=models.CharField(max_length=150,null=True)
    price=models.CharField(max_length=150,null=True)






    def __str__(self) :
        return   self.title

    class Meta:
        verbose_name_plural="5.Courses"

    def total_enrolled_students(self):
        total_enrolled_students=StudentCourseEnrollment.objects.filter(course=self).count()
        return total_enrolled_students

    def related_videos(self):
        related_videos=Course.objects.filter(techs__icontains=self.techs)
        return serializers.Serialize('json',related_videos)

    def course_rating(self):
        course_rating=CourseRating.objects.filter(course=self).aggregate(avg_rating=models.Avg('rating'))
        return course_rating['avg_rating']




class Chapter(models.Model):
    category=models.ForeignKey(CourseCategory,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='course_chapters')
    title=models.CharField(max_length=150)


    @property
    def section(self):
        return self.section_set.all()


    class Meta:
        verbose_name_plural="6.Chapters"

    def __str__(self) :
        return   f"{self.course}-{self.title}"


class Section(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    chapter=models.ForeignKey(Chapter,on_delete=models.CASCADE)
    title=models.CharField(max_length=150)
    description=models.TextField()
    video=models.CharField(max_length=150,null=True)
    remarks=models.TextField(null=True)
    is_active=models.BooleanField(default=False)
    imageURL=models.CharField(max_length=150,null=True)



    def __str__(self) :
        return   f"{self.chapter}-{self.title}"

    class Meta:
        verbose_name_plural="7.Section"

#student course enrollment
class StudentCourseEnrollment(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE,related_name='enrolled_courses')
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name='enrolled_student')
    is_active=models.BooleanField(default=False)
    enrolled_time=models.DateTimeField(auto_now_add=True)

    
    class Meta:
       unique_together = ("course", "student")


    class Meta:
        verbose_name_plural="8.Enrolled Courses"

    def __str__(self) :
        return   f"{self.course}-{self.student}-{self.is_active}"




#Course Rating and Reviews
class CourseRating(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    student=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveBigIntegerField(default=0)
    reviews=models.TextField(null=True)
    review_time=models.DateTimeField(auto_now_add=True)



    class Meta:
        verbose_name_plural="9.Course Rating"

    # def __str__(self) :
    #     return   f"{self.course}-{self.student}-{self.rating}"
