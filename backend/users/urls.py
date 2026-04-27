from django.urls import path, include, re_path
from users.employee_views import EmployeeViewSet, OneEmployeeViewSet
from users.user_views import GenderViewList, RoleViewList
from users.user_views import UserViewSet, OneUserViewSet
from rest_framework.authtoken import views

api = [
    path('employee', EmployeeViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('employee/<int:id>', OneEmployeeViewSet.as_view()),
    path('user', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('user/<int:id>', OneUserViewSet.as_view()),
    path('getgenders', GenderViewList.as_view()),
    path('getroles', RoleViewList.as_view())
]