"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Timetable Scheduler (1.0.0)"
admin.site.site_title = "Timetable Scheduler Console"
admin.site.index_title = "Timetable Scheduler Console"
admin.site_url = None

admin.autodiscover()
admin.site.enable_nav_sidebar = True

from http import HTTPStatus
from django.http import JsonResponse
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import OrderedDict


@api_view(['GET'])
def api_root(request, format=None):
    return Response(OrderedDict({
        'subjects': OrderedDict({
            'list': reverse('subject-list', request=request, format=format),
            'detail': reverse('subject-detail', request=request, format=format, kwargs={"pk": 1}),
        }),
        'classes': OrderedDict({
            'list': reverse('classsection-list', request=request, format=format),
            'detail': reverse('classsection-detail', request=request, format=format, kwargs={"pk": 1}),
        }),
        'teachers': OrderedDict({
            'list': reverse('teacher-list', request=request, format=format),
            'detail': reverse('teacher-detail', request=request, format=format, kwargs={"pk": 1}),
        }),
        'generate-csv': reverse('generate_csv', request=request, format=format),
    }))


urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
    path('api/', api_root),
    path('api/v1/', include('school.urls')),
]


def custom_handle_400(request, exception=None):
    status_code = str(HTTPStatus.BAD_REQUEST.value)
    _response = {'code': status_code, 'message': 'BAD REQUEST'}
    return JsonResponse(_response, safe=False, status=status_code)


def custom_handle_403(request, exception=None):
    status_code = str(HTTPStatus.UNAUTHORIZED.value)
    _response = {'code': status_code, 'message': 'PERMISSION DENIED.'}
    return JsonResponse(_response, safe=False, status=status_code)


def custom_handle_404(request, exception=None):
    status_code = str(HTTPStatus.NOT_FOUND.value)
    _response = {'code': status_code, 'message': 'Unknown URL'}
    return JsonResponse(_response, safe=False, status=status_code)


def custom_handle_500(request, exception=None):
    status_code = str(HTTPStatus.INTERNAL_SERVER_ERROR.value)
    _response = {'code': status_code, 'message': 'INTERNAL SERVER ERROR'}
    return JsonResponse(_response, safe=False, status=status_code)


handler400 = custom_handle_400
handler403 = custom_handle_403
handler404 = custom_handle_404
handler500 = custom_handle_500