from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from calories.models import Data, User
import requests
from django.http import JsonResponse
import json
from datetime import date
import json

# Create your views here.
def index(request):
    return render(request, "calories/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        remember_me = request.POST.get('checkout', False)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(1209600)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "calories/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "calories/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        print("going to login")
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return render(request, "calories/register.html", {
                "message": "Username already taken."
            })
        elif User.objects.filter(email=email).exists():
            return render(request, "calories/register.html", {
                "message": "Email already taken."
            })
        elif password != confirmation:
            return render(request, "calories/register.html", {
                "message": "Passwords must match."
            })
        elif password == '' or email == '' or username == '':
            return render(request, "calories/register.html", {
                "message": "Please enter all the fields."
            })
            
        user = User.objects.create_user(username, email, password)
        user.save()
        print("going to login")
        login(request, user)
        return HttpResponseRedirect(reverse("login"))
      
        
    return render(request, "calories/register_view.html")

def search(request):
    food = request.GET.get('q')
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    query = food
    print(food)
    response = requests.get(api_url + query, headers={'X-Api-Key': 'wKPy39tHMHLJ1yAErTtEwg==uT9FqsuxmC92i6gX'})
    if response.status_code == requests.codes.ok:
        print(response.text)
        data = json.loads(response.text)
        return JsonResponse(data, safe=False)
    else:
        print("Error:", response.status_code, response.text)
        
def today(request):
    return render(request, "calories/today.html")

def save(request):
    t_quantity = request.GET.get('t_quantity')
    t_calories = request.GET.get('t_calories')
    t_protein = request.GET.get('t_protein')
    t_carbs = request.GET.get('t_carbs')
    t_cholesterol = request.GET.get('t_cholesterol')
    t_fat_saturated = request.GET.get('t_fat_saturated')
    t_fat = request.GET.get('t_fat')
    t_fiber = request.GET.get('t_fiber')
    t_sugar = request.GET.get('t_sugar')
    t_sodium = request.GET.get('t_sodium')
    t_potassium = request.GET.get('t_potassium')
    
    # Perform any necessary operations with the extracted data
    dates = date.today().strftime('%Y-%m-%d')
    try:
        if(Data.objects.filter(user=request.user, date=dates).exists()):
            data = Data.objects.get(user=request.user, date=dates)
            data.t_quantity += float(t_quantity)
            data.t_calories += float(t_calories)
            data.t_protein += float(t_protein)
            data.t_carbs += float(t_carbs)
            data.t_cholesterol += float(t_cholesterol)
            data.t_fat_saturated += float(t_fat_saturated)
            data.t_fat += float(t_fat)
            data.t_fiber += float(t_fiber)
            data.t_sugar += float(t_sugar)
            data.t_sodium += float(t_sodium)
            data.t_potassium += float(t_potassium)
            data.save()
        else:
            data = Data(user=request.user, t_quantity=t_quantity, t_calories=t_calories, t_protein=t_protein, t_carbs=t_carbs, t_cholesterol=t_cholesterol, t_fat_saturated=t_fat_saturated, t_fat=t_fat, t_fiber=t_fiber, t_sugar=t_sugar, t_sodium=t_sodium, t_potassium=t_potassium)
            data.save()
        return JsonResponse({"response": "true"})
    
    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({"response": "false"})
    
    

def records(request):
    calories = []
    dates = []
    protein = []
    carbohydrates = []
    sugar = []
    fiber = []
    fat = []
    food = Data.objects.filter(user=request.user)
    print(food)
    for i in food:
        calories.append(i.t_calories)
        dates.append(i.date.strftime('%m-%d'))
        protein.append(i.t_protein)
        carbohydrates.append(i.t_carbs)
        sugar.append(i.t_sugar)
        fiber.append(i.t_fiber)
        fat.append(i.t_fat)
    
    calories_json = json.dumps(calories)
    dates_json = json.dumps(dates)
    protein_json = json.dumps(protein)
    carbohydrates_json = json.dumps(carbohydrates)
    sugar_json = json.dumps(sugar)
    fiber_json = json.dumps(fiber)
    fat_json = json.dumps(fat)
    
    print(calories_json, dates_json, protein_json, carbohydrates_json, sugar_json, fiber_json, fat_json)
    return render(request, "calories/record.html", {
        "calories_json": calories_json,
        "dates_json": dates_json,
        "protein_json": protein_json,
        "carbohydrates_json": carbohydrates_json,
        "sugar_json": sugar_json,
        "fiber_json": fiber_json,
        "fat_json": fat_json,
    })
    
def set(request):
    height = request.POST.get('height')
    weight = request.POST.get('weight')
    age = request.POST.get('age')
    sex = request.POST.get('sex')
    
    user = User.objects.get(username=request.user)
    user.height = height
    user.weight = weight
    user.age = age
    user.sex = sex
    user.set = True
    user.save()
    
    return HttpResponseRedirect(reverse("index"))

def recomendations(request):
    user = User.objects.get(username=request.user)
    h = user.height
    w = user.weight
    a = user.age
    s = user.sex
    if s == 'M':
        bmr = 66.5 + 13.8*w + 5.0*h - 6.8*a
        pmin = w*0.8
        pmax = w*1
        fat = bmr*0.3/9
    else:
        bmr = 655.1 + 9.6*w + 1.9*h - 4.7*a
        pmin = w*0.8
        pmax = w*1
        fat = bmr*0.3/9
        
    data = [bmr, pmin, pmax, fat]
    data_json = json.dumps(data)
    return JsonResponse(data_json, safe=False)


def bmi(request):
       
    return render(request, "calories/bmi.html")


def bmi_get(request):
     if request.method == "GET":
        height = request.GET.get('height')
        weight = request.GET.get('weight')
        age = request.GET.get('age')
        url = "https://fitness-calculator.p.rapidapi.com/dailycalorie"

        url = "https://fitness-calculator.p.rapidapi.com/bmi"

        querystring = {"age":age,"weight":weight,"height":height}

        headers = {
            "X-RapidAPI-Key": "ccf7ae98d4mshcdfe4935c380587p13792ejsn15f2cdbd69bb",
            "X-RapidAPI-Host": "fitness-calculator.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        
        return JsonResponse(response.json(), safe=False)