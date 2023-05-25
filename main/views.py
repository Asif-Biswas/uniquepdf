from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile


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

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return render(request, "home.html")
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
        profile = Profile.objects.create(
            user=user,
            firstname=firstname, 
            lastname=lastname, 
            username=username, 
            email=email, 
            contact=contact, 
            address=address, 
            graduationyear=graduationyear)
        profile.save()
        messages.success(request, "Account created successfully")
        return render(request, "login.html")
        
    return render(request, "register.html")