from django.shortcuts import render
from django.http import HttpResponse
import time, random
from datetime import datetime, timedelta

# Create your views here.

item_prices = {
    "Plain Pizza": 12.99,
    "Baked Ziti": 13.99,
    "Mom's Lasagna": 14.99,
    "Eggplant Parmesan": 13.99,
}

daily_special_items = [
    {"name": "Cheese Calzone", "price": 15.99},
    {"name": "Pepperoni Pizza", "price": 16.99},
    {"name": "Veggie Pizza", "price": 14.99},
    {"name": "Spaghetti and Meatballs", "price": 13.99},
    {"name": "Chicken Alfredo", "price": 14.99},
]

def home(request):
    template_name =  "restaurant/main.html"
    return render(request, template_name)

def main(request):
    template_name = "restaurant/main.html"
    return render(request, template_name)

def order(request):
    template_name = "restaurant/order.html"
    
    context = {
        "special_item": random.choice(daily_special_items)
    }

    return render(request, template_name, context)

def confirmation(request):
    template_name = "restaurant/confirmation.html"

    if request.POST:
        items = request.POST.getlist("items") 
        special_item = request.POST.get("special")
        toppings = request.POST.getlist("toppings")

        special_instructions = request.POST.get("instructions", "")
        name = request.POST.get("name", "")
        number = request.POST.get("number", "")
        email = request.POST.get("email", "")

        order_time = datetime.now()
        preparation_time = random.randint(30, 61)
        ready_time = (order_time + timedelta(minutes=preparation_time)).strftime("%a %b %d %H:%M:%S %Y.")
        total = 0.00

        for item in items:
            total += item_prices.get(item, 0)

        for topping in toppings:
            total += 1.00

        for item in daily_special_items:
            if item["name"] == special_item:
                total += item["price"]


        context = {
            "items": items,
            "toppings": toppings,
            "special_instructions": special_instructions,
            "name": name,
            "number": number,
            "email": email,
            "ready_time": ready_time,
            "total": total
        }

    return render(request, template_name, context)