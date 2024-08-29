from django.db import models
from django.contrib.auth.models import User

import datetime

from django_extensions.management import commands






class Book(models.Model):

  company_name = models.CharField(max_length=255, null=True)
  rating = models.CharField(max_length=255, null=True)
  reviews_count = models.CharField(max_length=255, null=True)
  address = models.CharField(max_length=255, null=True)
  category = models.CharField(max_length=255, null=True)
  phone = models.CharField(max_length=255, null=True)
  website = models.CharField(max_length=555, null=True)
  

  def __str__(self):
      return self.company_name
  




class Project(models.Model):
	name = models.CharField(max_length=200)
	start_date = models.DateField()
	responsible = models.ForeignKey(User, on_delete=models.CASCADE)
	week_number = models.CharField(max_length=2, blank=True)
	end_date = models.DateField()
	def __str__(self):
		return str(self.name)
	
	def save(self, *args, **kwargs):
		print(self.start_date.isocalendar()[1])
		if self.week_number=='':
			self.week_number=self.start_date.isocalendar()[1]

		super().save(*args, **kwargs)


class UploadedCSV(models.Model):
    file = models.FileField(upload_to='csv_files/')

    def __str__(self):
        return self.file.name



# Categories of Products
class Category(models.Model):
	name = models.CharField(max_length=50)


	def __str__(self):
		return self.name

	#@daverobb2011
	class Meta:
		verbose_name_plural = 'categories'


class HtmlContent(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()  # Field to store HTML content
	image1 = models.ImageField(upload_to='uploads/product/', blank=True, null=True, default='')
	category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
	#post_date = models.DateTimeField(default=None, null=True, blank=True)


	def __str__(self):
		return self.title


# Customers
class Customer(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email =models.EmailField(max_length=100, default='', blank=True)
	address = models.CharField(max_length=100, default='', blank=True)
	postcode = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=100, default='', blank=True)
	country =models.CharField(max_length=100, default='',blank=True)
	phone = models.CharField(max_length=100, default='',blank=True)
	#coord = models.CharField(max_length=100, blank=True, default='1')


	def __str__(self):
		return f'{self.first_name} {self.last_name}'
	


class Address(models.Model):
	address = models.CharField(max_length=1000)
	postcode = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	
	def __str__(self):
		return f'{self.address}, {self.postcode}, {self.city}, {self.country}'





# All of our Products
class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
	category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='', blank=True, null=True)
	description = models.CharField(max_length=950, default='', blank=True, null=True)
	services = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='uploads/product/')
	image1 = models.ImageField(upload_to='uploads/product/', blank=True, null=True, default='default_image.jpg')

	# Add Sale Stuff
	is_sale = models.BooleanField(default=False)
	sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=6)

	def __str__(self):
		return self.name


# Custom Products
class CProduct(models.Model):
	name = models.CharField(max_length=50)
	email =models.EmailField(max_length=100, default='', blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
	description = models.CharField(max_length=2000, default='', blank=True, null=True)
	quantity = models.IntegerField(default=1)
	image = models.ImageField(upload_to='uploads/product/')
	image1 = models.ImageField(upload_to='uploads/product/', blank=True, null=True, default='default_image.jpg')

	def __str__(self):
		return self.name




# Customer Orders
class Order(models.Model):
	order_id = models.CharField(max_length=100, primary_key=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	address = models.ForeignKey(Address, on_delete=models.CASCADE)
	email = models.EmailField(max_length=1000)
	delivery_status = models.CharField(max_length=100, default='', blank=True)
	delivery_company = models.CharField(max_length=100, default='', blank=True)
	tracking_id = models.CharField(max_length=100, default='', blank=True)
	date = models.DateField(default=datetime.datetime.today)
	status = models.BooleanField(default=False)
	
	def __str__(self):
		return f'{self.customer} - {self.product} - {self.address}'



# CustomerEnquiry

class Info(models.Model):
	name = models.CharField(max_length=250)
	email = models.EmailField(max_length=500)
	description = models.TextField(max_length=5000)
	items = models.CharField(max_length=2000, null=True, blank=True)

	def __str__(self):
		return self.name