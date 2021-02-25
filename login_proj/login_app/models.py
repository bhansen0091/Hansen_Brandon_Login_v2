from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        first_name_regex = re.compile(r"^[A-Z]{1}[a-zA-Z]+$")
        if not first_name_regex.match(post_data['first_name']):
            errors["first_name_invalid"] = "First name must begin with a capital and consist only of letters."
        if len(post_data['first_name']) < 2:
            errors['first_name_short'] = "First name must be at leased 2 characters long."

        last_name_regex = re.compile(r"^[a-zA-Z]+$")
        if not last_name_regex.match(post_data['last_name']):
            errors['last_name_invalid'] = "First name must begin with a capital and consist only of letters."
        if len(post_data['last_name']) < 2:
            errors['last_name_short'] = "Last name must be at leased 2 characters long."

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(post_data['email_address']):
            errors['email_address_invalid'] = "Invalid email address."

        if post_data['password'] != post_data['confirm_password']:
            errors['password_no_match'] = "Your passwords dont match."
        if len(post_data['password']) < 8:
            errors['password_short'] = "Passwords must be at leased 8 characters long."

        try:
            User.objects.get(email_address = post_data['email_address'])
            errors['email_unique'] = "That email is already in use."
        except:
            pass
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    email_address = models.CharField(max_length=320)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

