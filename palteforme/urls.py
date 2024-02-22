from rest_framework import routers
from django.urls import include, path
router=routers.DefaultRouter()
from .views import *



# router.register(r'course',course_list)
# router.register(r'enrollment',EnrollmentViewSet)
# router.register(r'assignment',AssignmentViewSet)
# router.register(r'submission',SubmissionViewSet)
# router.register(r'grade',GradeViewSet)
# router.register(r'interactionhistory',InteractionHistoryViewSet)
# router.register(r'readingstate',ReadingStateViewSet)


urlpatterns=[
    path('courses/', course_list),
    path('courses/<int:pk>/', course_detail),
    path('tutor-courses/<int:tutor_id>/', courses_by_tutor),
    path('home/', home, name='home'),
    path('voicecall/',voicecall),
    path('change_verification_status/', change_verification_status, name='change_verification_status'),
    path('get_verif_status/', get_verif_status),

    path('lesson/<int:pk>/', lesson),
    path('add_lesson/', postlesson),
    path('lessons_by_course/<int:pk>/', lesson_by_course),

    

    path('materials/', material_list),
    path('materials/<int:pk>/', material_detail),
    path('materials/course/<int:lesson_id>/', materials_by_course),

    path('get_pdf/<str:file_name>/', get_pdf),

    path('enrollments/', enrollment_list),
    path('enrollments/<int:pk>/', enrollment_detail),
    path('enrollement-student/<int:student_id>/', enrollement_by_student),

    path('assignments/', assignment_list),
    path('assignments/<int:pk>/', assignment_detail),
    path('tutor-assignment/<int:tutor_id>/', assignment_by_tutor),

    path('submissions/', submission_list),
    path('submissions/<int:pk>/', submission_detail),
    path('submission-student/<int:student_id>/', submission_by_student),
    path('submission-assignment/<int:assignment_id>/', submission_by_assignment),

    path('grades/', grade_list),
    path('grades/<int:pk>/', grade_detail),
    path('grades/<int:student_id>/<int:assignment_id>/', grade_by_student_assignment),

    path('interactionsHistory/', interactions_list),
    path('interactionsHistory/<int:pk>/', interactions_detail),

    path('readingState/', readingState_list),
    path('readingState/<int:pk>/', readingState_detail),
]

# urlpatterns = [
#     path('', include(router.urls)),
#     # Include a specific URL pattern for accessing an instance by ID
#     path('course/<int:pk>/', CourseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='course-detail'),
#     path('enrollment/<int:pk>/', EnrollmentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='enrollment-detail'),
#     # Repeat the pattern for other models as needed
# ]









