from datetime import timezone
from django.db import models

from django.db import models
from user.models import User


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment_capacity = models.PositiveIntegerField()
        
    class Meta:
        db_table="Course"
    def __str__(self):
        return self.title 

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    class Meta:
        db_table="Enrollment"


class Material(models.Model):
    title = models.CharField(max_length=255)
    content = models.FileField(upload_to='materials/') 
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    upload_date = models.DateField()
    document_type = models.CharField(max_length=50)  # e.g., PDF
    class Meta:
        db_table="Material"
    def __str__(self):
        return self.title 

class Assignment(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    class Meta:
        db_table="Assignment"
    def __str__(self):
        return self.title 
    
class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    studentName = models.CharField(max_length=255,blank=True,default='')
    submission_content = models.TextField()
    submission_date = models.DateField()
    class Meta:
        db_table="Submission"
  

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.FloatField()
    feedback = models.TextField()
    class Meta:
        db_table="Grade"
  

class InteractionHistory(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)  # e.g., upload, read
    interaction_date = models.DateTimeField()
    class Meta:
        db_table="InteractionHistory"
    

class ReadingState(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    read_state = models.FloatField()  # e.g., percentage completed
    last_read_date = models.DateField()
    class Meta:
        db_table="ReadingState"
  


# Create your models here.
