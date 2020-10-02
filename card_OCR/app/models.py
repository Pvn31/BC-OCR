from django.db import models

# Create your models here.
class card(models.Model):
    c_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,blank=True)
    company_name=models.CharField(max_length=100,blank=True)
    email=models.CharField(max_length=50,blank=True)
    website=models.CharField(max_length=50,blank=True)
    contact1=models.CharField(max_length=15,blank=True)
    contact2=models.CharField(max_length=15,blank=True)
    city=models.CharField(max_length=15,blank=True)
    state=models.CharField(max_length=15)
    pincode=models.CharField(max_length=15,blank=True)
    address=models.CharField(max_length=250,blank=True)

    def str(self):
        return self.c_id