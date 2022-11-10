from django.urls import path
from .import views
from .views import  StudentSignupView,EnrollCourseList,TeacherSignupView,CustomAuthToken, TeacherOnlyView,LogoutView, StudentOnlyView


urlpatterns = [
    path('signup/student/',StudentSignupView.as_view()),
    path('signup/teacher/',TeacherSignupView.as_view()),
    path('login/',CustomAuthToken.as_view(),name='auth-token'),
    path('login/<int:pk>/',CustomAuthToken.as_view(),name='auth-token'),
    path('logout/',LogoutView.as_view(),name='logout-view'),
    path('student/dashboard/',StudentOnlyView.as_view(),name='student-dashboard'),
    path('teacher/dashboard/',TeacherOnlyView.as_view(),name='teacher-dashboard'),

    path('category/', views.CategoryList.as_view()),
    #course
    path('course/',views.CourseList.as_view()),
    #course
    path('popular-courses/',views.CourseRatingList.as_view()),
    #coursedetail
    path('course-detail/<int:pk>/',views.CourseDetail.as_view()),
    #chapter
    path('chapter/<int:course_id>/',views.ChapterList.as_view()),
    #section
    path('section/',views.SectionList.as_view()),
    path('chapter-section-list/<int:chapter_id>/', views.ChapterSectionList.as_view()),

    # path('fetch-enroll-status_course/', views.fetch_enroll_status_course),

    #Specific Course Section
    path('course-chapter/<int:course_id>/',views.CourseChapterList.as_view()),
    #Teacher Courses
    path('teacher-courses/<int:teacher_id>/', views.TeacherCourseList.as_view()),
    path('student-enroll-course/', views.StudentEnrollCourseList.as_view()),

    path('fetch-enroll-course/<int:student_id>/', views.EnrollCourseList.as_view()),

    path('fetch-enroll-status/<int:course_id>/<int:student_id>/', views.fetch_enroll_status),
    path('course-rating/<int:course_id>/',views.CourseRatingList.as_view()),
    path('fetch-rating-status/<int:course_id>/<int:student_id>/', views.fetch_rating_status),

    path('category-courses-list/<int:category_id>/', views.CategoryCourseList.as_view()),

]
