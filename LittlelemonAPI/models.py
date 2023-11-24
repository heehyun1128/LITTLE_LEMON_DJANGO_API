from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    slug=models.SlugField()
    title=models.CharField(max_length=255,db_index=True)

class MenuItem(models.Model):
    title=models.CharField(max_length=255,db_index=True)
    price=models.DecimalField(max_digits=6,decimal_places=2,db_index=True)
    featured=models.BooleanField(db_index=True)
    category=models.ForeignKey(Category,related_name='menu_items', on_delete=models.PROTECT) #Use PROTECT to prevent the deletion of a referenced object if there are still objects that depend on it

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) #Use CASCADE when you want the deletion of a referenced object to automatically trigger the deletion of all dependent objects. 
    menuitem=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity=models.SmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)
    price=models.DecimalField(max_digits=6,decimal_places=2)

    class Meta:
        unique_together=('menuitem','user')
        
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    # if the referenced user is deleted, the delivery_crew field in the corresponding model instance will be set to NULL
    delivery_crew=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='delivery_crew',null=True,limit_choices_to={'groups__name': "delivery_crew"})
    status=models.BooleanField(db_index=True,default=0)
    total=models.DecimalField(max_digits=6,decimal_places=2)
    date=models.DateField(db_index=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)

    class Meta():
        unique_together = ('order','menuitem')