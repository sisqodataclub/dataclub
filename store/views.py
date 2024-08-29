from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Customer, Order, Address, CProduct, UploadedCSV, Project, HtmlContent, Info
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django import forms
from django.core.exceptions import ObjectDoesNotExist  # Add this line
from .forms import CustomerForm, CProductForm
from cart.cart import Cart
import stripe
import csv

from .forms import ScrapingForm
from .scraper import GoogleMapScraper 
from .utils import data_overview

from django.shortcuts import render, redirect
from .forms import UploadCSVForm
import pandas as pd
import plotly.express as px
from django_plotly_dash import DjangoDash
from dash import html, dcc
app = DjangoDash('app')

from django.core import management

from io import TextIOWrapper
from .forms import UploadCSVForm
from .models import UploadedCSV, Book
from .forms import UploadCSVForm
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine
from django.conf import settings
from django.db import transaction
from django_plotly_dash import DjangoDash
from . import plotly_app

def my_view(request):
    products1 = HtmlContent.objects.all()
    return render(request, 'markdown.html', {'products1': products1})


def dash_dashboard(request):
    return render(request, 'dash_view.html')

def services(request):
    return render(request, 'services.html')



def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            df = pd.read_csv(csv_file)

            # Iterate through DataFrame rows and create Book instances
            for _, row in df.iterrows():
                Book.objects.create(
                    company_name=row['company_name'],
                    rating=row['rating'],
                    reviews_count=row['reviews_count'],
                    address=row['address'],
                    category=row['category'],
                    phone=row['phone'],
                    website=row['website'],
                    coord=row['coord']
                    # Add other fields as needed
                )

            messages.success(request, "Your Password Has Been Updated...")

    else:
        form = UploadCSVForm()


    return render(request, 'upload_csv.html', {'form': form})




def data_overview(data, title):
    overview_analysis = {
        f'{title}': [
            data.shape[1], data.shape[0],
            data.isnull().any(axis=1).sum(),
            data.isnull().any(axis=1).sum() / len(data) * 100,
            data.duplicated().sum(),
            data.duplicated().sum() / len(data) * 100,
            sum((data.dtypes == 'object') & (data.nunique() > 2)),
            sum((data.dtypes == 'object') & (data.nunique() < 3)),
            data.select_dtypes(include=['int64', 'float64']).shape[1]
        ]
    }
    overview_analysis = pd.DataFrame(overview_analysis, index=['Columns', 'Rows', 'Missing_Values', 'Missing_Values %',
                                                               'Duplicates', 'Duplicates %', 'Categorical_variables',
                                                               'Boolean_variables', 'Numerical_variables']).round(2)
    return overview_analysis

def upload_csv1(request):
    csv_file = None
    overview_analysis = None

    if request.method == 'POST' and request.FILES['csvFile']:
        csv_file = request.FILES['csvFile']
        data = pd.read_csv(csv_file)

        # Perform data analysis
        overview_analysis = data_overview(data, title=csv_file.name)

        # Create Dash app
        app = DjangoDash('DataOverview')
        app.layout = html.Div(children=[
            html.H2(children='Data Overview'),
            dcc.Graph(
                id='data-table',
                figure={
                    'data': [
                        dict(
                            type='table',
                            header=dict(values=overview_analysis.columns),
                            cells=dict(values=overview_analysis.transpose().values.tolist())
                        )
                    ],
                    'layout': dict(title='Data Overview')
                }
            )
        ])

        return render(request, 'upload_csv.html', {'csv_file': csv_file, 'app': app})
    else:
        return render(request, 'upload_csv.html', {'csv_file': None, 'app': None})





def gantt_chart(request):
    projects = Project.objects.all()

    # Create a DataFrame for the Gantt chart
    data = {
        "Task": [project.name for project in projects],
        "Start": [project.start_date for project in projects],
        "Finish": [project.end_date for project in projects],
        "Resource": [project.responsible.username for project in projects],
    }

    fig = px.timeline(data, x_start="Start", x_end="Finish", y="Task", color="Resource", labels={"Task": "Project"})

    # Convert the Plotly figure to HTML
    chart_html = fig.to_html(full_html=False)

    return render(request, 'gantt_chart.html', {'chart_html': chart_html})





def upload_and_analyze(request):
    def scatter():
        x1 = [1,2,3,4]
        y1 = [30, 35, 25, 45]

        trace = go.Scatter(
            x=x1,
            y = y1
        )
        layout = dict(
            title='Simple Graph',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis = dict(range=[min(y1), max(y1)])
        )

        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context ={
        'plot1': scatter()
    }

    return render(request, 'upload_and_analyze/upload_and_analyze.html', context)





def scrape_data(request):
    if request.method == 'POST':
        form = ScrapingForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            
            # Configuring the scraper and loading companies from the provided URL
            business_scraper = GoogleMapScraper()
            business_scraper.config_driver()
            business_scraper.load_companies(url)
            
            # Performing infinite scroll for 120 seconds
            #infinite_scroll(business_scraper.driver)
            
            # Getting business info after scrolling
            business_scraper.get_business_info()
            
            # Closing the browser after completing the scraping
            business_scraper.driver.quit()
            
            return render(request, 'success.html')
    else:
        form = ScrapingForm()

    return render(request, 'scrape_data.html', {'form': form})


def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')


def category_summary(request):
	categories = Category.objects.all()
	return render(request, 'cat_blog.html', {"categories":categories})	

def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=foo)
		products = HtmlContent.objects.filter(category=category)
		return render(request, 'cat_list.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')


def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'product':product})

def blog(request,pk):
    blog = HtmlContent.objects.get(id=pk)
    products1 = HtmlContent.objects.all()
    return render(request, 'blogs.html', {'blog':blog, 'products1': products1})

def order(request, pk):
    try:
        order = Order.objects.get(order_id=pk)
        return render(request, 'customer_list.html', {'order': order})
    except ObjectDoesNotExist:
        messages.success(request, "There was an error, or the order does not exist.")
        return redirect('orderh')

def orderh(request):
    orders = Order.objects.all()
    return render(request, 'order.html', {'orders': orders})
    


def home(request):
    products = Product.objects.all()    
    products1 = HtmlContent.objects.all()
    return render(request, 'home.html', {'products': products, 'products1': products1})


def about(request):
	return render(request, 'about.html', {})


def personal(request):
	return render(request, 'personal.html', {})	

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
	return redirect('home')



def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("You Have Registered Successfully!! Welcome!"))
			return redirect('home')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})


# store/views.py
from django.shortcuts import render, redirect
from .forms import CustomerForm

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            # Save the customer instance
            customer = form.save(commit=False)

            # Create a new Address instance
            address = Address.objects.create(
                address=form.cleaned_data['address'],
                postcode=form.cleaned_data['postcode'],
                city=form.cleaned_data['city'],
                country=form.cleaned_data['country']
            )

            # Assign the created address to the customer
            customer.address = address
            customer.save()

            return redirect('create_payment_link')  # Redirect to customer detail page

    else:
        form = CustomerForm()

    return render(request, 'create_customer.html', {'form': form})


# Set your Stripe API key
stripe.api_key = "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" 

def cart_summary1(request):
    # Get the cart
    cart = Cart(request)
    totals1 = cart.cart_total()

    # Store the total in the session as a numerical value
    request.session['totals1'] = totals1

    return totals1

def create_payment_link(request):
    cart = Cart(request)
    total = str(cart.cart_total())
    
    # Get the cart total using the cart_summary1 method
    totals1 = float(request.session.get('totals1', total))  # Default to 0 if 'totals1' is not in the session

    amount = int(totals1 * 100)  # Convert to cents (e.g., $50.00)
    currency = "usd"
    success_url = "http://localhost:8000/success/"  # Update with your success URL
    cancel_url = "http://localhost:8000/cancel/"  # Update with your cancel URL

    try:
        line_items = [{
            'price_data': {
                'currency': currency,
                'unit_amount': amount,
                'product_data': {
                    'name': 'Payment'
                },
            },
            'quantity': 1,
        }]
        payment_link = stripe.checkout.Session.create(
            success_url=success_url,
            cancel_url=cancel_url,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
        )

        # Retrieve the payment link URL
        link_url = payment_link.url

        # Render the template with the payment link
        return redirect(link_url)

    except stripe.error.StripeError as e:
        # Handle any errors that occur during payment link creation
        print(f"Error creating payment link: {e}")
        return render(request, 'payment_error.html')
	

def create_cproduct(request):
    if request.method == 'POST':
        form = CProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the list view
    else:
        form = CProductForm()
    return render(request, 'personal.html', {'form': form})

from .forms import CustomerEnquiry


def enquiry(request):
    if request.method == 'POST':
        form = CustomerEnquiry(request.POST)
        if form.is_valid():
            cart = Cart(request)
            items = str(cart.get_prods())  # Get the items from the cart

            # Create an instance of the Info model but don't save it to the database yet
            enquiry_instance = form.save(commit=False)
            
            # Assign the items to the items field
            enquiry_instance.items = items
            
            # Now save the instance to the database
            enquiry_instance.save()

            return redirect('home')  # Redirect to the home page or any other view you prefer
    else:
        form = CustomerEnquiry()
    
    return render(request, 'customerenquiry.html', {'form': form})




