from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,logout,authenticate
from .forms import CustomUserCreationForm, StockForm

# Create your views here.
def LoginView(request):
    if request.method == "GET":
        return render(request, 'myapp/login.html', {"form" : AuthenticationForm()})
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect("dashboard")
        else:
            return render(request, 'myapp/login.html', {"form" : form})

def LogoutView(request):
    if request.method == "GET":
        logout(request)
        return redirect("login")

def DashboardView(request):
    if request.method == "GET":
        return render(request, 'myapp/dashboard.html')

def RegisterView(request):
    if request.method == "GET":
        return render(request, 'myapp/register.html', {"form" : CustomUserCreationForm()})
    else:
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')

        else:
            return render(request,'myapp/register.html',{"form":form})
        
def StockView(request,pk):
    money = request.user.money
    if request.method == "GET":
        return render(request,"myapp/stock.html",{"ticker":pk, "form":StockForm(),"money":money})
    else:
        form = StockForm(data=request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            order_type = form.cleaned_data.get('order_type')
            print(f"ticker: {pk}")
            print(f"quantity: {quantity}")
            print(f"order_type: {order_type}")
            return render(request,"myapp/stock.html",{"ticker":pk, "form":StockForm(), "money":money})