from rest_framework import serializers
from .models import *
from user.models import User
from user.serializers import UserSerializer
class CourseSerializer(serializers.ModelSerializer):
    # tutor=UserSerializer()
    class Meta:
        model = Course
        fields = '__all__'
        
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    # course=CourseSerializer()
    class Meta:
        model = Material
        fields = '__all__'                
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    # assignment=AssignmentSerializer()
    # student=UserSerializer()
    class Meta:
        model = Grade
        fields = '__all__'

class InteractionHistorySerializer(serializers.ModelSerializer):
    student =UserSerializer()
    material=MaterialSerializer()
    class Meta:
        model = Course
        fields = '__all__'
class ReadingStateSerializer(serializers.ModelSerializer):
    student =UserSerializer()
    material=MaterialSerializer()
    class Meta:
        model = Course
        fields = '__all__'














