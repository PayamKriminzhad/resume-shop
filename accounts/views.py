from django.shortcuts import redirect, render
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import EditUserForm, LoginForm, RegisterForm, EditUserForm
from .models import Dashbord



def Login(request):

    if request.user.is_authenticated:
        return redirect('/')
    
    form = LoginForm(request.POST or None)
            
    if form.is_valid():
        username=form.cleaned_data.get('user_name')
        password=form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form.add_error('user_name', 'کاربری با مشخصات وارد شده یافت نشد')

        
    context={
        'form':form,
    }

    return render(request, 'login.html', context)


def Register(request):

    if request.user.is_authenticated:
        return redirect('/')
    
    form = RegisterForm(request.POST or None)

    if form.is_valid():

        username=form.cleaned_data.get('user_name')
        email=form.cleaned_data.get('email')
        password=form.cleaned_data.get('password')

        user = User.objects.create(username=username, email=email, password=password)
        Dashbord.objects.create(owner_id=user.id, u_name=username)

        return redirect('/login')

    
        
    context={
        'form':form,
    }

    return render(request, 'register.html', context)


def Logout(request):
    logout(request)
    return redirect('/login')



@login_required(login_url='/login')
def UserMainPage(request):

    user_id = request.user.id
    user = User.objects.get(id=user_id)
    dashbord = Dashbord.objects.filter(owner_id=user_id).first()

    if user is None:
        raise Http404('کاربر مورد نظر یافت نشد')
    if dashbord is None:
        raise Http404('کاربر مورد نظر یافت نشد')

    context = {
        'dashbord' : dashbord
    }        

    return render(request, 'user_dashbord.html', context)



@login_required(login_url='/login')
def EditUserProfile(request):

    user_id = request.user.id
    user = User.objects.get(id=user_id)
    dashbord = Dashbord.objects.get(owner_id=user_id)

    if user is None:
        raise Http404('کاربر مورد نظر یافت نشد')

    form = EditUserForm(request.POST or None, request=request, initial={'f_name': user.first_name, 'l_name': user.last_name, 'u_name': user.username, 'ph_number': dashbord.ph_number, 'email': user.email})
    
    if form.is_valid():

        fname = form.cleaned_data.get('f_name')
        lname = form.cleaned_data.get('l_name')
        uname = form.cleaned_data.get('u_name')
        phonenum = form.cleaned_data.get('ph_number')
        email = form.cleaned_data.get('email')

        user.first_name = fname
        user.last_name = lname
        user.username = uname
        user.email = email
        user.save()

        dashbord.f_name = fname
        dashbord.l_name = lname
        dashbord.u_name = uname
        dashbord.email = email
        dashbord.ph_number = phonenum
        dashbord.save()

        return redirect('/user')

    context = {
        'form' : form,
    }        

    return render(request, 'user_edit.html', context)
