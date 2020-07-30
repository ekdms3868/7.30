from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, CustomUser
from .forms import ArticleForm, SigninForm, UserForm
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.http import HttpResponse

def main(request):
    posts = Article.objects.all()
    signin_form = SigninForm()
    return render(request, 'app/main.html', {'posts': posts, 'signin_form': signin_form})

def create(request):
    if not request.user.is_active:
        return HttpResponse("로그인 하세요")

    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.writer = request.user
            form.save()
            return redirect('main')
    else:
        form = ArticleForm()
        return render(request, 'app/create.html', {'form': form})

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return HttpResponse("로그인 실패")

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = CustomUser.objects.create_user(username=form.cleaned_data['username'], 
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            grade=form.cleaned_data['grade'],
            major=form.cleaned_data['major'])
            login(request, new_user)
            return redirect('main')
    else:
        form = UserForm()
        return render(request, 'app/signup.html', {'form':form})

def logout(request):
    auth.logout(request)
    return redirect('main')