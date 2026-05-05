from django.urls import path, include, re_path
from applications.application_views import ApplicationUploadView, ApplicationViewSet, OneApplicationViewSet, ChangeApplicationStatus, ChangeApplicationStatusMultiple
from applications.country_views import CountryViewSet, OneCountryViewSet
from applications.student_views import StudentViewSet, OneStudentViewSet, StudentFromOlympViewList
from applications.application_gen_views import ApplicationGenView
from rest_framework.authtoken import views


api = [
    path('application', ApplicationViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('application/<int:id>', OneApplicationViewSet.as_view()),
    path('applicationstatus/<int:id>', ChangeApplicationStatus.as_view()),
    path('applicationstatuses', ChangeApplicationStatusMultiple.as_view()),
    path('getapplicationexcel/<int:olymp_id>', ApplicationGenView.as_view()),
    path('country/<int:id>', OneCountryViewSet.as_view()),
    path('country', CountryViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('student/<int:id>', OneStudentViewSet.as_view()),
    path('student', StudentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('getstudentfromolymp/<int:olymp_id>', StudentFromOlympViewList.as_view({'get': 'list'})),
]
urlpatterns = [
    re_path(r'^upload/participants/(?P<olymp_id>\d+)/(?P<filename>[^/]+)$', ApplicationUploadView.as_view()),
]