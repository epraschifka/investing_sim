from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, OrderForm
from .models import CustomUser, Coin, Holding
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal

# Create your views here.
def LoginView(request):
    if request.method == "GET":
        return render(request, "myapp/login.html", {"form":AuthenticationForm()})
    
    else:
        form = AuthenticationForm(data=request.POST)   

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect("dashboard")
            
        return render(request, "myapp/login.html", {"form":form})

def RegisterView(request):
    if request.method == "GET":
        return render(request, "myapp/register.html",{"form":CustomUserCreationForm()})
    
    else:
        form = CustomUserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('dashboard')

    return render(request, "myapp/register.html", {"form":form})

def DashboardView(request):
    coins = Coin.objects.all()
    if request.method == "GET":
        return render(request, "myapp/dashboard.html", {"coins":coins})

def LogoutView(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    
def DataView(request,pk=""):
    if request.method == "GET":
        if (pk is not None):
            data = list(Coin.objects.filter(Q(symbol__contains = pk) | Q(name__contains = pk)).values())
        else:
            data = Coin.objects.all()
        return JsonResponse({"data":data})

def CoinView(request,pk):
    # coin represents current coin
    coin = Coin.objects.get(symbol=pk)

    # number owned is the number of this coin the user owns
    try:
        user_holding = Holding.objects.get(owner=request.user,coin=coin) 
        number_owned = user_holding.quantity
    except Holding.DoesNotExist:
        number_owned = 0


    if request.method == "GET":
        return render(request,"myapp/coin.html",{"coin":Coin.objects.get(symbol=pk),"form":OrderForm(), "number_owned":number_owned})
    
    if request.method == "POST":
        form = OrderForm(data=request.POST)
        if form.is_valid():
            price = float(request.POST.get("price"))
            quantity = float(request.POST.get("quantity"))
            cost = price * quantity
            if (cost <= request.user.money):
                request.user.money -= Decimal(cost)
                request.user.save()

                current_coin = Coin.objects.get(symbol=pk)

                # check if the user already owns any of this coin
                # if they do, store the holding in a variable
                # "existing holding"
                try:
                    existing_holding = Holding.objects.get(owner=request.user,coin=current_coin)
                    existing_holding.quantity += quantity
                    existing_holding.save()
                except Holding.DoesNotExist:
                    Holding.objects.create(coin=coin,owner=request.user,quantity=quantity)
                messages.success(request, f"Successfully purchased ${quantity} {pk} for ${cost}")
                return redirect("dashboard")
            else:
                messages.error(request,"Order unsucesssful: insufficient funds.")
                return render(request,"myapp/coin.html",{"coin":Coin.objects.get(symbol=pk),"form":form,"number_owned":number_owned})
            
            
        else:
            return render(request,"myapp/coin.html",{"coin":Coin.objects.get(symbol=pk),"form":OrderForm(),"number_owned":number_owned})