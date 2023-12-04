from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, OrderForm
from .models import CustomUser, Coin, Holding
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal
import json
from datetime import datetime

# Create your views here.
def handler404(request):
    if request.user.is_authenticated:
        return render(request, 'myapp/authenticated404.html', status=404)

    return render(request, 'myapp/unauthenticated404.html', status=404)

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
            user = form.save(commit=False)
            user.portfolio_value = user.money
            user.portfolio_graph = json.dumps({"date": [str(datetime.now())], "value": [float(user.money)]})
            user.save()
            login(request,user)
            return redirect('dashboard')

    return render(request, "myapp/register.html", {"form":form})

def DashboardView(request):
    if not request.user.is_authenticated:
        messages.error(request,"You do not have permission to access this page.")
        return redirect('login')
    coins = Coin.objects.all()
    holdings = Holding.objects.filter(owner=request.user)
        
    # we want a pie chart where each section represents one coin.
    # However, one user can have many holdings of the same coin.
    # To do this, we follow the below steps.
    # repeat steps 1-4 for each coin owned by the user:
    # 1. initialize variable coin_cost, coin_value, coin_quantity = 0
    # 2. For each holding of this coin, add its cost to coin_cost,
    # add its value to coin_value, and add holding.quantity to coin_quantity
    # 3. let coin_revenue_percent=(coin_value - coin_cost)/coin_cost
    # 4. push coin_quantity and coin_revenue_percent into an array

    # let our final data array be represented by piechart_data
    piechart_data = {"data":[]}

    # Before we do this, need to find the list of coins owned by user
    coins = set({})
    for holding in holdings:
        coins.add(holding.coin)
    
    # now, we can execute the steps listed above
    for coin in coins:
        coin_holdings = Holding.objects.filter(coin=coin)

        # 1. initialize variable coin_cost, coin_value, coin_quantity = 0
        coin_cost = 0
        coin_value = 0
        coin_quantity = 0

        # 2. For each holding of this coin, add its cost to coin_cost,
        # add its value to coin_value, and add holding.quantity to coin_quantity
        for holding in coin_holdings:
            coin_cost += (holding.quantity * holding.price_bought_at)
            coin_value += (holding.quantity * coin.price)
            coin_quantity += holding.quantity

        # 3. let coin_revenue_percent=(coin_value - coin_cost)/coin_cost
        coin_revenue_percent = round(100*(coin_value - coin_cost)/coin_cost,2)

        # 4. push coin, coin_quantity and coin_revenue_percent into an array
        piechart_data['data'].append({"coin_name":coin.name,"coin_value":float(coin_value), "coin_quantity":float(coin_quantity), "coin_revenue_percent":float(coin_revenue_percent)})
    
    # add user's cash to piechart_data 
    piechart_data['data'].append({"coin_name":"Cash","coin_value":float(request.user.money), "coin_quantity":float(request.user.money), "coin_revenue_percent":float(0)})

    # convert dictionary into json
    piechart_data_json = json.dumps(piechart_data)
    

    if request.method == "GET":
        return render(request, "myapp/dashboard.html", {"coins":coins, "holdings":holdings, "piechart_data":piechart_data_json, "crypto_value":request.user.portfolio_value - request.user.money})

def LogoutView(request):
    if request.method == "POST":
        logout(request)
        messages.success(request,"Successfully logged out.")
        return redirect("login")

def DataView(request,pk=""):
    if request.method == "GET":
        if (pk is not None):
            data = list(Coin.objects.filter(Q(symbol__contains = pk) | Q(name__contains = pk)).values())
        else:
            data = Coin.objects.all()
        return JsonResponse({"data":data})

def CoinView(request,pk):
    if not request.user.is_authenticated:
        messages.error(request,"You do not have permission to access this page.")
        return redirect('login')
    # coin represents current coin
    order_coin = Coin.objects.get(symbol=pk)

    # find any holdings of this coin the current user already has
    holdings = Holding.objects.filter(owner=request.user,coin=order_coin)
    number_owned = 0

    # find total amount of this coin owned by the user
    for holding in holdings:
        number_owned += holding.quantity

    if request.method == "GET":
        return render(request,"myapp/coin.html",{"coin":Coin.objects.get(symbol=pk),"form":OrderForm(), "number_owned":number_owned})
    
    if request.method == "POST":
        form = OrderForm(data=request.POST)
        if form.is_valid():
            order_coin = Coin.objects.get(symbol=pk)
            order_price = order_coin.price
            order_quantity = Decimal(request.POST.get("quantity"))
            order_type = request.POST.get("order-type")

            # case where order type is "buy"
            if order_type == "buy":
                cost = order_price * order_quantity
                if cost <= request.user.money:
                    request.user.money -= cost
                    request.user.portfolio_value += cost
                    request.user.save()

                    # create new holding to represent this purchase
                    Holding.objects.create(coin=order_coin,owner=request.user,quantity=order_quantity, price_bought_at=order_price)
                    messages.success(request, f"Successfully purchased {order_quantity} {pk} for ${round(cost,2)}")
                    return redirect("dashboard")
                else:
                    messages.error(request,"Order unsuccesssful (insufficient funds).")
                    return render(request,"myapp/coin.html",{"coin":Coin.objects.get(symbol=pk),"form":form,"number_owned":number_owned})
                
            if order_type == "sell":
                # case where order type is "sell"
                # check if the user has at least quantity of this coin
                # by iterating through each of their holdings of this coin
                # let remainder denote what is "left over" after
                # subtracting the holding quantity from the order quantity
                total_quantity = 0

                for holding in holdings:
                    total_quantity += holding.quantity
                
                # if the user has less than quantity of this coin,
                # reject the order
                if order_quantity > total_quantity:
                    messages.error(request,"Order unsuccesssful (you don't own enough of this coin).")
                    return render(request,"myapp/coin.html",{"coin":Coin.objects.get(symbol=pk),"form":form,"number_owned":number_owned})
                
                # otherwise, the order is valid.
                # sell off each of the user's holdings until
                # we reach quantity
                order_quantity_copy = order_quantity
                holdings_copy = holdings

                for holding in holdings_copy:
                    remainder = max(0,holding.quantity - order_quantity_copy)
                    order_quantity_copy = max(order_quantity_copy - holding.quantity,0)
                    holding.quantity = remainder

                    # if the holding's quantity is now zero, delete it
                    if holding.quantity == 0:
                        holding.delete()
                    
                    # else, save it
                    if holding.quantity > 0:
                        holding.save()

                    # if quantity is zero, we can stop
                    if order_quantity_copy == 0:
                        break

                profit = Decimal(order_quantity) * Decimal(order_price)
                request.user.money += profit
                request.user.portfolio_value -= profit
                request.user.save()
                messages.success(request,f"Successfully sold {order_quantity} {order_coin.name} for {order_quantity * order_price}.")
                return redirect("dashboard")
            
def BaseView(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return redirect("login")