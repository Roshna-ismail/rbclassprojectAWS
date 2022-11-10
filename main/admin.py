from django.contrib import admin
from . import models
# from django.contrib.auth.admin import UserAdmin

# class UserAdminConfig(UserAdmin):
#     pass

# Register your models here.
# class AuthorAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Author, AuthorAdmin)

admin.site.register(models.User)
admin.site.register(models.Teacher)
admin.site.register(models.Student)
admin.site.register(models.CourseCategory)
admin.site.register(models.Course)
admin.site.register(models.Chapter)
admin.site.register(models.Section)
admin.site.register(models.StudentCourseEnrollment)
admin.site.register(models.CourseRating)
