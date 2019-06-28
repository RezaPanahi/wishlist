from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime

now = str(datetime.now())

class UserManager(models.Manager):
    def regValidator(self, form):
        name = form['name']
        username = form['username']
        reg_password = form['reg_password']
        confirm_password = form['confirm_password']
        date_hired = form['date_hired']

        errors = {}

        if not name:
            errors['name'] = 'Name cannot be blank.'
        elif len(name) < 3:
            errors['name'] = 'Name must be at least 3 characters'



        if not username:
            errors['username'] = 'Username cannot be blank.'
        elif len(username) < 3:
            errors['username'] = 'Username must be at least 3 characters'


        if not reg_password:
            errors['reg_password'] = 'Password cannot be blank.'
        elif len(reg_password) < 8:
            errors['reg_password'] = 'Password must be at least 8 characters long.'


        if not confirm_password:
            errors['confirm_password'] = 'Please enter password.'
        elif reg_password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match.'


        if not date_hired:
            errors['date_hired'] = 'Date hired cannot be blank.'
        elif str(form['date_hired']) > str(now):
            errors['date_hired'] = "Cannot pick future date"

        return errors

    def loginValidator(self,form):
        username = form['username']
        password = form['password']
        errors = {}

        if not username:
            errors['username'] = 'Username name cannot be blank.'
        elif not User.objects.filter(username=username):
            errors['username'] = 'Username does not exist. Please register'
        # IF EMAIL GOES THROUGH, DO THIS:
        else:
            if not password:
                errors['password'] = 'Password required.'
                return errors, False
            else:
                user = User.objects.get(username=username)

                if not bcrypt.checkpw(password.encode(), user.password.encode()):
                    errors['password'] = 'Incorrect password. Please try again.'
                return errors, user
        return errors, False


class wishListManager(models.Manager):
    def wishListValidator(self, form):
        item = form['item']


        errors = {}

        if not item:
            errors['item'] = 'item field cannot be blank'
        elif len(item) < 4:
            errors['item'] = 'Item must be at least 4 characters long.'

        return errors

class User(models.Model):
    name= models.CharField(max_length=255)
    username= models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class wishList(models.Model):
    item = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name='item_added', on_delete=models.CASCADE)
    add_other_user_item_to_wishlist = models.ManyToManyField(User, related_name='other_user_item_added')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = wishListManager()
