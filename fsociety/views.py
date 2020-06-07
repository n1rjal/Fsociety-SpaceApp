from django.shortcuts import render,Http404
from django.http import JsonResponse
import pickle
import numpy as np
from .models import Crops
from django.contrib.auth import authenticate

clf_prec=pickle.load(open("precmodel_prec.sav","rb"))
clf_temp=pickle.load(open("precmodel_temp.sav","rb"))
def forecast_temp(date):
    year,month,day=date.split("-")
    sum=[]
    summ=0
    unit="C"
    for day in range(1,31):
        predicted_data=clf_temp.predict(np.array([(year,month,day)]))
        a=int(predicted_data)
        sum.append(abs(a))
        
    for s in sum:
        summ+=s
        
    summ=summ/30

    summ=abs(round(summ,2))
    msg=str(abs(round(summ,2)))+unit
    return([summ,msg])

def forecast_prec(date):
    year,month,day=date.split("-")
    unit="mm month-1"
    sum=0
    for day in range(1,31):
        predicted_data=clf_prec.predict(np.array([(year,month,day)]))
        a=int(predicted_data)
        sum+=a

    sum=abs(sum)
    sum=abs(round(sum,2))
    msg=""+str(sum)+unit
    return ([sum,msg])


# Create your views here.
def home(request):
    return render(request,'fsociety/index.html')

def reqitem(request):
    if request.method=='GET':
        vardict=request.GET
        year=request.GET['date-to-predict']
        totalprec,msgprec=forecast_prec(year)
        totaltemp,msgtemp=forecast_temp(year)
        
        allcropsgt=Crops.objects.filter(maxtemp__gte=totaltemp)
        allcropslt=Crops.objects.filter(mintemp__lte=totaltemp)
        crops1=allcropslt.intersection(allcropsgt)

        allcropsgt=Crops.objects.filter(maxppt__gte=totalprec)
        print(allcropsgt)
        allcropslt=Crops.objects.filter(minppt__lte=totalprec)

        
        crops2=allcropslt.intersection(allcropsgt)
        crops=crops2.intersection(crops1)

        print(crops)
        output=[]
        for crop in crops:
            output.append(crop.json())
        
        context={
            "predictedtempnumber":totaltemp,
            "predictedprenumber":totalprec,
            "predictedtempmsg":msgtemp,
            "predictedprepmsg":msgprec,
            "name":vardict['name'],
            "place":vardict['place'],
            "date":year,
            "cropsinfo":output,
        }
        
        return render(request,'fsociety/process.html',context)

def apireqitem(request):
    if request.method=='GET':
        username=request.GET.get('username')
        password=request.GET.get('password')
        print(username,password)
        sampleuser=authenticate(username=username,password=password)
        print(sampleuser)
        if sampleuser is None:
            return JsonResponse({"Error":"Error Occured"})
        vardict=request.GET
        year=request.GET['date-to-predict']
        totalprec,msgprec=forecast_prec(year)
        totaltemp,msgtemp=forecast_temp(year)
        
        allcropsgt=Crops.objects.filter(maxtemp__gte=totaltemp)
        allcropslt=Crops.objects.filter(mintemp__lte=totaltemp)
        crops1=allcropslt.intersection(allcropsgt)

        allcropsgt=Crops.objects.filter(maxppt__gte=totalprec)
        print(allcropsgt)
        allcropslt=Crops.objects.filter(minppt__lte=totalprec)

        
        crops2=allcropslt.intersection(allcropsgt)
        crops=crops2.intersection(crops1)

        print(crops)
        output=[]
        for crop in crops:
            output.append(crop.json())

        if output:
                
            context={
                "predictedtempnumber":totaltemp,
                "predictedprenumber":totalprec,
                "predictedtempmsg":msgtemp,
                "predictedprepmsg":msgprec,
                "name":vardict['name'],
                "place":vardict['place'],
                "date":year,
                "cropsinfo":output,
            }
        
            return JsonResponse(context)
        else:
            return JsonResponse({"error":"no food found"})
