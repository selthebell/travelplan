# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
from django.db import models
from datetime import date
from django.utils.dateparse import parse_date
import re
EMAIL_REGEX=re.compile(r"(^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


class userDBManager(models.Manager):
      def login(self, postData):
          errors=[]
          if( (len(postData['username'])<3) ):
               print "UserName has to be atleast 3characters!"
               errors.append("UserName has to be atleast 3characters!")
          if(len(postData['password'])<8):
               print "Password less than 8characters"
               errors.append("Password needs to be 8 characters long")
          if errors:
              print "Not Created"
              return(False,errors)
          ret_user=userDB.objects.filter(username=postData['username'])
          if ret_user:
              userFound=userDB.objects.get(username=postData['username'])
              password=postData['password'].encode()
                # Check that a unhashed password matches one that has previously been
                #   hashed
              if bcrypt.checkpw(password.encode(), userFound.password.encode()):
                  return(True,userFound)
              else:
                  errors.append("Could not login")
                  return(False,errors)
          else:
              errors.append("Could not login")
              return(False,errors)

      def register(self, postData):
          errors=[]
          print postData
          if(len(postData['name'])<3):
              print "Name is not entered"
              errors.append("Name has to be atleast 3characters!")
          if( (len(postData['username'])<3) ):
              print "Username is not entered correct"
              errors.append("UserName has to be atleast 3characters!")
          if(len(postData['password'])<8):
              print "password less than 8characters"
              errors.append("Password needs to be 8 characters long!")
          if(postData['password']<>postData['confirm_pwd']):
              print "both passwords do not match"
              errors.append("Please confirm password")
          if errors:
              print "not created"
              return(False,errors)
          else:
              ret_user=userDB.objects.filter(username=postData['username'])
              if ret_user:
                  errors.append("Please use different login info!")
                  print "Please use different login info!"
                  return(False,errors)
              print "inside save"
              password=postData['password'].encode();
               # Hash a password for the first time, with a randomly-generated salt
              hashed = bcrypt.hashpw(password, bcrypt.gensalt())
              newUser=userDB(name=postData['name'],username=postData['username'],password=hashed)
              newUser.save()
              return(True,newUser)

class userDB(models.Model):
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    username=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects=userDBManager()
class travelplanManager(models.Manager):
    def createTravel(self,postData):
        errors=[]
        date_str=postData['fromdate'].encode()
        dateFrom=parse_date(date_str)
        date_str1=postData['todate'].encode()
        dateTo=parse_date(date_str1)
        dateToday=date.today()
        if(len(postData['destination'])<=0):
            print "Destination needs to be entered"
            errors.append("Destination needs to be entered!")
        if(len(postData['description'])<=0):
            print "Description needs to be entered"
            errors.append("Description needs to be entered!")
        if(  date_str=="" or dateToday > dateFrom ):
            print "From Date entered needs to be later than today"
            errors.append("From Date entered needs to be later than today!")
        if(  date_str1=="" or dateFrom > dateTo):
            print "To Date entered needs to be greater than Start date"
            errors.append("To Date entered needs to be greater than Start date!")
        if errors:
            print "Not Created"
            return(False,errors)
        else:
            currentuser=userDB.objects.get(id=postData['id'])
            traveluser=travelplan(destination=postData['destination'],description=postData['description'],traveldate_from=postData['fromdate'],traveldate_to=postData['todate'],user_travel=currentuser)
            traveluser.save()
            return(True,traveluser)

class travelplan(models.Model):
    destination=models.CharField(max_length=50)
    description=models.TextField()
    traveldate_from=models.DateField()
    traveldate_to=models.DateField()
    user_travel=models.ForeignKey(userDB,related_name='travel_user')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects=travelplanManager()

class tripManager(models.Manager):
    def joinTrip(self,postData,id):
        usertrip=userDB.objects.get(id=postData['userid'])
        traveljoin=travelplan.objects.get(id=id)
        tripplan=trip(user_trip=usertrip,travel_join=traveljoin)
        tripplan.save()
        return(True,tripplan)

class trip(models.Model):
    user_trip=models.ForeignKey(userDB,related_name='trip_user')
    travel_join=models.ForeignKey(travelplan,related_name='join_travel')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects=tripManager()
