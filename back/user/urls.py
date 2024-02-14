from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from user import views
from rest_framework import routers
from .views import *
router=routers.DefaultRouter()



urlpatterns =[
     path('profile/',views.ProfileView.as_view()),
     path('api/auth/', views.CustomAuthToken.as_view()),
     path('api/signup/', views.signup), 
     path('api/profile/<int:pk>/',user_profile), 



    # path('signup/', views.signup),
    # path('api/auth/', views.CustomAuthToken.as_view()),   
]

urlpatterns = format_suffix_patterns(urlpatterns)

