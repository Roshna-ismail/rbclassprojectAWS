from multiprocessing import context
from unicodedata import category
from venv import create
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import StudentCourseEnrollSerializer, StudentSignupSerializer,UserSerializer,TeacherSignupSerializer,TeacherSerializer,CategorySerializer,StudentSerializer,CourseSerializer,ChapterSerializer,CourseRatingSerializer,SectionSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .permissions import IsStudentUser,IsTeacherUser
from rest_framework import permissions
from .import models
from .serializers import StudentSerializer
from django.http import JsonResponse




class StudentSignupView(generics.GenericAPIView):
    serializer_class=StudentSignupSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            # "message":"account created successfully"
        })


class TeacherSignupView(generics.GenericAPIView):
    serializer_class=TeacherSignupSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            # "message":"account created successfully"
        })

class CustomAuthToken(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user':UserSerializer(user, context=self.get_serializer_context()).data,
            'is_student':user.is_student
        })


class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)



class StudentOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsStudentUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user


class TeacherOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsTeacherUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user




class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
        queryset=models.Teacher.objects.all()
        serializer_class=TeacherSerializer
        # permission_classes=[permissions.IsAuthenticated]


class StudentList(generics.ListCreateAPIView):
    queryset=models.Student.objects.all()
    serializer_class=StudentSerializer
    # permission_classes=[permissions.IsAuthenticated]
# awash lo update w dele w spesfic data
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
        queryset=models.Student.objects.all()
        serializer_class=StudentSerializer
        # permission_classes=[permissions.IsAuthenticated]

# class CategoryList(generics.ListCreateAPIView):
#     queryset=models.CourseCategory.objects.all()
#     serializer_class=CategorySerializer

class CategoryList(generics.ListCreateAPIView):
    queryset=models.CourseCategory.objects.all()
    serializer_class=CategorySerializer




#allcourses
class CourseDetail(generics.RetrieveAPIView):
    queryset=models.Course.objects.all()
    serializer_class=CourseSerializer

#lastcourses
class CourseList(generics.ListCreateAPIView):
    queryset=models.Course.objects.all()
    serializer_class=CourseSerializer
    # pagination_class=StandardResultsSetPagination

    def get_queryset(self):
        qs=super().get_queryset()
        if 'result' in self.request.GET:
            limit=int(self.request.Get['result'])
            qs=models.Course.objects.all().order_by('-id')[:limit]
        if 'category' in self.request.GET:
            category=self.request.GET['category']
            category=models.CourseCategory.objects.filter(id=category).first()
            qs=models.Course.objects.filter(category=category)
        return qs


        # if 'course' in self.request.GET:
        #     chapter=self.request.GET['course']
        #     course=models.CourseCategory.objects.filter(id=category).first()
        #     qs=models.Course.objects.filter(category=category)
        # return qs




#specific Teacher course
class TeacherCourseList(generics.ListAPIView):
    serializer_class=CourseSerializer

    def get_queryset(self):
        teacher_id=self.kwargs['teacher_id']
        teacher=models.User.objects.get(pk=teacher_id)
        return models.Course.objects.filter(teacher=teacher)



#specific Teacher course
class CategoryCourseList(generics.ListAPIView):
    serializer_class=CourseSerializer

    def get_queryset(self):
        category_id=self.kwargs['category_id']
        category=models.CourseCategory.objects.get(pk=category_id)
        return models.Course.objects.filter(category=category)



#chapterx
class ChapterList(generics.ListCreateAPIView):
    queryset=models.Chapter.objects.all()

    serializer_class=ChapterSerializer


    def get_queryset(self):
        course_id=self.kwargs['course_id']
        course=models.Course.objects.get(pk=course_id)
        return models.Chapter.objects.filter(course=course)







class CourseChapterList(generics.ListAPIView):
    serializer_class=ChapterSerializer

    def get_queryset(self):
        course_id=self.kwargs['course_id']
        course=models.Course.objects.get(pk=course_id)
        return models.Chapter.objects.filter(course=course)



class SectionList(generics.ListCreateAPIView):
    queryset=models.Section.objects.all()
    serializer_class=SectionSerializer


class ChapterSectionList(generics.ListAPIView):
    serializer_class=SectionSerializer

    def get_queryset(self):
        chapter_id=self.kwargs['chapter_id']
        chapter=models.Chapter.objects.get(pk=chapter_id)
        return models.Section.objects.filter(chapter=chapter)



class StudentEnrollCourseList(generics.ListCreateAPIView):
    queryset=models.StudentCourseEnrollment.objects.all()
    serializer_class=StudentCourseEnrollSerializer

def fetch_enroll_status(request,student_id,course_id,*args,**kwargs):

    student=models.User.objects.filter(id=student_id).first()
    course=models.Course.objects.filter(id=course_id).first()
    enrollStatus=models.StudentCourseEnrollment.objects.filter(course=course,student=student,is_active=True).count()
    if enrollStatus:
        return JsonResponse({'bool':True,'is_active':True})


    else:
        return JsonResponse({'bool':False})

#
# ,"user": StudentCourseEnrollSerializer(user).data,
# user=models.StudentCourseEnrollment.objects






class EnrollCourseList(generics.ListAPIView):
    queryset=models.StudentCourseEnrollment.objects.all()
    serializer_class=StudentCourseEnrollSerializer

    def get_queryset(self):
        if 'student_id' in self.kwargs:
            student_id=self.kwargs['student_id']
            student=models.User.objects.get(pk=student_id)
            return models.StudentCourseEnrollment.objects.filter(student=student).distinct()



class CourseRatingList(generics.ListCreateAPIView):
    queryset=models.CourseRating.objects.all()
    serializer_class=CourseRatingSerializer

    def get_queryset(self):
        if 'popular' in self.request.GET:
            sql="SELECT *,AVG(cr.rating) as avg_rating FROM main_courserating as cr INNER JOIN main_course as c ON cr.course_id=c.id GROUP BY c.id ORDER BY avg_rating desc LIMIT 4"
            return models.CourseRating.objects.raw(sql)
        if 'all' in self.request.GET:
            sql="SELECT *,AVG(cr.rating) as avg_rating FROM main_courserating as cr INNER JOIN main_course as c ON cr.course_id=c.id GROUP BY c.id ORDER BY avg_rating desc"
            return models.CourseRating.objects.raw(sql)
    #
    # def get_queryset(self):
    #     course_id=self.kwargs['course_id']
    #     course=models.Course.objects.get(pk=course_id)
    #     return models.CourseRating.objects.filter(course=course)

def fetch_rating_status(request,student_id,course_id):
    student=models.User.objects.filter(id=student_id).first()
    course=models.Course.objects.filter(id=course_id).first()
    ratingStatus=models.CourseRating.filter(course=course,student=student).count()
    if ratingStatus:
        return JsonResponse({'bool':True,})
    else:
        return JsonResponse({'bool':False})
