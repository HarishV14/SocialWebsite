from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


'''any requests to /users/follow/ will match the regular expression of
the user_detail pattern and that view will be executed instead. Remember that in
every HTTP request, Django checks the requested URL against each pattern in order
of appearance and stops at the first match.'''
urlpatterns = [
    # this custome login view
    # path('login/',views.user_login,name='login')
    path("", views.dashboard, name="dashboard"),
    path("redirect/", views.redirect_view, name="redirect"),
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
    # users
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),


    
    # this inbuild login view functionalities
    # login and logout
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    # reset password urls
    path(
        "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
