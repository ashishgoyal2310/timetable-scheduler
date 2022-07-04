import csv

from django.shortcuts import render
from http import HTTPStatus
from django.http import HttpResponse, JsonResponse

from rest_framework import mixins, generics
from rest_framework.decorators import api_view

from school.models import Subject, ClassSection, Teacher
from school.serializers import SubjectSerializer, ClassSectionSerializer, TeacherSerializer

# Create your views here.
@api_view(['GET'])
def generate_csv(request):
    _response = {'status': 'WIP'}
    class_time_table = {}

    subject_qs = Subject.objects.all()
    period = [0, 1, 2, 3, 4] # 5 period starting from 0 as first period

    occupied_subjects = {obj.name.lower(): [] for obj in subject_qs}
    print(occupied_subjects)

    def set_occupied(name, period):
        if name.lower() not in occupied_subjects:
            occupied_subjects[name.lower()] = []
        occupied_subjects[name.lower()].append(period)

    def is_occupied(name, period):
        return (period in occupied_subjects[name.lower()])

    class_section_qs = ClassSection.objects.filter().order_by("name")

    tmp_subjects = list(occupied_subjects.values())
    for class_section_obj in class_section_qs:
        c_name = class_section_obj.name
        class_subjects = class_section_obj.subjects.order_by("name")
        class_subject_names = {obj.name.lower() for obj in class_subjects}
        print(tmp_subjects)

        time_table = ['Teacher N/A', 'Teacher N/A', 'Teacher N/A', 'Teacher N/A', 'Teacher N/A']
        total_period = period.copy()
        for sub_name in class_subject_names:
            for pos in total_period.copy():
                if is_occupied(sub_name, pos):
                    pass
                else:
                    time_table[pos] = sub_name
                    set_occupied(sub_name, pos)
                    total_period.remove(pos)
                    break
        class_time_table[c_name] = time_table

    with open('timetable.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        for c_name, time_table in class_time_table.items():
            # write the header
            header = ["Class %s" % c_name, '--', '--', '--', '--', '--']
            writer.writerow(header)

            # write the header
            header = ['Day', 'Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5']
            writer.writerow(header)

            # write multiple rows
            time_table.insert(0, 'Day')
            writer.writerow(time_table)
            # for day in ["Mon", "Tue", "Web", "Thu", "Fri"]:
            #     time_table[0] = day
            #     writer.writerow(time_table)

    return JsonResponse(_response, safe=False)


class SubjectListApi(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailApi(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ClassSectionListApi(generics.ListCreateAPIView):
    queryset = ClassSection.objects.all()
    serializer_class = ClassSectionSerializer


class ClassSectionDetailApi(generics.RetrieveAPIView):
    queryset = ClassSection.objects.all()
    serializer_class = ClassSectionSerializer


class TeacherListApi(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class TeacherDetailApi(generics.RetrieveUpdateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
