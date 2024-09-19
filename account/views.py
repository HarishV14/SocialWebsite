from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
            username=cd['username'],
            password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

from .models import Profile

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            # method does not save the instance to the database immediately when commi=False
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            #When users register on your site, you will create an empty profile associated 
            Profile.objects.create(user=new_user)
            return render(request,'account/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})

from django.contrib.auth.decorators import login_required

from django.contrib import messages


@login_required
def edit(request):
    if request.method == 'POST':
        '''instance-This means that when the form is rendered, it will be 
                    pre-populated with the user's current information, allowing them 
                    to see and edit their existing data.
           request.POST is a dictionary-like object containing all the form data submitted 
                        via an HTTP POST request
        '''
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # this used when u submit this will redirect

            messages.success(request, "Profile updated " "successfully")
            # return render(request,'account/dashboard.html')
        else:
            messages.error(request, 'Error updating your profile')
        # return render(request,'account/dashboard.html')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html',{'user_form': user_form,'profile_form': profile_form})


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


# this for the redirecting url there select when changes form submit and comes to this and give that selcet value
# in the redirect url
from django.shortcuts import redirect

def redirect_view(request):
    redirect_url = request.GET.get("redirect")
    if redirect_url:
        return redirect(redirect_url)
    return redirect("default")