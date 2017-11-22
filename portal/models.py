from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)


class Student(models.Model):
    stud_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    branch = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Guide(models.Model):
    staff_id = models.CharField(max_length=10)
    access_level = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)


class ProjectGuide(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    guide1 = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='guide1')
    guide2 = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='guide2')