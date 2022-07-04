from xml.dom import ValidationErr
from rest_framework import serializers

from school.models import Subject, ClassSection, Teacher


class SubjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subject
        fields = ['url', 'id', 'name']


class ClassSectionSerializer(serializers.HyperlinkedModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(many=True, queryset=Subject.objects.all(), write_only=True)
    subject_names = serializers.SerializerMethodField(read_only=True)

    def get_subject_names(self, obj):
        return obj.subjects.all().values_list('name', flat=True)

    class Meta:
        model = ClassSection
        fields = ['url', 'id', 'name', 'class_strength', 'subjects', 'subject_names']

    def validate_subjects(self, value):
        if len(value) != 5:
            raise serializers.ValidationError('Should be 5 subject.')
        return value


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class_teaches = serializers.PrimaryKeyRelatedField(many=True, queryset=ClassSection.objects.all(), write_only=True)
    class_teaches_names = serializers.SerializerMethodField(read_only=True)

    def get_class_teaches_names(self, obj):
        return obj.class_teaches.all().values_list('name', flat=True)

    class Meta:
        model = Teacher
        fields = ['url', 'id', 'name', 'subject', 'class_teaches', 'class_teaches_names']