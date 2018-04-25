from __future__ import unicode_literals
from django.contrib.messages import constants as message_constants
from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import sessions, messages
from .models import User, Quotes
from forms import dateForm
import bcrypt
import re

MESSAGE_LEVEL = message_constants.DEBUG
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):

    return render(request, 'firstapp/index.html')


    


def process(request):
    success = True
    request.session['name'] = request.POST['name']
    request.session['alias'] = request.POST['alias']
    request.session['email'] = request.POST['email']
    request.session['password'] = request.POST['password']
    request.session['birthdate'] = request.POST['birthdate']
    password = request.session['password']
    hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    print hash1
    if request.method == 'POST':
        
        #First Name
        if len(request.POST['name']) < 2:
            success = False
            print "False First Name"
            messages.add_message(request, messages.INFO, 'Your first name must be longer than 2 characters.')
        
        #Last Name
        if len(request.POST['alias']) < 2:
            success = False
            print "Aliase"
            messages.add_message(request, messages.INFO, 'Your last name must be longer than 2 characters.')

        #Email
        if len(request.POST['email']) > 0:
            if EMAIL_REGEX.match(request.POST['email']):
                
                print "EMail is good!"
            else:
                messages.add_message(request, messages.INFO, 'Your Email is Invalid, enter an Email')
                success = False
        else:
            messages.add_message(request, messages.INFO, 'Your Email can''t'' be left blank!')
            success = False

        #Password
        if len(request.POST['password']) < 8:
            messages.add_message(request, messages.INFO, 'Your password must be 8 characters!')
            print "Invalid Password"
            success = False
        #Confirm Password
        if request.POST['confirm_password'] == request.POST['password']:
            print "Correct Password"
        if request.POST['confirm_password']!= request.POST['password']:
            messages.add_message(request, messages.INFO, 'Your passwords do not match!')
            print "false password"
            success = False

        if success == True:
            if User.objects.filter(email = request.session['email']).exists():
                messages.add_message(request, messages.INFO, 'A user with this Email already exists.')
                return redirect('/')
            User.objects.create(
                name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=hash1, birthdate=request.POST['birthdate'])
            request.session['name'] = request.POST['name']


            userid = User.objects.filter(email=request.POST['email']).all()
            for item in userid:
                request.session['user_id'] = item.id
                print "Success"
                return redirect('/quotes')
        if success == False:
            
            print 'Test Success'
            return redirect('/')

   

def success(request):
    print request.session['user_id']
    context = {
        'quotes': Quotes.objects.exclude(favorites=request.session['user_id']),
        'favorites': Quotes.objects.filter(favorites=request.session['user_id']),
    }
    return render(request, 'firstapp/success.html', context)


def login(request):
    listemail = User.objects.filter(email=request.POST['email']).all()
    hash1 = request.POST['password']
    for item in listemail:
        print hash1 
        if bcrypt.checkpw(hash1.encode(), item.password.encode()):
            print "Password match!"
            request.session['name'] = item.name
            request.session['user_id'] = item.id
            print request.session['name']
            return redirect('/quotes')
        else: 
            print "Passwords do not match"
            messages.add_message(request, messages.INFO, 'Your password is incorrect')
    return redirect('/')


def addquote(request):
    success = True
    print "Adding quote *************************"
    #Author
    if len(request.POST['author']) < 3:
        success = False
        print "Author name too short ************************************"
        messages.add_message(request, messages.INFO, 'The name of the author must be longer than 3 characters.')
        
    
    #Message
    if len(request.POST['message']) < 10:
        success = False
        print "Quote too short *********************************"
        messages.add_message(request, messages.INFO, 'The quote must be longer than 10 character')

    if success == True:
        print "True Success*****************************"
        user = User.objects.get(name=request.session['name'])
        context = {
            'quotes': Quotes.objects.create(author=request.POST['author'], message=request.POST['message'], poster=user)
        }
        return redirect('/quotes', context)

    if success == False:
        print "False Success *************************************"
        return redirect('/quotes')

def users(request, id):

    context = {
        'quotes': Quotes.objects.filter(poster_id=id),
        'user': User.objects.filter(id=id),
        'count': Quotes.objects.filter(poster=id).count()
    }
    print Quotes.objects.filter(poster=id).count()
    print id
    return render(request, 'firstapp/users.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')

def addfav(request, id):
    print "adding favorite ****************************"
    print id
    me = User.objects.get(id=request.session['user_id'])
    quotes = Quotes.objects.get(id=id)
    quotes.favorites.add(me)
    return redirect('/quotes')

def removefav(request, id):
    print "removing favorite *******************8"
    print id
    me = User.objects.get(id=request.session['user_id'])
    quotes = Quotes.objects.get(id=id)
    quotes.favorites.remove(me)
    return redirect('/quotes')
