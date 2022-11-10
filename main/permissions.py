from rest_framework.permissions import BasePermission



class IsStudentUser(BasePermission):
    def has_Permission(self, request, view):
        return bool(request.user and request.user.is_student)

class IsTeacherUser(BasePermission):
    def has_Permission(self, request, view):
        return bool(request.user and request.user.is_teacher)