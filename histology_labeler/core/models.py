from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class SlideImage(models.Model):
    title = models.CharField(max_length=200)
    image_file = models.ImageField(upload_to='slides/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Annotation(models.Model):
    slide = models.ForeignKey(SlideImage, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Case(models.Model):
    patient_id = models.CharField(max_length=20)
    diagnosis = models.CharField(max_length=100)
    age = models.IntegerField()
    gene_mutation = models.CharField(max_length=100, blank=True)
    ihc_results = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Case {self.patient_id} - {self.diagnosis}'
