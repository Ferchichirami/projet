from ast import List
import base64
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import FileResponse
from django.shortcuts import render
from .models import *
from rest_framework import viewsets,authentication,permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.utils import timezone
from .serializers import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




@api_view(['POST'])
def change_verification_status(request):
    new_status = request.data.get('new_status')
    if new_status not in [True,False]:
        return Response({'message': 'Invalid new_status parameter'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        verif_instance = verif.objects.get(id=1)
    except verif.DoesNotExist:
        return Response({'message': 'Verif instance does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    verif_instance.needVerification =new_status
    verif_instance.save()

    return Response({'message': 'value changed'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_verif_status(request):
    try:
            verif_instance = verif.objects.get(id=1)
    except verif.DoesNotExist:
            return Response({'message': 'Verif instance does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'needVerification': verif_instance.needVerification}, status=status.HTTP_200_OK)



@api_view(['GET', 'POST'])
def course_list(request):
    if request.method == 'GET':
    
        courses = Course.objects.all()
        serialized_courses = []
        for course in courses:
             serializer = CourseSerializer(course)
             image_path = course.image.path
             if os.path.exists(image_path):
                  with open(image_path, "rb") as img_file:
                         encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
                         course_data = serializer.data
                         course_data['image'] = f"data:image/jpeg;base64,{encoded_image}"
                         serialized_courses.append(course_data)
             else:
                    return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND) 
        return Response(serialized_courses)



    

    elif request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['POST'])
def postlesson(request):
     if request.method == 'POST':
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def lesson_by_course(request, pk):
    try:

        lessons = Lesson.objects.filter(course__id=pk)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    



@api_view(['GET', 'PUT', 'DELETE'])
def lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    if request.method == 'GET':
        serializer =LessonSerializer(lesson)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def courses_by_tutor(request, tutor_id):
    try:
        courses = Course.objects.filter(tutor__id=tutor_id)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        

@api_view(['GET', 'POST'])
def material_list(request):
    if request.method == 'GET':
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def material_detail(request, pk):
    try:
        material = Material.objects.get(pk=pk)
    except Material.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MaterialSerializer(material)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MaterialSerializer(material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def materials_by_course(request, lesson_id):
    if request.method == 'GET':
        try:
            materials = Material.objects.filter(lesson__id=lesson_id)
            serializer = MaterialSerializer(materials, many=True)
            return Response(serializer.data)
        except Material.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['lesson'] = Lesson.objects.get(pk=lesson_id)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_pdf(request, file_name):
    # Validate and sanitize file_name as needed
    file_path = os.path.join('media/materials', file_name)

    try:
        with open(file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{smart_str(file_name)}"'
            return response
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    

# @csrf_exempt
# def upload_pdf(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         course = request.POST.get('course')
#         content = request.FILES.get('content')
#         upload_date = timezone.now()

#         if title and description and content:
#             Material.objects.create(title=title,course=course,content=content,upload_date=upload_date,description=description)
#             return JsonResponse({'message': 'File uploaded successfully'})
#         else:
#             return JsonResponse({'message': 'Incomplete data provided'}, status=400)
#     else:
#         return JsonResponse({'message': 'Invalid request method'}, status=405)


@api_view(['GET', 'POST'])
def enrollment_list(request):
    if request.method == 'GET':
        enrollments = Enrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def enrollment_detail(request, pk):
    try:
        enrollment = Enrollment.objects.get(pk=pk)
    except Enrollment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EnrollmentSerializer(enrollment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
def enrollement_by_student(request, student_id):
    if request.method == 'GET':
        try:
            enrollment = Enrollment.objects.filter(student__id=student_id)
            serializer = EnrollmentSerializer(enrollment, many=True)
            return Response(serializer.data)
        except Enrollment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == 'POST':
        try:
            data = request.data
            data['student'] = student_id
            data['enrollment_date'] = timezone.now()
            serializer = EnrollmentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['GET', 'POST'])
def assignment_list(request):
    if request.method == 'GET':
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def assignment_detail(request, pk):
    try:
        assignment = Assignment.objects.get(pk=pk)
    except Assignment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AssignmentSerializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def assignment_by_tutor(request, tutor_id):
    try:
        assignments = Assignment.objects.filter(tutor__id=tutor_id)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    except Assignment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def submission_list(request):
    if request.method == 'GET':
        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def submission_detail(request, pk):
    try:
        submission = Submission.objects.get(pk=pk)
    except Submission.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubmissionSerializer(submission)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SubmissionSerializer(submission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        submission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def submission_by_student(request, student_id):
    try:
        submissions = Submission.objects.filter(student__id=student_id)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    except Submission.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def submission_by_assignment(request, assignment_id):
    try:
        submissions = Submission.objects.filter(assignment__id=assignment_id)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)
    except Submission.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET', 'POST'])
def grade_list(request):
    if request.method == 'GET':
        grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def grade_detail(request, pk):
    try:
        grade = Grade.objects.get(pk=pk)
    except Grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GradeSerializer(grade)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GradeSerializer(grade, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        grade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

@api_view(['GET'])
def grade_by_student_assignment(request, student_id, assignment_id):
    try:
        grade = Grade.objects.filter(student__id=student_id,assignment__id=assignment_id)
        serializer = GradeSerializer(grade, many=True)
        return Response(serializer.data)
    except grade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def interactions_list(request):
    if request.method == 'GET':
        interactions = InteractionHistory.objects.all()
        serializer = InteractionHistorySerializer(interactions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InteractionHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def interactions_detail(request, pk):
    try:
        interactions = InteractionHistory.objects.get(pk=pk)
    except InteractionHistory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InteractionHistorySerializer(interactions)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InteractionHistorySerializer(interactions, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        interactions.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET', 'POST'])
def readingState_list(request):
    if request.method == 'GET':
        readingStates = ReadingState.objects.all()
        serializer = ReadingStateSerializer(readingStates, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReadingStateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def readingState_detail(request, pk):
    try:
        readingState = ReadingState.objects.get(pk=pk)
    except ReadingState.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReadingStateSerializer(readingState)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReadingStateSerializer(readingState, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        readingState.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def voicecall(request):
    return render(request,'voicecalls.html')



def home(request):
 return render(request, 'f.html')









from spyne import Application, rpc, ServiceBase, Unicode, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.server.django import DjangoApplication

from .models import Grade, User, Assignment
from typing import Dict,Any


class GradeService(ServiceBase):
    @rpc(Integer, Integer,_returns=Integer)
    def get_grade_by_id(self,  student_id,assignment_id):
        try:
            grade_instance = Grade.objects.filter(student_id=student_id, assignment_id=assignment_id)

            return  f"Grade: {grade_instance.grade}, Feedback: {grade_instance.feedback}"
        except Exception as e:
               raise ValueError(f"Error processing data: {e.args[0]}") 
    # @rpc(Integer, _returns=List[Integer])
    # def get_grades_by_student(self,  student_id):
    #     grades = Grade.objects.filter(student_id=student_id)
    #     return [
    #         {
    #             "id": grade.pk,
    #             "assignment": {
    #                 "id": grade.assignment.id,
    #                 "title": grade.assignment.title,
    #             },
    #             "grade": grade.grade,
    #             "feedback": grade.feedback,
    #         } for grade in grades
    #     ]



spyne_app = Application(
    [GradeService],
    tns='http://grade.tn',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

Django_app = DjangoApplication(spyne_app)

gradeapi = csrf_exempt(Django_app)