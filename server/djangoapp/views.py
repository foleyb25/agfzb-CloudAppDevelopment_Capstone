from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['password']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # <HINT> Get user information from request.POST
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        # <HINT> username, first_name, last_name, password
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            # <HINT> Login the user and 
            # redirect to course list page
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/3376dfa8-0236-47e0-ad38-431deb75996a/default/get-dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    
def get_dealership_by_state(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/3376dfa8-0236-47e0-ad38-431deb75996a/default/get-dealerships?state=Texas"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    
def get_dealership_by_id(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/3376dfa8-0236-47e0-ad38-431deb75996a/default/get-dealerships?dealerId=15"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)
    
# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = f"https://us-south.functions.appdomain.cloud/api/v1/web/3376dfa8-0236-47e0-ad38-431deb75996a/default/get-reviews?dealerId={dealer_id}"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url)
        # Concat all dealer's short name
        sentiments = ' '.join([review.sentiment for review in reviews])
        # Return a list of dealer short name
        return HttpResponse(sentiments)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    print("IN ADD REVIEW")
    if request.user.is_authenticated:
        # Create review dictionary
        review = {
            "time": datetime.utcnow().isoformat(),
            "name": request.user.username,  # Assuming the User model has a username field
            "dealership": dealer_id,
            "review": request.POST.get('review', ''),  # Assuming the review is sent as a POST field
            "purchase": request.POST.get('purchase', False),  # Example field
            "purchase_date": request.POST.get('purchase_date', ''),
            "car_make": request.POST.get('car_make', ''),
            "car_model": request.POST.get('car_model', ''),
            "car_year": request.POST.get('car_year', ''),

        }

        # Create json_payload to be sent
        json_payload = {
            "review": review
        }

        # Define the URL for posting the review, e.g., your cloud function endpoint
        url = "your cloud function endpoint for posting reviews"

        # Make POST request to the cloud function and get the response
        response = post_request(url, json_payload, dealerId=dealer_id)

        # Return the response as an HttpResponse
        return HttpResponse(response)
    else:
        # If the user is not authenticated, return a message or redirect to login page
        return HttpResponse("User is not authenticated", status=401)


