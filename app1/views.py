from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from json.decoder import JSONDecodeError
from django.core.exceptions import ObjectDoesNotExist
from .models import Feedback
from .models import Order
from .models import Cust
from .models import cartforuser
from .models import painting
from .cart import Cart
import json
from django.http import JsonResponse
# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    paintings = painting.objects.all()
    username = request.session.get('username', '')
    cart_items = None
    count=0
    if username:
        cart_items_obj = cartforuser.objects.filter(username=username).first()
        if cart_items_obj:
            cart_items_json = cart_items_obj.cartcontent
            cart_items = json.loads(cart_items_json)
            count = len(cart_items)
    return render(request, 'home.html', {'paintings': paintings, 'username': username, 'cart_items': cart_items,'count': count})

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2 or len(pass1)<8:
            xyz="justnottogeterror"
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            subject = 'Account Created Successfully'
            message = 'Your account has been successfully created.'
            from_email = 'paintingwebsitepal@example.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            return redirect('login')
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        acc=request.POST.get('acc')
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            if acc=="Customer":
                request.session['username'] = username
                return redirect('home')
            else:
                return render(request, 'painterhome.html')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')
def Customize(request):
   if request.method == 'POST':
        fn = request.POST.get('firstName')
        ln = request.POST.get('lastName')
        uemail = request.POST.get('email')
        uphone = request.POST.get('phone')
        mess = request.POST.get('message')
        img = request.FILES.get('image') 
        name=fn+' '+ln
        cq = Cust.objects.create(
            fname=fn,
            lname=ln,
            email=uemail,
            phone=uphone,
            message=mess,
            cimage=img 
        )
        subject = 'Customized Order Details '
        message = name+', We recived your order.\nYour order will be delivered shortly.\nThank you'
        from_email = 'paintingwebsitepal@example.com'
        recipient_list = [uemail]
        send_mail(subject, message, from_email, recipient_list)
        cq.save()
        return render(request, 'customize.html')
   else:
       return render(request, 'customize.html')
def LogoutPage(request):
    logout(request)
    return redirect('login')
def Deletequery(request,qid):
    query=Cust.objects.get(pk=qid)
    email = query.email
    fname=query.fname
    lname=query.lname
    name=fname+" "+ lname
    query.delete()
    subject = 'Customized Order Details '
    message = name+',Your order has been delivered succesfully.\nThank you'
    from_email = 'paintingwebsitepal@example.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    queries=Cust.objects.all()
    return render(request, 'viewcustomize.html' ,{'queries':queries})
def PainterHomePage(request):
    return render(request, 'painterhome.html')
def Viewfeedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'viewfeedback.html',{'feedbacks': feedbacks})
def aboutus(request):
    return render(request, 'aboutus.html')
def Viewcustomize(request):
    queries=Cust.objects.all()
    return render(request, 'viewcustomize.html' ,{'queries':queries})
def contact(request):
    if request.method == 'POST':
        fn=request.POST.get('firstname')
        ln=request.POST.get('lastname')
        uemail=request.POST.get('email')
        uphone=request.POST.get('phone')
        mess=request.POST.get('message')
        name=fn+' '+ ln
        subject = 'FeedBack Appericiation '
        message = name+',Thanks for you valuable feedback.\nThank you'
        from_email = 'paintingwebsitepal@example.com'
        recipient_list = [uemail]
        send_mail(subject, message, from_email, recipient_list)
        fb=Feedback(fname=fn, lname=ln, email=uemail, phone=uphone, message=mess)
        fb.save()
        return render(request, 'contact.html')
    else:
        return render(request, 'contact.html')
def Uploadpainting(request):
    if request.method == 'POST':
        uimg = request.FILES.get('myFile')
        uname = request.POST.get('paintingName')
        uprice = request.POST.get('paintingPrice')
        umedium = request.POST.get('paintingMedium')
        urating = '0'
        people='0'
        paint = painting(img=uimg, name=uname, price=uprice, medium=umedium, rating=urating,noofpeoplerated=people)
        paint.save()
        return redirect('uploadpainting')  
    else:
        paintings = painting.objects.all()
        return render(request, 'uploadpainting.html', {'paintings': paintings})
def updaterating(request, pid,prating):
    try:
        update = painting.objects.get(pk=pid)
        new_rating = float(prating)
        current_rating = float(update.rating)
        current_no_of_people_rated = int(update.noofpeoplerated)
        total_people_rated = current_no_of_people_rated + 1
        new_avg_rating = ((current_rating * current_no_of_people_rated) + new_rating) / total_people_rated
        update.rating = round(new_avg_rating, 2)
        update.noofpeoplerated = total_people_rated
        update.save()
        paintings = painting.objects.all()
        return render (request,'home.html',{'paintings': paintings})
    except painting.DoesNotExist:
        return HttpResponse("The painting does not exist.")
def Deletepainting(request, pid):
    try:
        paint = painting.objects.get(pk=pid)
        paint.delete()
    except ObjectDoesNotExist:
        pass
    paintings = painting.objects.all()
    return render(request, 'uploadpainting.html', {'paintings': paintings})
def Placeorder(request):
    return render(request,'placeorder.html')



def cartsave(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        new_cartcon = request.POST.get('cart')
        try:
            new_cart_content = json.loads(new_cartcon)
        except JSONDecodeError:
            return redirect('home')
        existing_cart = cartforuser.objects.filter(username=uname).first()
        if existing_cart:
            existing_cart_content = json.loads(existing_cart.cartcontent)
            for item in new_cart_content:
                if item not in existing_cart_content:
                    existing_cart_content.append(item)
            existing_cart.cartcontent = json.dumps(existing_cart_content)
            existing_cart.save()
        else:
            cfu = cartforuser(username=uname, cartcontent=new_cartcon)
            cfu.save()
        
        return redirect('home')


def remove_item_from_cart(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        title = request.POST.get('title')
        username = request.session.get('username', '')
        if username:
            cart_items_obj = cartforuser.objects.filter(username=username).first()
            if cart_items_obj:
                cart_items = json.loads(cart_items_obj.cartcontent)
                cart_items = [item for item in cart_items if item['title'] != title]
                cart_items_obj.cartcontent = json.dumps(cart_items)
                cart_items_obj.save()
                return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

def payment_page(request):
    if 'username' in request.session:
        username = request.session.get('username', '')
        cart_items = cartforuser.objects.filter(username=username).first()
        if cart_items:
            cart_content = eval(cart_items.cartcontent)  
            total_price = sum(int(item['price'].replace('Rs.', '')) * int(item['quantity']) for item in cart_content)
            if cart_content:
                return render(request, 'payment.html', {'cart_content': cart_content, 'total_price': total_price})
            else:
                return render(request, 'nothing.html') 
        else:
            return render(request, 'nothing.html')
    else:
        return redirect('login')  

def payment_success(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        total = request.POST.get('total')
        details = request.POST.get('details') 
        order = Order(
            username=request.user.username, 
            name=name,
            details=details,
            phone=phone,
            email=email,
            address=address,
            total=total
        )
        order.save()
        subject = 'Order  Confirmation'
        message = name+',Your Payment is successful\nYour order '+details+' has been Confired.\nThank you'
        from_email = 'paintingwebsitepal@example.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        username=request.user.username
        cartremove= cartforuser.objects.filter(username=username).first()
        cartremove.delete()
        return redirect('home') 
    else:
        return HttpResponse("Invalid request method")

def Vieworders(request):
    orders = Order.objects.all()  
    return render(request, 'vieworders.html', {'orders': orders})
def deleteorder(request,oid):
    try:
        orders=Order.objects.get(pk=oid)
        email=orders.email
        details=orders.details
        name=orders.name
        orders.delete()
        subject = 'Order Delivery '
        message = name+',Your order '+details+' has been delivered succesfully.\nThank you'
        from_email = 'paintingwebsitepal@example.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
    except ObjectDoesNotExist:
        pass
    return redirect('vieworders')
