from django.db import models

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name


class ClassSection(models.Model):
    name = models.CharField(max_length=64, unique=True)
    class_strength = models.IntegerField(default=0)
    subjects = models.ManyToManyField("Subject", related_name='class_sections')

    def __str__(self) -> str:
        return self.name


class Teacher(models.Model):
    name = models.CharField(max_length=128)
    subject = models.ForeignKey("Subject", on_delete=models.SET_NULL, null=True)
    class_teaches = models.ManyToManyField("ClassSection", related_name='teachers')

    def __str__(self) -> str:
        return self.name