from unicodedata import category
import django
from django.contrib.auth.models import User
from eventapp.models import Address, Cart, EventCategory, EventDetails
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm, AddressForm
from django.contrib import messages
from django.views import View
import decimal
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator # for Class Based Views


# Create your views here.

def home(request):
    categories = EventCategory.objects.filter(is_active=True, is_featured=True)[:3]
    products = EventDetails.objects.filter(is_active=True, is_featured=True)[:8]
    context = {'categories': categories,'products': products,}
    return render(request, 'index.html', context)


def detail(request, slug):
    product = get_object_or_404(EventDetails, slug=slug)
    related_products = EventDetails.objects.exclude(id=product.id).filter(is_active=True, category=product.category)
    context = {
        'product': product,
        'related_products': related_products,

    }
    return render(request, 'store/detail.html', context)


def all_categories(request):
    categories = EventCategory.objects.filter(is_active=True)
    return render(request, 'store/categories.html', {'categories':categories})


def category_products(request, slug):
    category = get_object_or_404(EventCategory, slug=slug)
    products = EventDetails.objects.filter(is_active=True, category=category)
    categories = EventCategory.objects.filter(is_active=True)
    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/category_products.html', context)


# Authentication 
class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'account/register.html', {'form': form})
    
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations! Registration Successful!")
            form.save()
        return render(request, 'account/register.html', {'form': form})
        

@login_required
def profile(request):
    addresses = Address.objects.filter(user=request.user)

    return render(request, 'account/profile.html', {'addresses':addresses})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        form = AddressForm()
        return render(request, 'account/add_address.html', {'form': form})

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            user=request.user
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            reg = Address(user=user, city=city, state=state)
            reg.save()
            messages.success(request, "New Address Added Successfully.")
        return redirect('store:profile')


@login_required
def remove_address(request, id):
    a = get_object_or_404(Address, user=request.user, id=id)
    a.delete()
    messages.success(request, "Address removed.")
    return redirect('store:profile')

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(EventDetails, id=product_id)

    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()
    
    return redirect('store:cart')


@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    amount = decimal.Decimal(0)
    shipping_amount = decimal.Decimal(10)
    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount

    addresses = Address.objects.filter(user=user)

    context = {
        'cart_products': cart_products,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'total_amount': amount + shipping_amount,
        'addresses': addresses,
    }
    return render(request, 'store/cart.html', context)


@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('store:cart')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('store:cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('store:cart')


@login_required
def checkout(request):
    user = request.user
    address_id = request.GET.get('address')
    address = get_object_or_404(Address, id=address_id)

    cart = Cart.objects.filter(user=user)
    for c in cart:
        
        c.delete()
    return redirect('store:cart')

def shop(request):
    return render(request, 'store/shop.html')

def test(request):
    return render(request, 'store/test.html')

#admin
def admin(request):
    return render(request,'admin.html')

@login_required
def addcat(request):
    if request.method == 'POST':
        title=request.POST['title']
        slug=request.POST['slug']
        description=request.POST['description']
        is_active=request.POST['is_active']
        is_featured=request.POST['is_featured']
        category_image=request.FILES['category_image']
        
        cat=EventCategory(title=title,
                    slug=slug,
                    description=description,
                    is_active=True,
                    is_featured=True,
                    category_image=category_image,)
                    
        cat.save()
        print('success')
        return redirect('store:addpro')
    ve=EventCategory.objects.all()
    return render(request,'store/addcat.html',{'ve':ve} )


@login_required
def addpro(request):
    if request.method == 'POST':
        title=request.POST['title']
        slug=request.POST['slug']
        price=request.POST['price']
        category=request.POST['category']
        category=EventCategory.objects.get(id=category)
        detail_description=request.POST['detail_description']
        is_active=request.POST['is_active']
        is_featured=request.POST['is_featured']
        product_image = request.FILES['file']
        pro=EventDetails(title=title,
                    slug=slug,
                    price=price,
                    category=category,
                    detail_description=detail_description,
                    is_active=True,
                    is_featured=True,
                    product_image=product_image)  
        pro.save()
        print('success')
        return redirect('store:showpage')
    we=EventCategory.objects.all()
    return render(request,'./store/addpro.html',{'we':we} )


@login_required
def deleteproduct(request,pk):
    pro=EventDetails.objects.get(id=pk)
    pro.delete()  
    print("successfully deleted")
    return redirect('store:showpage')

    
@login_required
def showpage(request):
    a=EventDetails.objects.all()
    return render(request,'./store/showcat.html',{'all':a})

def edit (request,pk): 
    cat=EventCategory.objects.get(id=pk)
    pro=EventDetails.objects.get(id=pk)
    return render(request, 'edit.html', {'stud': cat,'std':pro})

def edit_pro(request,pk):
    if request.method=='POST':
        prod=EventDetails.objects.get(id=pk)
        prod.title = request.POST.get('title')
        prod.slug = request.POST.get('slug')
        prod.detail_description=request.POST.get('age')
        prod.product_image = request.POST.get('Tname')
        prod.price = request.POST.get('price')
        prod.save() 
        print("successfully updated")
        return redirect('showpage')
    return render(request,'showcat.html',)