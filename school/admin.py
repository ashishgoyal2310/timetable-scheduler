from django.contrib import admin

# Register your models here.
from school.models import Subject, ClassSection, Teacher


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(ClassSection)
class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'class_strength',)
    list_filter = ('subjects',)
    filter_horizontal = ('subjects',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject',)
    list_filter = ('subject', 'class_teaches',)
    raw_id_fields = ['subject']
    filter_horizontal = ('class_teaches',)
