import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Chat

import openai


OPENAI_SECRET_KEY = os.environ.get('OPENAI_SECRET_KEY')
openai.api_key = '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'


def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant'},
            {'role': 'user', 'content': message},
        ]
    )

    print(response)

    answer = response.choices[0].message.content.strip()
    return answer


def chatbot(request):

    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()

        return JsonResponse({'message': message, "response": response})
    
    context = {
        'chats': chats,
    }

    return render(request, 'chatbot.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)

                return redirect('home')
            except:
                error_message = 'Account creation failed. Please try again'
                context = {
                    'error_message': error_message
                }

                return render(request, 'register.html', context)

        else:
            error_message = 'Passwords don\'t match!'
            
            context = {
                'error_message': error_message
            }

            return render(request, 'register.html', context)
    return render(request, 'register.html')


def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password'
            context = {
                'error_message': error_message
                }
            return render(request, 'login.html', context)
        
    return render(request, 'login.html')

def logout(request):
    
    auth.logout(request)
    
    return redirect('login')