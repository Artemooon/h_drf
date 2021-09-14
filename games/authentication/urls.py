from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name="user_register"),
    path('logout/', views.Logout.as_view(), name="user_logout"),
    path('account-activate/<token>/', views.ActivateAccount.as_view(), name="activate_account")
]
