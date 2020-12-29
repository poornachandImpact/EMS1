"""ems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from  employee import views

urlpatterns = [
    path('', views.user_login, name="login"),
    path('index/', views.index,name='index' ),
    path('employee_list', views.employee_list,name='employee_list' ),
    path('add_emp/', views.add_emp ,name='employee_add'),
    path('<int:id>/employee_edit/', views.employee_edit ,name='employee_edit'),
    path('<int:id>/employee_delete/', views.employee_delete ,name='employee_delete'),
    path('success/',views.success),
    path('logout/',views.user_logout,name = "logout"),
    path('profile/',views.MyProfile.as_view(),name="my_profile"),
    path('profile/update/',views.ProfileUpdate.as_view(),name="update_profile")
]


'''
Adding Polls from super admin
'''