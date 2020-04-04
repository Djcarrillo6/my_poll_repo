from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import bcrypt

from .forms import CreatePollForm
from .models import *


def index(request):
    return render(request, 'index.html')


def reg(request):
    errors = User.objects.validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")

    is_user_in_db = User.objects.filter(email=request.POST['email']).first()

    if is_user_in_db:
        print("Username already exists")
        return redirect("/")

    hashed_pw = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()

    user_created = User.objects.create(
        first_name=request.POST['fname'],
        last_name=request.POST['lname'],
        email=request.POST['email'],
        password=hashed_pw
    )

    request.session['user_id'] = user_created.id

    return redirect("/home")


def log(request):

    errors = User.objects.valid_login(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")

    found_user = User.objects.filter(email=request.POST['email']).first()

    if found_user:
        is_pw_correct = bcrypt.checkpw(
            request.POST['password'].encode(), found_user.password.encode())

        if is_pw_correct:
            request.session['user_id'] = found_user.id
            return redirect('/home')
        else:
            print("Password does NOT match our records!")
            return redirect("/")
    else:
        print("Email address does NOT match our records!")
        return redirect("/")


def logout(request):
    request.session.clear()
    return redirect("/")


def home(request):

    user_id = request.session.get('user_id')

    if user_id is None:
        messages.error(request, 'Please login/register')
        return redirect("/")
    else:
        polls = Poll.objects.filter(submitted_by=user_id)
        user_from_db = User.objects.get(id=user_id)
        context = {
            'user': user_from_db,
            'polls': polls,
        }
        return render(request, 'poll/home.html', context)


def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreatePollForm()
    context = {
        'form': form
    }
    return render(request, 'poll/create.html', context)


def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid Form')

        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll': poll
    }
    return render(request, 'poll/vote.html', context)


def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll': poll
    }
    return render(request, 'poll/results.html', context)


def delete_poll(request, poll_id):
    poll_to_delete = Poll.objects.get(pk=poll_id)
    poll_to_delete.delete()
    return redirect('/home')
