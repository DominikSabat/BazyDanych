from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(primary_key=True,unique=True)
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.email

class Product(models.Model):
    product_ID = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    price = models.FloatField()
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    category = models.CharField(max_length=50)
    rating_mean = models.FloatField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.product_name

class Wishlist(models.Model):
    wishlist_ID = models.AutoField(primary_key=True)
    email = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_ID = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.email)+" Wishlist"

class ProductReview(models.Model):
    email = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_ID = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField()

    def __str__(self):
        return str(self.email)+" Reviews"

class SalesOrder(models.Model):
    sale_order_id = models.AutoField(primary_key=True)
    order_date = models.DateField(auto_now_add=True)
    order_status = models.CharField(max_length=20)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    address = models.CharField(max_length=200)
    email = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.email) + " Sales Order: "+str(self.sale_order_id)

class SalesOrderLine(models.Model):
    sale_order_line_no = models.AutoField(primary_key=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    product_ID = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale_order_id = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.sale_order_line_no)+" line of " + str(self.sale_order_id)