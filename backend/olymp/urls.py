from django.urls import path, include, re_path
from olymp.olymp_views import OlympViewSet, OneOlympViewSet
from olymp.participant_views import ParticipantViewSet, OneParticipantViewSet
from olymp.result_views import ResultViewSet, OneResultViewSet
from rest_framework.authtoken import views

api = [
    path('olympiada', OlympViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('olympiada/<int:id>', OneOlympViewSet.as_view()),
    path('participant', ParticipantViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('participant/<int:id>', OneParticipantViewSet.as_view()),
    path('results', ResultViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('result/<int:id>', OneResultViewSet.as_view()),
]