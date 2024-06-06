from django.db import models

# Create your models here.
class Feedback(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    message=models.CharField(max_length=100)
    class Meta:
        db_table="feedback"
class Cust(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    email=models.EmailField()
    phone=models.CharField(max_length=20)
    message=models.CharField(max_length=100)
    cimage=models.ImageField(null=True,blank=True,upload_to="images/")
    class Meta:
        db_table="cust"
class painting(models.Model):
    img=models.ImageField(upload_to='paintings/')
    name=models.CharField(max_length=20)
    price=models.CharField(max_length=20)
    medium=models.CharField(max_length=20)
    rating=models.CharField(max_length=20)
    noofpeoplerated=models.CharField(max_length=20,default='0')
    class Meta:
        db_table="painting"
class cartforuser(models.Model):
    username=models.CharField(max_length=20)
    cartcontent=models.CharField(max_length=400)
    class Meta:
        db_table="cartforuser"
class Order(models.Model):
    username=models.CharField(max_length=20)
    name=models.CharField(max_length=20)
    details=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    address=models.CharField(max_length=100)
    total=models.CharField(max_length=10)
    class Meta:
        db_table="orders"