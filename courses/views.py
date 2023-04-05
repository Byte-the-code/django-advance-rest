from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from courses.serializers import CourseSerializer
from courses.models import Course


class CoursesView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

