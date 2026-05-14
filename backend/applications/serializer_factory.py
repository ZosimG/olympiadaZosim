from common.serializers import ApplicationSerializer, StudentSerializer


def get_application_serializer():
    return ApplicationSerializer

def get_student_serializer():
    return StudentSerializer