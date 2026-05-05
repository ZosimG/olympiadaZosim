from django.urls import path, include, re_path
from schools.school_views import SchoolViewSet, OneSchoolViewSet, FileUploadView
from schools.subdivision_views import SubdivisionViewSet, OneSubdivisionViewSet, SubdivisionFileUploadView
from rest_framework.authtoken import views

api = [
    path('subdivision', SubdivisionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('subdivision/<int:id>', OneSubdivisionViewSet.as_view()),
    path('school', SchoolViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('school/<int:id>', OneSchoolViewSet.as_view())
]
urlpatterns = [
    re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
    re_path(r'^uploadsubdivision/(?P<filename>[^/]+)$', SubdivisionFileUploadView.as_view()),
]