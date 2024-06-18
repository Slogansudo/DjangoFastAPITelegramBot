from django.shortcuts import render, redirect
from django.views.generic import DetailView
from db_models.models import Status, OurTeam, Comments, Category, Product, Cart
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class UsersLoginView(View):
    def get(self, request):
        return render(request, 'auth/login_users.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        data = {'username': username,
                'password': password
                }
        login_form = AuthenticationForm(data=data)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('landing')
        else:
            return render(request, 'auth/login_users.html')


class UsersLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing')


class UserRegisterView(View):
    def get(self, request):
        return render(request, 'auth/register_user.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password_1']
        password2 = request.POST['password_2']
        if password1 != password2:
            return redirect('register')
        else:
            user = User(first_name=first_name, last_name=last_name, email=email, username=username)
            user.set_password(password1)
            user.save()
            return redirect('login')


class LandingPageView(View):
    def get(self, request):
        products = Product.objects.order_by('-discount')[:3]
        comments = Comments.objects.all()
        new_products = Product.objects.order_by('-last_update')[: 3]
        categories = Category.objects.order_by('-created_date')[:3]
        data = {'products': products,
                'comments': comments,
                'categories': categories,
                'new_products': new_products
                }
        return render(request, 'index.html', context=data)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'profile.html', {'user': user})


class SettingsProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'setting_acount.html', {'user': user})

    def post(self, request):
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if len(password1) < 4:
            return render(request, 'setting_acount.html', {'comment': 'Password must be at least'})
        if password1 != password2:
            return render(request, 'setting_acount.html', {'comment': 'The password was entered incorrectly'})
        else:
            users = User.objects.get(username=username)
            user = request.user
            if users.username != user.username:
                if not users:
                    user.username = username
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.set_password(password1)
                    user.save()
                    return redirect('landing')
                else:
                    return render(request, 'setting_acount.html', {'comment': 'such username exists'})
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.set_password(password1)
                user.save()
                user = User.objects.get(username=username)
                return render(request, 'setting_acount.html', {'user': user, 'comment': 'succesfull'})
