from django.db import models
import datetime
from datetime import datetime
import re
from django.utils import timezone

class userManager(models.Manager):
    def validator(self,postData):
        errors={}
        if len(postData['fname']) < 2:
            errors["fname"] = "first name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "last name should be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email Address"
        if len(user.objects.filter(email = postData['email'])) > 0:
            errors["email"] = "Email address must be unique"

        if postData['bdate'] == "":
            errors["bdate"] = "Birth date is mandatory"
        else:
            bdate = datetime.strptime(postData['bdate'],'%Y-%m-%d')
            date_num1 = datetime.today().year
            date_num2 = bdate.year
            if datetime.today() < bdate:
                errors["bdate"] = "Birth date should be in the past"
            elif (date_num1 - date_num2) < 13:
                errors["bdate"] = "Age should be 13 years old at least"

        if len(postData['pass']) < 8:
            errors["password"] = "password should be at least 8 charcters"
        if postData["con-pass"] != postData['pass']:
            errors["password"] = "Password should be the same"
        return errors

class user(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.CharField(max_length=45)
    birth_date=models.DateField()
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=userManager()

    def create(first,last,email,birth,pwd):
        return user.objects.create(
        first_name=first,
        last_name=last,
        email=email,
        birth_date=birth,
        password=pwd
        )
    
    def show_logged(id):
        return user.objects.get(id=id)
    

class messageManager(models.Manager):
    def validator(self,postData):
        errors={}
        if postData['content'] =="" :
            errors["content"] = "Post should not be empty"
        return errors

class message(models.Model):
    message=models.TextField()
    user_owner=models.ForeignKey(user, related_name= "uploaded_messages", on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=messageManager()

    def show():
        return message.objects.all().order_by("-created_at")

    def create(content,id):
        return message.objects.create(
            message=content,
            user_owner= user.objects.get(id=id), 
        )

    def delete(id1):
        m1 = message.objects.filter(id=id1)
        post_date = m1[0].created_at
        current_date = timezone.now()
        mins = (current_date -post_date).total_seconds()/60
        errors={}
        if mins < 30:
            m1.delete()
        else:
            errors["time"] = "30 mins is already passed"
        return errors

class commentManager(models.Manager):
    def validator(self,postData):
        errors={}
        if postData['content'] =="" :
            errors["content"] = "Comment should not be empty"
        return errors

class comment(models.Model):
    comment=models.TextField()
    user_owner=models.ForeignKey(user, related_name= "uploaded_comments", on_delete = models.CASCADE)
    message_owner=models.ForeignKey(message, related_name= "related_comments", on_delete = models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=commentManager()

    def show():
        comment.objects.all()

    def create(content,usr_id,mess_id):
        return comment.objects.create(
            comment=content,
            user_owner = user.objects.get(id=usr_id),
            message_owner= message.objects.get(id=int(mess_id))
        )

    def delete(id):
        c1 = comment.objects.filter(id=int(id))
        c1.delete()