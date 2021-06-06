from django.shortcuts import render, redirect
from account.forms import register_form
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = register_form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username}'s Account Created Successfully!!!")
            return redirect('app-home')
    else:
        form = register_form()
    return render(request, 'account/register.html',{"form":form})

def login(request):
    return render(request, 'account/login.html')