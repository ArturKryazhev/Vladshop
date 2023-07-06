from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm
from django.contrib.auth.models import User

def mainPage(request):
    notebooks = Notebook.objects.all()
    smartphones = SmartPhone.objects.all()
    categories=Category.objects.all()
    cart = Cart.objects.all()
    context={'notebooks':notebooks,
             'smartphones':smartphones,
             'categories':categories,
             'cart': cart}
    print(context)
    return render(request, 'base.html', context)

def notebookView(request,post_slug):
    notebooks = Notebook.objects.get(slug=post_slug)

    context={'notebooks': notebooks
             }
    return render(request, 'notebook_detail.html',context)

def smartphoneView(request,post_slug):
    smartphones = SmartPhone.objects.get(slug=post_slug)
    context={'smartphones': smartphones}
    return render(request, 'smartphone_detail.html',context)

def AddToCartView(request,slug):
    
    
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user).first()
    else:
        cart=Cart.objects.filter(for_anonymous_user = True)
        if not cart:
            cart = Cart.objects.create(for_anonymous_user = True)
    notebooks = Notebook.objects.get(slug=slug)
    notebook_cart, created = notebook_has_Cart.objects.get_or_create(products = notebooks, carts = cart, kolichestvo= 1)
    return redirect('cart')

def AddToCartViewSmartphone(request,slug): #проверить, добавить в url
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user).first()
    else:
        cart=Cart.objects.filter(for_anonymous_user = True)
        if not cart:
            cart = Cart.objects.create(for_anonymous_user = True)
    smartphones = SmartPhone.objects.get(slug=slug)
    smartphone_cart, created = smartphone_has_Cart.objects.get_or_create(products = smartphones, carts = cart, kolichestvo= 1)
    return redirect('cart')

def CartView(request):
    cart = Cart.objects.filter(user = request.user).first()
    try:
        notebooks_in_cart = notebook_has_Cart.objects.filter(carts=cart)
    except notebook_has_Cart.DoesNotExist:
        notebooks_in_cart = None
       
    try:
        smartphone_in_cart = smartphone_has_Cart.objects.filter(carts=cart)
    except smartphone_has_Cart.DoesNotExist:
        smartphone_in_cart = None
      
  
   # products = smartphones + notebooks
    context = {'notebooks_in_cart':notebooks_in_cart,
               'smartphone_in_cart': smartphone_in_cart}
    return render(request, 'cart.html',context)

def CartEditNotebook(request, pk):
   
    notebooks_in_cart = notebook_has_Cart.objects.get(id=pk)
    qty = int(request.POST.get('qty'))
    notebooks_in_cart.kolichestvo = qty
    notebooks_in_cart.save() 
    return redirect('cart')   

def CartEditSmartphone(request, pk):
    smartphone_in_cart = smartphone_has_Cart.objects.get(id=pk)
    qty = int(request.POST.get('qty'))
    smartphone_in_cart.kolichestvo = qty
    smartphone_in_cart.save() 
    return redirect('cart') 

def CheckoutView(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user).first()
    else:
        cart=Cart.objects.filter(for_anonymous_user = True)
    
    try:
        notebooks_in_cart = notebook_has_Cart.objects.filter(carts=cart)
    except notebook_has_Cart.DoesNotExist:
        notebooks_in_cart = None
       
    try:
        smartphone_in_cart = smartphone_has_Cart.objects.filter(carts=cart)
    except smartphone_has_Cart.DoesNotExist:
        smartphone_in_cart = None
    form = OrderForm()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = request.user
            new_order.products_from_cart = cart
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.comment = form.cleaned_data['comment'] 
            new_order.save()
            return redirect('/')

    context = {
        'notebooks_in_cart':notebooks_in_cart,
        'smartphone_in_cart': smartphone_in_cart,
        'cart': cart,
        'form': form
    }
    return render(request, 'checkout.html',context)

def  MakeOrderView(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user = request.user).first()
    else:
        cart=Cart.objects.filter(for_anonymous_user = True)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = request.user
            new_order.products_from_cart = cart
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.comment = form.cleaned_data['comment'] 
            new_order.save()
            return redirect('/')
    return redirect('/checkout/')
# Create your views here.
