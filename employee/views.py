from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.hashers import make_password, check_password
from employee.form import UserForm
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ems.decorators import role_required,admin_only
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
# Create your views here.
def index(request):
    print(request.role)
    return render(request,"employee/index.html")
@login_required(login_url="login")
@role_required(allowed_roles=["Admin"])
# @admin_only
def add_emp(request):
    if request.role == "Admin":
        if request.method == 'POST':
             user_form = UserForm(request.POST)
             print(" test make_password",make_password("1234"))
             if user_form.is_valid():
                 u = user_form.save()
                 messages.success(request, "Employee added successfully")
                 return HttpResponseRedirect(reverse('employee_list'))
             else:
                 messages.error(request, "Something went worng!")
                 return HttpResponse("Invalid Form")
        else:
            user_form = UserForm()
            return render(request, "employee/add_emp.html",{"user_form":user_form})
    else:
        return HttpResponseRedirect(reverse('employee_list'))

@login_required(login_url="login")
def employee_list(request):
    # print(request.role)
    users = User.objects.all()
    return render(request, "employee/employees.html", {"users": users})

@login_required(login_url="login")
def employee_edit(request,id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            u=user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/edit.html', {"user_form": user_form})
    else:
        user_form = UserForm(instance=user)
        return render(request, 'employee/edit.html', {"user_form": user_form})
@login_required(login_url="login")
def employee_delete(request,id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        user_form = UserForm(instance=user)
        return render(request, 'employee/delete.html', {"user": user})

def user_login(request):
    # print(request.role)
    if request.method == "POST":
        username  = request.POST["username"]
        password = request.POST["password"]
        user  = authenticate(request,username =username,password=password)
        if user:
            login(request,user)
            return  redirect("index")
        else:
            print("Invalid credentials")
            error = "Provide valid Credentials"
            return render(request,'employee/login.html',{"error":error})
    else:
        return render(request, 'employee/login.html')
@login_required(login_url="login")
def success(request):
    user = request.user
    return render(request, 'employee/success.html',{"user":user})

@login_required(login_url="login")
def user_logout(request):
    if request.method =="POST" or request.method =="GET":
        logout(request)
        return redirect("login")


class ProfileUpdate(UpdateView):
    fields = ['salary','designation']
    template_name = "auth/profile_update.html"
    success_url = reverse_lazy('my_profile')
    def get_object(self):
        return  self.request.user.profile


class MyProfile(DetailView):
    template_name = 'auth/profile.html'
    def get_object(self):
        return  self.request.user.profile