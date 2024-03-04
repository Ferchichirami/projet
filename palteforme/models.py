from django.db import models

from django.db import models
from user.models import User
from datetime import datetime


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    enrollment_capacity = models.PositiveIntegerField()
    image=models.ImageField(upload_to='courseImages/')

    class Meta:
        db_table="course"
    def __str__(self):
        return self.title 


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        db_table = "lesson"

    def __str__(self):
        return self.title
    

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    class Meta:
        db_table="enrollment"


class Material(models.Model):
    title = models.CharField(max_length=255)
    content = models.FileField(upload_to='materials/') 
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(default=datetime.now())
    document_type = models.CharField(max_length=50)  # e.g., PDF

    class Meta:
        db_table = "material"

    def __str__(self):
        return self.title

class Assignment(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    class Meta:
        db_table="assignment"
    def __str__(self):
        return self.title 
    
class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    studentName = models.CharField(max_length=255,blank=True,default='')
    submission_content = models.TextField()
    submission_date = models.DateField()
    class Meta:
        db_table="submission"
  

class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.FloatField()
    feedback = models.TextField()
    class Meta:
        db_table="grade"
  

class InteractionHistory(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)  # e.g., upload, read
    interaction_date = models.DateTimeField()
    class Meta:
        db_table="interactionHistory"
    

class ReadingState(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    read_state = models.FloatField()  # e.g., percentage completed
    last_read_date = models.DateField()
    class Meta:
        db_table="readingState"
class verif(models.Model):
    needVerification=models.BooleanField(default=False)

NOTIFICATION_TYPES = [
    ('success', 'Success'),
    ('information', 'Information'),
    ('warning', 'Warning'),
    ('danger', 'Danger'),
]


class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_sent')
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='Information')
    targeted_users = models.ManyToManyField(User, through='NotificationTarget', related_name='targeted_adm_notifications', blank=True)

    class Meta:
        db_table="notifi_cation"

class NotificationTarget(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    class Meta:
        db_table="notificationtarget"



class message(models.Model):
    message = models.CharField(max_length=1000)
    username = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sent_messages')
    receiver= models.ForeignKey(User, on_delete=models.CASCADE,related_name='received_messages')
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now())

    class Meta:
        db_table="message"        
# Create your models here.
