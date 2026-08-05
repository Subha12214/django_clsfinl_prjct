from django.shortcuts import render,redirect
from .models import Product,CartModel
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        cartproduct_count=CartModel.objects.filter(host=request.user).count()
    else:
        cartproduct_count=False
    print(request.method)
    print(request.GET)
    no_match=False
    trend=False
    offer=False
    if 'search' in request.GET:
        q=request.GET['search']
        data=Product.objects.filter(Q(pname__icontains=q) | Q(pdesc__icontains=q))
        if not data.exists():
            no_match=True
    elif 'category' in request.GET:
        cat=request.GET['category']
        # print(cat)
        data=Product.objects.filter(pcategory=cat)
    elif 'trending' in request.GET:
        data=Product.objects.filter(trending=True)
        trend=True
    elif 'offer' in request.GET:
        data=Product.objects.filter(offer=True)
        offer=True
    else:
        data=Product.objects.all()

    category=[]
    for i in Product.objects.all():
        # print(i.pcategory)
        if i.pcategory not in category:
            category+=[i.pcategory]
    print(category)
    return render(request,'home.html',{'data':data,'no_match':no_match,'category':category,'search':True,'trend':trend,'offer':offer,'cartproduct_count':cartproduct_count})

@login_required(login_url='login_')
def addtocart(request,id):
    product=Product.objects.get(id=id)
    try:
        cp=CartModel.objects.get(pname=product.pname,host=request.user)
        cp.quantity+=1
        cp.totalprice+=product.price
        cp.save()
    except:
        CartModel.objects.create(
            pname=product.pname,
            
            price=product.price,
            pcategory=product.pcategory,
            quantity=1,
            totalprice=product.price,
            host=request.user
        )
    return redirect('cart')

@login_required(login_url='login_')
def cart(request):
    cartproduct_count=CartModel.objects.filter(host=request.user).count()
    tp=0
    cart_products=CartModel.objects.filter(host=request.user)
    for i in cart_products:
        tp+=i.totalprice
    print(tp)
    return render(request,'cart.html',{'cart_products':cart_products,'tp':tp,'cartproduct_count':cartproduct_count})


@login_required(login_url='login_')
def remove(request,id):
    product=CartModel.objects.get(id=id)
    product.delete()
    return redirect('cart')


@login_required(login_url='login_')
def increment(request,id):
    product=CartModel.objects.get(id=id)
    product.quantity+=1
    product.totalprice+=product.price
    product.save()
    return redirect('cart')


@login_required(login_url='login_')
def decrement(request,id):
    product=CartModel.objects.get(id=id)
    if product.quantity>1:
        product.quantity-=1
        product.totalprice-=product.price
        product.save()
    else:
        product.delete()
    return redirect('cart')