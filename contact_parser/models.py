from django.db import models


class ExcelDocument(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_file = models.FileField()


class Contact(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    document = models.ForeignKey(ExcelDocument, on_delete=models.CASCADE)
