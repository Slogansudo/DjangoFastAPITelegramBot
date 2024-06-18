from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views import View

from db_models.models import Product, OurTeam, Comments, Category, Cart


# Create your views here.


class ShopView(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'shop.html', {'products': products})

    def post(self, request):
        data = request.POST.get("search")
        products = Product.objects.filter(title__icontains=data)
        if not products:
            if data == "chegirma":
                products = Product.objects.filter(discount__isnull=False)
                return render(request, 'shop.html', {'products': products})
        return render(request, 'shop.html', {'products': products})


class AboutUsView(LoginRequiredMixin, View):
    def get(self, request):
        team = OurTeam.objects.all()
        comments = Comments.objects.all()
        return render(request, 'about.html', {'team': team, 'comments': comments})


class ServicesView(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.filter(discount__isnull=False)
        return render(request, 'services.html', {'products': products})


class BlogsView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'blog.html', {'categories': categories})

    def post(self, request):
        search = request.POST.get("search")
        categories = Category.objects.filter(title__icontains=search)
        if not categories:
            if search.isdigit():
                categories = Category.objects.filter(products_count=search)
                return render(request, 'blog.html', {'categories': categories})
            return render(request, 'blog.html', {'categories': categories})
        return render(request, 'blog.html', {'categories': categories})


class ContactUsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, 'contact.html', {'user': user})


class ShopDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        categories = Category.objects.all()
        return render(request, 'shop-detail.html', {'product': product, 'categories': categories})

    def post(self, request, id):
        search = request.POST.get("comment")
        comment = Comments(customer=request.user, text=search)
        comment.save()
        product = Product.objects.get(id=id)
        product.comments.add(comment)
        product.save()
        cart = Cart(product=product, user=request.user, payment_status=False, total_price=product.price, price_type=product.price_type)
        cart.save()
        product = Product.objects.get(id=id)
        categories = Category.objects.all()
        return render(request, 'shop-detail.html', {'product':product, 'categories': categories})


class CartDetailView(LoginRequiredMixin, View):
    def get(self, request):
        users = request.user
        cart = Cart.objects.filter(user=users)
        total_price = 0
        price_type = ''
        for car in cart:
            total_price += car.total_price
            price_type = car.price_type
        number_order = cart.count()
        data = {'cart': cart,
                 'total_price': total_price,
                'price_type': price_type,
                'number_order': number_order
                }
        return render(request, 'cart.html', data)

    def post(self, request):
        users = request.user
        cart = Cart.objects.filter(user=users).first()
        if cart:
            cart.delete()
        cart = Cart.objects.filter(user=users)
        total_price = 0
        price_type = ''
        for product in cart:
            total_price += product.total_price
            price_type = product.price_type
        number_order = cart.count()
        data = {
            'cart': cart,
            'total_price': total_price,
            'number_order': number_order,
            'price_type': price_type
        }
        return render(request, 'cart.html', data)


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        users = request.user
        cart = Cart.objects.filter(user=users)
        total_price = 0
        price_type = ''
        for product in cart:
            total_price += product.total_price
            price_type = product.price_type
        number_order = cart.count()
        data = {
            'cart': cart,
            'total_price': total_price,
            'number_order': number_order,
            'price_type': price_type,
            "user": request.user
        }
        return render(request, 'checkout.html', data)

