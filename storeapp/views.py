from django.shortcuts import render
from .models import users,products
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q


# Create your views here.
def home(request):
    return render(request, 'login.html')

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

def openbuy(request,id):
    product = products.objects.get(id=id)
    return render(request,'buy.html',{'product':product})

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
    
    return render(request,'profile.html')

def dashboard(request):
    return render(request,'adminbar.html')