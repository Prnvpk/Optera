from django.shortcuts import render
from .models import users,products,orders
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
from .forms import PaymentForm





# Create your views here.
def home(request):
    return render(request, 'login.html')

def index(request):
    featured_products = products.objects.all()[:4]
    return render(request, 'index.html', {'featured_products': featured_products})

def register(request):
    if request.method == 'POST':
        Name = request.POST.get('name')
        Email = request.POST.get('mail')
        Number = request.POST.get('num')
        Password = request.POST.get('pass')

        data = users.objects.create(
            name=Name,
            gmail=Email,
            number=Number,
            password=Password
        )
        data.save()
        return render(request, 'login.html')
    return HttpResponse("failed")

def showuser(request):
    data = users.objects.all()
    
    
    paginator = Paginator(data, 3)   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'view.html', {'page_obj': page_obj})


def login(request):
    if request.method == "POST":
        mail = request.POST.get('mail')
        pas  = request.POST.get('pass')  

        if mail == 'admin@gmail.com' and pas == 'admin123':
            return render(request,'admin.html')
        
        try:
            data = users.objects.get(gmail=mail, password=pas)
            request.session['uid'] = data.id
            return render(request,'index.html')
        except users.DoesNotExist:
            return HttpResponse("Invalid credentials")

def openuser(request):
    if 'uid' in request.session:

        data = request.session['uid']
        user= users.objects.get(gmail=data)

        return render(request,'profile.html',{'data':user})

def logout(request):
    request.session.flush()
    return redirect('/')

    

def openproduct(request):
    query =request.GET.get('q')

    if query:
        productitems=products.objects.filter(Q(product_name__icontains=query)|
                                             Q(description__icontains=query))
        
    else:
        productitems=products.objects.all()

    context={
        'products':productitems,
        'query':query,
    }
    return render(request,'product.html',context)
    
def dashboard(request):
    return render(request,'admin.html')




def addtocart(request, pid):
    cart = request.session.get('cart', {})

    pid = str(pid)  

    if pid in cart:
        cart[pid] += 1
    else:
        cart[pid] = 1

    request.session['cart'] = cart
    return redirect('cart')


def opencart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for pid, qty in cart.items():
        product = products.objects.get(id=int(pid))  
        subtotal = product.price * qty
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': qty,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def removefromcart(request, pid):
    cart = request.session.get('cart', {})

    pid = str(pid)  

    if pid in cart:
        del cart[pid]

    request.session['cart'] = cart
    return redirect('cart')

def increase_qty(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1

    request.session['cart'] = cart
    return redirect('cart')

def decrease_qty(request, id):
    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] -= 1
        if cart[str(id)] <= 0:
            del cart[str(id)]

    request.session['cart'] = cart
    return redirect('cart')




def address_page(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        house = request.POST.get('house', '').strip()
        street = request.POST.get('street', '').strip()
        city = request.POST.get('city', '').strip()
        pincode = request.POST.get('pincode', '').strip()

        if not all([name, mobile, house, street, city, pincode]):
            return HttpResponse(
                '<script>alert("Please fill all address fields."); window.history.back();</script>'
            )

        request.session['checkout_address'] = f"{name}, {mobile}, {house}, {street}, {city} - {pincode}"
        return redirect('payment')

    return render(request, 'address.html')



   


def addpro(request):
    if request.method == 'POST':
        Proname = request.POST.get('pname')
        Price = request.POST.get('price')
        Quantity = request.POST.get('quantity')
        Description = request.POST.get('description')
        Image = request.FILES.get('image')

        try:
            data = products.objects.create(
                product_name=Proname,
                price=Price,
                quantity=Quantity,
                description=Description,
                image=Image
            )
            data.save()
            return HttpResponse('<script>alert("Product added successfully"); window.location="/addproduct";</script>')
        
        except Exception :
            return HttpResponse("Something went wrong")
    return render(request,'addproduct.html')


def viewproduct(request):
    data = products.objects.all()
    return render(request, 'viewproduct.html', {'products': data})


def deleteproduct(request, id):
    product = get_object_or_404(products, id=id)
    product.delete()
    return redirect('viewproduct')



def editproduct(request, id):
    product = get_object_or_404(products, id=id)

    if request.method == 'POST':
        product.product_name = request.POST.get('pname')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.description = request.POST.get('description')

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        return redirect('viewproduct')

    return render(request, 'editproduct.html', {'product': product})

def openprofile(request):

    #Check session
    uid = request.session.get('uid')
    if not uid:
        return redirect('login')

    #Logged user
    data = get_object_or_404(users, id=uid)

    
    user_orders = orders.objects.filter(user=data).order_by('-id')

    
    total_orders = user_orders.count()

    context = {
        'data': data,
        'orders': user_orders,
        'total_orders': total_orders,
    }

    return render(request, 'profile.html', context)

def openbuy(request,id):
    product = products.objects.get(id=id)
    return render(request,'buy.html',{'product':product})


def buy(request,id):
    if request.method =='POST':
        product = products.objects.get(id=id)
        if 'uid' in request.session:

            user_id = request.session['uid']
            user = users.objects.get(id=user_id)

            quantity = request.POST.get('quantity')
            address = request.POST.get('address')
            try:
                order = orders.objects.create(product=product,user=user,quantity=quantity,address=address)
                order.save()
                product.quantity=product.quantity - int(quantity)
                product.save()
                return HttpResponse(
                    '<script>alert("Payment completed successfully!"); window.location="/my-orders/";</script>'
                 )
            except Exception:
                return HttpResponse('failed to place order')
        else:
            return HttpResponse('please login to continue')
    return HttpResponse('invalid request method')              




#payment


from django.shortcuts import render
from django.http import HttpResponse

def payment_page(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    user_id = request.session.get('uid')
    if not user_id:
        return redirect('/login')

    if request.method == "POST":
        card_number = request.POST.get("card_number")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")

        if not card_number or not expiry_date or not cvv:
            return HttpResponse(
                '<script>alert("Invalid Payment Details"); window.history.back();</script>'
            )

        address = request.session.get('checkout_address')
        if not address:
            return redirect('address')

        user = get_object_or_404(users, id=user_id)
        order_created = False

        for pid, qty in cart.items():
            product = products.objects.filter(id=int(pid)).first()
            if not product:
                continue

            quantity = int(qty)
            if quantity <= 0:
                continue

            if product.quantity <= 0:
                return HttpResponse(
                    f'<script>alert("{product.product_name} is out of stock."); window.location="/cart/";</script>'
                )

            if product.quantity < quantity:
                return HttpResponse(
                    f'<script>alert("Only {product.quantity} item(s) left for {product.product_name}."); window.location="/cart/";</script>'
                )

            orders.objects.create(
                product=product,
                user=user,
                quantity=quantity,
                address=address
            )
            product.quantity -= quantity
            product.save()
            order_created = True

        if not order_created:
            return HttpResponse(
                '<script>alert("No valid products found in cart."); window.location="/cart/";</script>'
            )

        request.session['payment_done'] = True
        request.session.pop('cart', None)
        request.session.pop('checkout_address', None)

        return HttpResponse(
            '<script>alert("Payment completed successfully!"); window.location="/my-orders/";</script>'
        )

    return render(request, "payment.html")




def admin_orders(request):
    all_orders = orders.objects.all().order_by('-order_date')
    paginator = Paginator(all_orders, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'adminorder.html', {
        'orders': page_obj,
        'page_obj': page_obj
    })





def update_order_status(request, oid):
    order = get_object_or_404(orders, id=oid)

    if request.method == "POST":
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()

    return redirect('admin_orders')



def user_order_status(request):
    user_id = request.session.get('uid')   # ✅ SAME SESSION NAME

    if not user_id:
        return redirect('login')

    user_orders = orders.objects.filter(user_id=user_id).order_by('-order_date')

    return render(request,'order_status.html',{'orders':user_orders})







