from django.shortcuts import render,redirect
from .models import *
import bcrypt
from django.contrib import messages

def form(request):
    return render(request,"form.html")

def register(request):
    errors = user.objects.validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        passwd = request.POST['pass']
        hashed_pwd= bcrypt.hashpw(passwd.encode(), bcrypt.gensalt()).decode()
        X =user.create(
            first=request.POST['fname'],
            last=request.POST['lname'],
            email=request.POST['email'],
            birth=request.POST['bdate'],
            pwd=hashed_pwd
        )
        request.session['id'] = X.id
        request.session['username'] = X.first_name
    return redirect("/wall")

def login(request):
    check_user = user.objects.filter(email=request.POST['e-mail'])
    if check_user:
        logged_user = check_user[0]
        if bcrypt.checkpw(request.POST['passwd'].encode(),logged_user.password.encode()):
            request.session['id'] = logged_user.id
            request.session['username'] = logged_user.first_name
            return redirect("/wall")
        else:
            messages.error(request,"Invalid password")
            return redirect("/")
    else:
        messages.error(request,"Invalid email")
        return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def wall(request):
    if not 'id' in request.session:
        messages.error(request,"No user logged in")
        return redirect("/")
    context={
        "allmessage":message.show(),
        "allcomment":comment.show()
    }
    return render(request, "wall.html",context)

def create_post(request):
    errors = message.objects.validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect("/wall")
    message.create(
        request.POST['content'],
        request.session['id']
    )
    return redirect("/wall")

def delete_post(request,id):
    errors = message.delete(id)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
    return redirect("/wall")

def create_comment(request):
    errors = comment.objects.validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect("/wall")
    comment.create(
        request.POST['content'],
        request.session['id'],
        request.POST['mess']
    )
    return redirect("/wall")

def delete_comment(request,id):
    comment.delete(id)
    return redirect("/wall")