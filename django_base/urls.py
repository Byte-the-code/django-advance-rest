from django.contrib import admin
from django.urls import path, include

from django_base.views import HelloWorldView

from courses.views import CoursesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello-world/', HelloWorldView.as_view(), name='hello_world'),
    path('course/', CoursesView.as_view(), name='course')

]
