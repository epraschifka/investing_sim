from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView, name="login"),
    path('dashboard/', views.DashboardView, name="dashboard"),
    path('register/', views.RegisterView, name="register"),
    path('logout/', views.LogoutView, name="logout"),
    path('stock/<str:pk>', views.StockView, name= "stock"),
]