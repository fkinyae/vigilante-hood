from django.shortcuts import render,redirect
from .forms import UserSignUpForm,UserUpdateForm,ProfileUpdateForm, NeighbourHoodForm, BusinessForm, PostForm
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_text,force_bytes,DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse,reverse_lazy
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from  django.http import HttpResponse,Http404
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from hood import forms
from .models import Business, NeighbourHood, Posts




# Create your views here.
@login_required(login_url='/registration/login/')
def welcome(request):
    hoods = NeighbourHood.objects.all()
    context = {
        "hoods" : hoods,
    }
    return render(request, "index.html", context)

#Usersignup view
def usersignup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link=reverse('activate',kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(user)})
            activate_url='http://'+domain+link
            
            email_body='Hi ' +user.username+ ' Please use this link to verify your account\n' +activate_url
            
            email_subject = 'Activate Your Account'
            
            to_email = form.cleaned_data.get('email')
            
            email = EmailMessage(email_subject, email_body, 'francis.kinyae@student.moringaschool.com',[to_email])
            
            email.send()
            
            return HttpResponse('We have sent you an email, please confirm & activate your email address to complete registration')
    else:
        
        form = UserSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        #return HttpResponse('Your account has been activate successfully')
        return render(request, "email/successful.html")

        
    else:
        return HttpResponse('Activation link is invalid!')
        #return render(request, "email/invalid.html")
    
    
    

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        
        user = authenticate(request, password=password, username=username)
        if user is None:
            context = {"error": "Invalid username or password"}
            return render(request, "registration/login.html",context)
        login(request,user)
    return render(request, "registration/login.html")

class    PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')
    
def view_profile(request):
    context = {
        'user':request.user
    }    
    return render (request, "registration/profile.html", context)    


def edit_profile(request):
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST, instance=request.user)
        profile_form=ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form=UserUpdateForm(instance=request.user)   
        profile_form=ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form":user_form,
        "profile_form":profile_form,
        
    }
    return render (request, "registration/edit_profile.html",context)  


def hood_view(request):
    if request.method == "POST":
        form = NeighbourHoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = request.user.profile
            hood.save()
            return redirect('welcome')
    else:
            form = NeighbourHoodForm( instance = request.user.profile)
        
    context = {
            "form":form
        }    
    return render(request,"hood.html",context)

def each_hood(request, id):
    hood = NeighbourHood.objects.get(id=id)
    
    if request.method == "POST":
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save( commit=False)
            business.owner = request.user.profile
            business.hood =  hood
            business.save()
            return redirect('all_businesses', hood.id)
    else:
        form = BusinessForm(instance=request.user)    
    context = {
        "form" : form,
    }    
    return render(request, "business.html", context)

def all_businesses(request, id):
    
    businesses = Business.objects.filter(hood=id)
    hood = NeighbourHood.objects.get(id=id)

    
    context = {
        "businesses" : businesses,
        "hood" : hood
    }    
    return render(request, "all_businesses.html", context)



def write_post(request, id):
    
    hood = NeighbourHood.objects.get(id=id)
    
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post=form.save( commit=False)
            post.owner=request.user.profile
            post.hood=hood
            post.save()
            return redirect('all_posts', hood.id)
    else:
        form = PostForm(instance=request.user.profile)
    context = {
        "form" : form
    }        
    return render(request, "post.html", context)

def all_posts(request, id):
    
    hood = NeighbourHood.objects.get(id=id)
    posts = Posts.objects.filter(hood=id)
    
    context = {
        "posts" : posts,
        "hood" : hood
    }
    
    return render(request, "all_posts.html", context)

def search_hoods(request):
    
    hoods = NeighbourHood.objects.all()

    
    if 'hood' in request.GET and request.GET["hood"]:
        search_term = request.GET.get("hood")
        searched_hoods = NeighbourHood.find_neighborhood(search_term)
        message = f"{search_term}"
        
        return render(request, 'searched_hood.html', {"message":message, "searched_hoods":searched_hoods, "hoods":hoods})
    
    else:
        message ="You haven't searched for any term"
        return render(request, 'searched_hood.html',{"message":message})
        



    





            
       

    
    


