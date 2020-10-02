from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import sys
from subprocess import run,PIPE
from .models import card
from .main_ import test
from card_OCR.settings import MEDIA_ROOT,MEDIA_URL

def index(request):
    return render(request,'home.html')
def demo(request):
    image=request.FILES['image']
    fs=FileSystemStorage()
    filename=fs.save(image.name,image)
    fileurl=fs.open(filename)
    templateurl=fs.url(filename)
    url = MEDIA_ROOT+MEDIA_URL+filename
    print(url)
    print("raw url",filename)
    print("file url",fileurl)
    print("template url",templateurl)
    contacts,pincode,email,website,city,state,address,name = test(filename)

    # image= run([sys.executable,'F://Visual Studio Code//djangoproject//main.py',str(fileurl),str(filename)],shell=False,stdout=PIPE)
    # print("final text",image.stdout)
    sep=" "
    def converttostr(input_seq, seperator):
        final_str = seperator.join(input_seq)
        return final_str
    def remove(string):
        return string.replace(" ","")
    name=converttostr(name,sep)
    name=remove(name)
    company_name="xyz"
    email=converttostr(email,sep)
    website=converttostr(website,sep)
    contact1,contact2="",""
    if(len(contacts)):
        contact1=contacts[0]
        if(len(contacts)>1):
            contact2=contacts[1]
    else:
        contact1,contact2=" "," "
    contact1=remove(contact1)
    contact2=remove(contact2)
    city=converttostr(city,sep)
    state=converttostr(state,sep)
    pincode=converttostr(pincode,sep)
    address=converttostr(address,sep)
    address=remove(address)
    print(name,email,website,contact1,contact2,city,state,pincode,address)
    params={"name":name,"companyName":company_name,"email":email,"website":website,"contact1":contact1,"contact2":contact2,"city":city,"state":state,"pincode":pincode,"address":address}
    print(params)
    return render(request,'show.html',params)

def show(request):
    if request.method=="POST":
        name=request.POST.get("name")
        company_name=request.POST.get("cname")
        email=request.POST.get("email")
        website=request.POST.get("website")
        contact1=request.POST.get("contact1")
        contact2=request.POST.get("contact2")
        city=request.POST.get("city")
        state=request.POST.get("state")
        pincode=request.POST.get("pincode")
        address=request.POST.get("address")
        card1=card(name=name,company_name=company_name,email=email,website=website,contact1=contact1,contact2=contact2,city=city,state=state,pincode=pincode,address=address)
        card1.save()
    return render(request,"home.html")
