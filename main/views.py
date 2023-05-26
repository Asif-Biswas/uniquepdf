from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
import random
# import ;ogin required
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "home.html")

def pdf(request):
    if request.user.is_anonymous:
        messages.error(request, "Please login to Download PDF")
        return render(request, "login.html")
    try:
        profile = Profile.objects.get(username=request.user.username)
    except:
        messages.error(request, "Please update your profile to Download PDF")
        return render(request, "home.html")
    graduation_year_last_2_digits = str(profile.graduationyear)[-2:]
    len_of_total_profile = Profile.objects.all().count()
    len_of_total_profile = str(len_of_total_profile)
    len_of_total_profile = len_of_total_profile.zfill(5)
    certificate_id = graduation_year_last_2_digits + len_of_total_profile
    return render(request, "pdf.html", {"profile": profile, "certificate_id": certificate_id})


def tpdf(request):
    if request.user.is_anonymous:
        messages.error(request, "Please login to Download PDF")
        return render(request, "login.html")
    try:
        profile = Profile.objects.get(username=request.user.username)
    except:
        messages.error(request, "Please update your profile to Download PDF")
        return render(request, "home.html")
    graduation_year_last_2_digits = str(profile.graduationyear)[-2:]
    len_of_total_profile = Profile.objects.all().count()
    len_of_total_profile = str(len_of_total_profile)
    len_of_total_profile = len_of_total_profile.zfill(5)
    certificate_id = graduation_year_last_2_digits + len_of_total_profile
    return render(request, "tpdf.html", {"profile": profile, "certificate_id": certificate_id})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("profile")
        else:
            # No backend authenticated the credentials
            messages.error(request, "Invalid Credentials")
            return render(request, "login.html")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        graduationyear = request.POST.get("graduationyear")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")
        print(firstname, lastname, username, email, contact, address, graduationyear, password, confirmpassword)
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "register.html")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "register.html")
        if len(password) < 8:
            messages.error(request, "Password must be atleast 8 characters long")
            return render(request, "register.html")
        if password != confirmpassword:
            messages.error(request, "Passwords do not match")
            return render(request, "register.html")
        
        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        len_of_total_profile = Profile.objects.all().count() + 1
        len_of_total_profile = str(len_of_total_profile)
        len_of_total_profile = len_of_total_profile.zfill(5)
        certificate_id = graduationyear[-2:] + len_of_total_profile
        while Profile.objects.filter(certificate_id=certificate_id).exists():
            len_of_total_profile = int(len_of_total_profile) + 1
            len_of_total_profile = str(len_of_total_profile)
            len_of_total_profile = len_of_total_profile.zfill(5)
            certificate_id = graduationyear[-2:] + len_of_total_profile

        transcript_id = graduationyear[-2:] + str(random.randint(10000, 99999))
        while Profile.objects.filter(transcript_id=transcript_id).exists():
            transcript_id = graduationyear[-2:] + str(random.randint(10000, 99999))


        profile = Profile.objects.create(
            user=user,
            firstname=firstname, 
            lastname=lastname, 
            username=username, 
            email=email, 
            contact=contact, 
            student_id=address, 
            graduationyear=graduationyear,
            certificate_id=certificate_id,
            transcript_id=transcript_id)
        profile.save()
        messages.success(request, "Account created successfully")
        return render(request, "login.html")
        
    return render(request, "register.html")


def verify(request):
    if request.method == "POST":
        certificate_id = request.POST.get("pdf")
        try:
            profile = Profile.objects.get(certificate_id=certificate_id)
        except:
            messages.error(request, "Invalid Certificate ID")
            return render(request, "verify.html")
        return render(request, "pdf.html", {"profile": profile})
    return render(request, "verify.html")


def tverify(request):
    if request.method == "POST":
        certificate_id = request.POST.get("pdf")
        try:
            profile = Profile.objects.get(transcript_id=certificate_id)
        except:
            messages.error(request, "Invalid Transcript ID")
            return render(request, "tverify.html")
        return render(request, "tpdf.html", {"profile": profile})
    return render(request, "tverify.html")

@login_required(login_url="login")
def profile(request):
    profile = Profile.objects.get(username=request.user.username)
    return render(request, "profile.html", {"profile": profile})
