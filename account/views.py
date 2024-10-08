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
from actions.utils import create_action

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
            # When users register on your site, you will create an empty profile associated
            Profile.objects.create(user=new_user)
            create_action(new_user, "has created an account")
            return render(request,'account/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})

from django.contrib.auth.decorators import login_required

from django.contrib import messages

@login_required
def edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        '''instance-This means that when the form is rendered, it will be 
                    pre-populated with the user's current information, allowing them 
                    to see and edit their existing data.
           request.POST is a dictionary-like object containing all the form data submitted 
                        via an HTTP POST request
        '''
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(
            instance=profile, data=request.POST, files=request.FILES
        )
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
        profile_form = ProfileEditForm(instance=profile)
    return render(request,'account/edit.html',{'user_form': user_form,'profile_form': profile_form})

from actions.models import Action

@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',flat=True)

    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
        actions = actions[:10]
        # select_related() will help you to boost performance for retrieving related objects in one-to-many relationship
        actions = actions.select_related("user", "user__profile").prefetch_related(
            "target"
        )[:10]

    return render(
        request, "account/dashboard.html", {"section": "dashboard", "actions": actions}
    )


# this for the redirecting url there select when changes form submit and comes to this and give that selcet value
# in the redirect url
from django.shortcuts import redirect

def redirect_view(request):
    redirect_url = request.GET.get("redirect")
    if redirect_url:
        return redirect(redirect_url)
    return redirect("default")

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(
        request, "account/user/list.html", {"section": "people", "users": users}
    )


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request, "account/user/detail.html", {"section": "people", "user": user}
    )


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    print("hi")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
                create_action(request.user, "is following", user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})
