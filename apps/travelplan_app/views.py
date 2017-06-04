# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from .models import userDB,travelplan,trip
from django.db.models import Count, Min, Sum, Avg
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    return render(request,'travelplan_app/index.html')

def register(request):
    if( request.method=='POST'):
        ret_val=userDB.objects.register(request.POST)
        if ret_val[0]:
            newusers=ret_val[1]
            request.session['user']={
                'id':newusers.id,
                'name':newusers.name,
            }
            context={
                "users": newusers
            }
            messages.add_message(request,messages.INFO,"Registered successfully!")
            return redirect('travelplan:travels')
        else:
            for error in ret_val[1]:
                print error;
                messages.error(request,error)
            return redirect('travelplan:index')
    return redirect('travelplan:index')
def login(request):
    if( request.method=='POST'):
        ret_val=userDB.objects.login(request.POST)
        if ret_val[0]:
            newusers=ret_val[1]
            request.session['user']={
                'id':newusers.id,
                'name':newusers.name,
            }
            context={
                "users": newusers
            }
            messages.add_message(request,messages.INFO,"Logged in successfully!")
            return redirect('travelplan:travels')
        else:
            for error in ret_val[1]:
                print error;
                messages.error(request,error)
            return redirect('travelplan:index')

    return redirect('travelplan:index')


def logout(request):
    request.session.clear()
    return redirect('travelplan:index')

def showadd(request):
    if 'user' in request.session :
        return render(request,'travelplan_app/plan.html')
    return redirect('travelplan:index')

def add(request):
    if 'user' in request.session :
        if( request.method=='POST'):
            ret_val=travelplan.objects.createTravel(request.POST)
        if ret_val[0]:
            newusers=ret_val[1]
        else:
            for error in ret_val[1]:
                print error;
                messages.error(request,error)
            return render(request,'travelplan_app/plan.html')
        return redirect('travelplan:travels')
    return redirect('travelplan:index')

def travels(request):
    if 'user' in request.session :
        if( request.method=='GET'):
            allusers=trip.objects.all()
            currentuser=userDB.objects.filter(id=request.session['user']['id'])
            newusers=travelplan.objects.filter(user_travel=currentuser)
            usersother=trip.objects.filter(user_trip=currentuser)
            other_users=travelplan.objects.filter(~Q(join_travel__in=trip.objects.filter(user_trip=currentuser)),~Q(user_travel=currentuser)).distinct()
            context={
                "users": newusers,
                "joinedtrips" : usersother,
                "others":other_users,
                "allusers":allusers
            }
            return render(request,'travelplan_app/travels.html',context)
    return redirect('travelplan:index')

def joinTrip(request,id):
    if 'user' in request.session :
        if( request.method=='POST'):
            try:
                retval=trip.objects.joinTrip(request.POST,id)
                return redirect('travelplan:travels')
            except:
                print("The destination doesn't exist")
                messages.error(request,"Couldnt Join the trip:DB error")
                return redirect('travelplan:travels')
    return redirect('travelplan:index')

def destination(request,id):
    if 'user' in request.session :
        if( request.method=='GET'):
            try:
                destination=travelplan.objects.get(id=id)
                otherusers=trip.objects.filter(Q(travel_join=destination))
                context={
                    "destination" : destination,
                    "otherusers" : otherusers
                }
                return render(request,'travelplan_app/destination.html',context)
            except:
                print("The destination doesn't exist")
                messages.error(request,"The destination doesn't exist.")
                return render(request,'travelplan_app/destination.html')
    return redirect('travelplan:index')

def delete(request):
    if 'user' in request.session :
        if(request.method=='POST'):
            trip.objects.all().delete()
            return redirect('travelplan:travels')
    return redirect('travelplan:index')
