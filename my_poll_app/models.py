from django.db import models
from django.contrib import messages
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data['fname']) < 2:
            errors['fname'] = "First name must be a minimum of 2 characters"
        if len(data['lname']) < 2:
            errors['lname'] = "Last name must be a minimum of 2 characters"
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Email address is invalid"
        if data['password'] != data['cpassword']:
            errors['password'] = "Passwords DO NOT match"
        if len(data['password']) < 8:
            errors['password'] = "Password must be AT LEAST 8 characters long"
        return errors

    def valid_login(self, data):
        errors = {}
        if data['email'] == "":
            errors['email'] = "Email CAN NOT be blank"
        if data['password'] == "":
            errors['password'] = "Password CAN NOT be blank"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = UserManager()


class Poll(models.Model):
    question = models.TextField()
    option_one = models.CharField(max_length=30)
    option_two = models.CharField(max_length=30)
    option_three = models.CharField(max_length=30)
    option_one_count = models.IntegerField(default=0)
    option_two_count = models.IntegerField(default=0)
    option_three_count = models.IntegerField(default=0)
    submitted_by = models.ForeignKey(
        User, related_name="user_polls", on_delete=models.CASCADE, default=True)

    def total(self):
        return self.option_one_count + self.option_two_count + self.option_three_count

