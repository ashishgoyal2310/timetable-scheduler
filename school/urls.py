from django.urls import path, re_path

from school import views

urlpatterns = []

urlpatterns += [
    path('subjects/', views.SubjectListApi.as_view(), name='subject-list'),
    path('subjects/<int:pk>/', views.SubjectDetailApi.as_view(), name='subject-detail'),

    path('classes/', views.ClassSectionListApi.as_view(), name='classsection-list'),
    path('classes/<int:pk>/', views.ClassSectionDetailApi.as_view(), name='classsection-detail'),

    path('teachers/', views.TeacherListApi.as_view(), name='teacher-list'),
    path('teachers/<int:pk>/', views.TeacherDetailApi.as_view(), name='teacher-detail'),

    path('generate/', views.generate_csv, name='generate_csv'),
]
