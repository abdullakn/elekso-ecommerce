from django import forms
from accounts.forms import ReviewForm
from products.models import Product_Table
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views import View
from .models import *
from products.models import *
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from  django.contrib.sessions.models import Session
from django.views.decorators.cache import cache_control
from django.contrib import messages
from cart.models import CartItem,Cart
from cart.views import _cart_id
from django.http import JsonResponse
import json
from order.models import OrderProduct
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator  
from django.core.mail import EmailMessage
import os
from twilio.rest import Client
import random
from datetime import date, datetime, timedelta
import requests
from . decorator import login_required
from . utils import is_logged_in
import uuid

from django.core.files.base import ContentFile
import base64

from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.


def sample_view(request):
    return render(request,'accounts/signin.html')

def register(request):
    return render(request,'accounts/register.html')


def profile_view(request,ref_code):
    ref_id=str(ref_code)
    try:
        print("inside try")
        referal=Referal.objects.get(code=ref_id)
        print(referal)
        request.session['ref_profile']=referal.id
        print(request.session['ref_profile'])
        print("try end")
    except:
        pass      


def generate_coupen():
    coupen=str(uuid.uuid4()).replace("-","")[:4]
    return coupen


    

class UserRegistation(View):
   
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('user_home')
        return render(request,'accounts/register.html') 

    def post(self,request):
       data=request.POST
       username=data['username']
       email=data['email']
       phone_number=data['phonenumber']
       password=data['password']
       confirm=data['confirmpassword']
       ref_code=data['referal']
       if password != confirm :
           return render(request,'accounts/register.html',{'err':"Password are not same"})
       else:    
            user_data=UserData.objects.create_user(username=username,email=email,phone_number=phone_number,password=password)
            user_data.save()
            print("before func")
            profile_view(request,ref_code)
            print("after func")
            referal_id=request.session.get('ref_profile')
            print(referal_id)
            if referal_id is not None:
                recommended_by_profile=Referal.objects.get(id=referal_id)
                print(recommended_by_profile)
                print("after reco")
                registered_user=UserData.objects.get(id=user_data.id)
                print(registered_user)
                print("after reg")
                registered_profile=Referal.objects.get(user=registered_user)
                print(registered_profile)
                registered_profile.recommended_by=recommended_by_profile.user
                registered_profile.save()
                if registered_profile.recommended_by == None:
                    pass
                else:
                    generate=generate_coupen()
                    coupen="REF"+generate
                    coupen1="REC"+generate
                    print(coupen1)
                    coupen_obj=ReferalCoupen(user=user_data,coupen_code=coupen)
                    coupen_obj.save()
                    coupen1_obj=ReferalCoupen(user=recommended_by_profile.user,coupen_code=coupen1)
                    print(coupen1_obj)

                    coupen1_obj.save()

                    #get the refered user
                    # coupen1=generate_coupen()

            

            user=authenticate(request,username=username,password=password)
            if user is not None:
                    login(request,user)
                    
                    return redirect('user_home')
                    

# class Login(View):
  
#     def get(self,request):
#         if request.user.is_authenticated:
#             return redirect('user_home')
        
#         return render(request,'accounts/signin.html')

#     def post(self,request):
#         data=request.POST
#         username=data["username"]
#         password=data['password']
#         user=authenticate(request,username=username,password=password)
#         use=UserData.objects.get(username=username)
#         if use.is_active == False:
#             messages.info(request,"Your Account is Blocked")
#             return redirect('login')
#         print(user)
#         if user is not None:

           

#             try:

#                 current_item=CartItem.objects.filter(user=user)
#                 print(current_item)
#                 item_list=[]
#                 for item in current_item:
#                     item_list.append(item.product)

#                 print(item_list[0])    

           
#                 cart=Cart.objects.get(cart_id=_cart_id(request))
#                 print(cart)
#                 current_item=CartItem.objects.filter(user=request.user)
#                 print(current_item)
#                 is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
#                 print(is_cart_item_exists)
#                 if is_cart_item_exists:
#                     cart_item=CartItem.objects.filter(cart=cart)
                   
#                     print(cart_item[0].product)
                    
#                     for item in cart_item:
#                         if item.product in item_list:
                            
#                             pro=CartItem.objects.get(product=item.product)
#                             print(pro)
#                             pro.quantity+=1
#                             pro.user=user
#                             pro.save()
#                         else:   
#                             cart_items=CartItem.objects.filter(cart=cart) 
#                             for item in cart_items:
#                                 item.user=user                       
#                                 item.save()            
                        

#             except:
#                 pass  

                 
                    
#             login(request,user)
              
#             return redirect('user_home')

#         # elif user.is_active == False:
#         #     return render(request,'accounts/signin.html',{'err':"Temperorly Blocked"})   

#         else:

#             data = {'status': 'invalid'}
#             # return JsonResponse(data=data)
#             return render(request,'accounts/signin.html',{'err':"Invalid Username or Password"})   


       


class Login(View):
  
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('user_home')
        
        return render(request,'accounts/signin.html')

    def post(self,request):
        data=request.POST
        username=data["username"]
        password=data['password']
        user=authenticate(request,username=username,password=password)
        use=UserData.objects.get(username=username)
        if use.is_active == False:
            messages.info(request,"Your Account is Blocked")
            return redirect('login')
        print(user)
        if user is not None:

            try:
           
                cart=Cart.objects.get(cart_id=_cart_id(request))
                print(cart)
                is_cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                print(is_cart_item_exists)
                if is_cart_item_exists:
                    cart_item=CartItem.objects.filter(cart=cart)
                    print(cart_item)
                    for item in cart_item:
                        item.user=user
                        item.save()
            except:
                pass  

                 
                    
            login(request,user)
            
            url=request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                params=dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage=params['next']
                    return redirect(nextPage)
              
                
            except:
                return redirect('user_home')
                   

        # elif user.is_active == False:
        #     return render(request,'accounts/signin.html',{'err':"Temperorly Blocked"})   

        else:

            data = {'status': 'invalid'}
            # return JsonResponse(data=data)
            return render(request,'accounts/signin.html',{'err':"Invalid Username or Password"})   




def user_home(request):
    print(request.user)

    offer_pro=ProductOffer.objects.all()
    
    today = date.today()
    today1 = today.strftime("%Y-%m-%d")
    for offer in offer_pro:
        print(offer.offer_end)
        if str(offer.offer_end) < today1 :
            pro=Product_Table.objects.get(id=offer.product.id)
            pro.offer_price=None
            pro.save(update_fields=['offer_price'])
             
        else:
            pass     


            
    
    category=Category.objects.all()
    print(category)

    prod=Product_Table.objects.filter(category=1)
    product=Product_Table.objects.filter(category=2)
    cat=Category.objects.filter(id=1)
    # lap_offer=CategoryOffer.objects.get(category__name="Laptop")
    # mob_offer=CategoryOffer.objects.get(category__name="Mobile Phones")
    prod_offer=ProductOffer.objects.all()
    
    
    return render(request,'accounts/index.html',{'products':prod,'prod':product,'category':category,'prod_offer':prod_offer})  


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('user_home')         


# class Login(View):
#     def get(self, request):
#         # if request.user.is_authenticated:
#         #     return redirect('/home')
#         return render(request, 'signin.html', {})
    
#     def post(self,request):
#         data=request.POST
#         us=data["username"]
#         psw=data["password"]
          
#         user=authenticate(request,username=us,password=psw)
#         print(user)
#         if user is not None:
#             login(request,user)
#             # return render(request,'home.html',{'name':user})
#             return HttpResponse("success")

#                         # return redirect('/home')
#         else:
#              return render(request,'signin.html',{"error":"**Invalid user Name or Password"})       
# 
def admin_login(request):

    if request.session.has_key('admin'):
        return redirect('admin_home')
      

    if request.method=="POST":

        admin_name="admin"
        admin_password="12345"
        data=request.POST
        user=data["username"]
        passw=data["password"]    
        if admin_name ==  user and admin_password == passw:
            request.session['admin'] = True
            return redirect('admin_home')
            
        else:
            return render(request,'accounts/admin_login.html',{'err':"username or passwords is incorrec"})
    else:
        return redirect(request,'accounts/admin_login.html')         





class AdminLogin(View):
    def get(self,request):
        if is_logged_in(request):
             return redirect('admin_home')
            # return render(request,'admin/admin_home.html')
        # else:
        #     return render(request,'accounts/admin_login.html')
        return render(request,'accounts/admin_login.html')


    def post(self,request):
        admin_name="admin"
        admin_password="12345"
        data=request.POST
        user=data["username"]
        passw=data["password"]    
        if(admin_name ==  user and admin_password == passw):
            request.session['admin'] = True
            return redirect('admin_home') 
            
        else:
            return render(request,'accounts/admin_login.html',{'err':"invalid username or password"})
            # return redirect('admin_login')
       


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_home(request):
    if is_logged_in(request):
        order=OrderProduct.objects.all()
        new_users = UserData.objects.filter(date_joined__month=datetime.now().month).count()
        today_order=OrderProduct.objects.filter(created_at__day=datetime.now().day).count()
        print(new_users)
        pend=OrderProduct.objects.filter(status='Pending',user_cancelled=False).count()
        accept=OrderProduct.objects.filter(status='Accepted').count()
        print(accept)
        cancelled=OrderProduct.objects.filter(status='Cancelled').count()
        print(cancelled)
        deliver=OrderProduct.objects.filter(status='Delivered').count
        user_cancelled=OrderProduct.objects.filter(user_cancelled=True).count
        day1=datetime.now().day
        day2=day1-1
        day3=day2-1
        day4=day3-1
        day5=day4-1
        day6=day5-1
        day7=day6-1

        day1_order =OrderProduct.objects.filter(created_at__day=day1).count()
        day2_order =OrderProduct.objects.filter(created_at__day=day2).count()
        day3_order =OrderProduct.objects.filter(created_at__day=day3).count()
        day4_order =OrderProduct.objects.filter(created_at__day=day4).count()
        day5_order =OrderProduct.objects.filter(created_at__day=day5).count()
        day6_order =OrderProduct.objects.filter(created_at__day=day6).count()
        day7_order =OrderProduct.objects.filter(created_at__day=day7).count()
        print(day1)
        delivered=OrderProduct.objects.filter(status='Delivered')
        revenue=0
        for deliv in delivered:
            revenue+=deliv.product_price
        
        context={
            'new_user':new_users,
            'new_order':today_order,
            'order':order,
            'sales':order.count,
            'revenue':revenue,
            'pend':pend,
            'accept':accept,
            'cancel':cancelled,
            'delivered':deliver,
            'user_cancelled':user_cancelled,
            'day1':day1_order,'day2':day2_order,'day3':day3_order,'day4':day4_order,'day5':day5_order,'day6':day6_order,'day7':day7_order
        }
        return render(request,'admin/index.html',context)
    else:
        return redirect('admin_login') 


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
    #  if request.session.has_key('admin'):
        del request.session['admin']
        # request.session.flush()
        return redirect('admin_login')   

     


def product_details(request,slug):
        cat=Category.objects.all()

        # pro=Category.objects.get(slug='llaptop')
        # print(pro.name)
        # list_pro=Product_Table.objects.filter(category=pro.id)
        # print(list_pro)
        # offer=CategoryOffer.objects.get(category=slug)
        # print(offer.offer)



        #check user purchase this product,this is checked for submiting review

        if request.user.is_authenticated:

            try:
                orderproduct=OrderProduct.objects.filter(user=request.user,product__slug=slug).exists()
            except OrderProduct.DoesNotExist:
                orderproduct=None
        else:
            orderproduct=None        

        #get the review for displaying 

        review=ReviewRating.objects.filter(product__slug=slug,status=True)  
        count=0
        for i in review:
            count += 1 
        print(review)  

    
       
        
        if request.user.is_authenticated:

            product=Product_Table.objects.get(slug=slug)
            

            in_cart=CartItem.objects.filter(user=request.user,product=product).exists()

        else:    
           product=Product_Table.objects.get(slug=slug)
           in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()
        print(product.category.slug)
        
        return render(request,'accounts/product-detail.html',{'products':product,'in_cart':in_cart,'category':cat,'orderproduct':orderproduct,'review':review,'count':count})   


def product_store(request,slug):
    category=Category.objects.get(slug=slug)
    product=Product_Table.objects.filter(category=category)
    count=product.count()
    paginator=Paginator(product,3)
    page=request.GET.get('page')
    paged_product=paginator.get_page(page)
    cat=Category.objects.all()
    brand=Brand.objects.all()
    print(brand)

    

    
    
    print(count)
    return render(request,'accounts/store.html',{'products':paged_product,'count':count,'category':cat,'brand':brand})        
        


def check_user(request):
    if request.method == "GET":
        user=request.GET['username']
        if UserData.objects.filter(username=user).exists():
            return HttpResponse(" not available")
        else:
            return HttpResponse("available") 


def user_accounts(request):
    return render(request,'accounts/user_accounts.html')   


def user_profile(request):
    cat=Category.objects.all()
    data=UserData.objects.get(username=request.user)
    try:
        pro=UserPropic.objects.get(user=request.user)
        propic=pro.pro_pic
    except:
        propic='/pro_pics/avatar.jpg'

    try:
        referal=Referal.objects.get(user=request.user)   
    except Referal.DoesNotExist:
        referal=None


    try:
        coupen=ReferalCoupen.objects.filter(user=request.user)
    except ReferalCoupen.DoesNotExist:
        coupen=None        

      

    context={
        'user':data,
        'propic':propic,
        'category':cat,
        'referal':referal,
        'coupen':coupen
    }

    if request.method=='POST':
        email=request.POST['email']
        phone=request.POST['phone']
        data.email=email
        data.phone_number=phone
        
        data.save()
        return redirect('user_profile')
    return render(request,'accounts/user_profile.html',context)   



def user_propic(request):
    if request.method=='POST':
        # pic=request.FILES['pic']
        image=request.POST['pro_img1']
        format, img1 = image.split(';base64,')
        ext = format.split('/')[-1]
        img_data1 = ContentFile(base64.b64decode(img1), name="propic" + '1.' + ext)
        print(img_data1)
        if UserPropic.objects.filter(user=request.user).exists():
            propic=UserPropic.objects.get(user=request.user)
            propic.pro_pic=img_data1
            propic.save()
            print("saved")
        else:    
            propic=UserPropic(user=request.user,pro_pic=img_data1) 
            propic.save()
        return redirect('user_profile')

        


def user_address(request):

    addresses=UserAddress.objects.filter(user=request.user)
    if request.method=='POST':
        data=request.POST
        first_name=data['first_name']
        last_name=data['last_name']
        phone=data['phone']
        email=data['email']
        address_line1=data['address_line1']
        address_line2=data['address_line2']
        city=data['city']
        state=data['state']
        address=UserAddress(user=request.user,first_name=first_name,last_name=last_name,phone=phone,email=email,address_line1=address_line1,address_line2=address_line2,city=city,state=state)
        address.save()
        return redirect('user_address')

    context={'addresses':addresses}
    return render(request,'accounts/user_address.html',context)    



def edit_address(request,id):
    address=UserAddress.objects.get(id=id)
    if request.method=='POST':
        data=request.POST
        first_name=data['first_name']
        last_name=data['last_name']
        phone=data['phone']
        email=data['email']
        address_line1=data['address_line1']
        address_line2=data['address_line2']
        city=data['city']
        state=data['state']
        address.first_name=first_name
        address.last_name=last_name
        address.phone=phone
        address.email=email
        address.address_line1=address_line1
        address.address_line2=address_line2
        address.city=city
        address.state=state
        address.save()
        return redirect('user_address')
    context={'address':address}
    return render(request,'accounts/edit_address.html',context)    




def delete_address(request,id):
    UserAddress.objects.get(id=id).delete()
    return redirect('user_address')     


def user_order(request):
    order=OrderProduct.objects.filter(user=request.user)
    context={'order':order}
    return render(request,'accounts/user_order.html',context)   

def cancel_order(request,id):
    order=OrderProduct.objects.get(id=id)
    order.user_cancelled=True
    order.status="Cancelled"
    order.save()
    pro=order.product.id
    product=Product_Table.objects.get(id=pro)
    product.stock +=1
    product.save()
    return redirect('user_order')




def collect_address(request):
    if request.method == "GET":
        id=request.GET['address']
        print(id)
        add=UserAddress.objects.get(id=id)
        print(add.last_name)

        data = {}
        data['first_name']=add.first_name
        data['last_name']=add.last_name
        data['phone']=add.phone
        data['email']=add.email
        data['address1']=add.address_line1
        data['address2']=add.address_line2
        data['city']=add.city
        data['state']=add.state

        return HttpResponse(json.dumps(data), content_type="application/json")
        





def search_product(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        products=Product_Table.objects.order_by('id').filter(product_name__icontains=keyword)
        print(keyword)
        count=products.count

        context={'products':products,'count':count}

    return render(request,'accounts/store.html',context) 



def forgotpassword(request):
    if request.method == 'POST':
        email=request.POST['email']
        if UserData.objects.filter(email=email).exists():
            user=UserData.objects.get(email=email)
            current_site=get_current_site(request)
            mail_subject="Reset Your password"
            message=render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has been sent your email address')
            return redirect('login')

        else:
            messages.error(request,'Account Does not exists')
            return redirect('forgotpassword')
    return render(request,'accounts/forgotpassword.html')  


def reset_password_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=UserData._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,UserData.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid 
        messages.success(request,'Please Reset your Password') 
        return redirect('reset_password')
    else:
        messages.error(request,'This link has been expired') 
        return redirect('login') 



def reset_password(request):
    if request.method=='POST':
        create_password=request.POST['create_password']
        confirm_password=request.POST['confirm_password']
        if create_password == confirm_password:
            uid=request.session.get('uid')
            user=UserData.objects.get(pk=uid)
            user.set_password(create_password)
            user.save()
            messages.success(request,'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request,'Password is Not matching')
            return redirect('reset_password')
    else:        
        return render(request,'accounts/reset_password.html')



def login_otp(request):
    if request.method=='POST':
        phone=request.POST['phone']
        if UserData.objects.filter(phone_number=phone).exists():
            otp = random.randint(100000,999999)
            strotp=str(otp)
            account_sid ='AC44dd3466566f9fefe81146d0c3ac8805'
            auth_token ='b6a8da4bfb71d1c93567e3c68789b143'
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                     body="Your Elekso login OTP is"+strotp,
                     from_='+19412188661',
                     to='+91'+phone
                 )
            request.session['otp']=otp
            print(request.session['otp'])
            request.session['phone']=phone
            print(request.session['phone'])
            print(otp,phone)
            messages.success(request,"OTP Sended Successfully")
            return redirect('login_otp')  
        messages.error(request,"enter valid phone number")    
        return redirect('login_otp')    
             


    return render(request,'accounts/login_otp.html')




def verify_otp(request):
    if request.method=='POST':
        enter_otp=request.POST['otp']
        otp=int(enter_otp)
        if request.session.has_key('otp'):
            sended_otp=request.session['otp']
            print(type(sended_otp))
            
            if sended_otp == otp :
                print("in if")
                phone=request.session['phone']
                print(phone)
                user=UserData.objects.get(phone_number=phone)
                login(request,user)
                del request.session['otp']
                del request.session['phone']
                
                return redirect('user_home')
            else:    
                messages.error(request,"entered OTP is wrong")
                return redirect('login_otp') 
        else:
            return redirect('login_otp')          
    return render(request,'accounts/otp_verify.html')




def filter_brand(request,brand):
  
    products=Product_Table.objects.order_by('id').filter(brand__brand=brand)
    
    count=products.count

    context={'products':products,'count':count}

    return render(request,'accounts/store.html',context)     


def submit_review(request,id):  
    url=request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            review=ReviewRating.objects.get(user__id=request.user.id,product__id=id)
            form=ReviewForm(request.POST,instance=review)
            form.save()
            messages.success(request,'Your Review has been updated')
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form=ReviewForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.rating=form.cleaned_data['rating']
                data.review=form.cleaned_data['review']
                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=id
                data.user_id=request.user.id
                data.save()
                messages.success(request,'Your Review has been submitted')
                return redirect(url)





def check_referal(request):
    if request.method == "GET":
        referal=request.GET['referal']
        if Referal.objects.filter(code=referal).exists():
            return HttpResponse("available")
        else:
            return HttpResponse("not available")            



def verify_coupen(request):
    if request.method=='POST':
        coupen=request.POST['coupen']
        if ReferalCoupen.objects.filter(coupen_code=coupen).exists():
            cartitem=CartItem.objects.filter(user=request.user)
            print(cartitem)
            for pro in cartitem:
                if pro.product.offer_price == None:
                    
                    price=pro.product.price*(20/100)
                    pro.product.offer_price=pro.product.price-price
                    pro.product.save()
                else:
                    price=pro.product.offer_price*(20/100)  
                    pro.product.offer_price=pro.product.offer_price-price
                    pro.product.save()
            referal=ReferalCoupen.objects.get(coupen_code=coupen) 
            referal.delete()       
            messages.success(request,'your reference coupen is applied')
            return redirect('payments')
        elif NormalCoupen.objects.filter(coupen_code=coupen).exists():
            coupen_obj=NormalCoupen.objects.get(coupen_code=coupen)
            if UsedOffer.objects.filter(coupen=coupen_obj,user=request.user).exists():
                messages.error(request,'you already used this coupen')  
                return redirect('payments') 
            else:
                coupen_obj=NormalCoupen.objects.get(coupen_code=coupen)
                cartitem=CartItem.objects.filter(user=request.user)
                for pro in cartitem:
                    if pro.product.offer_price == None:
                        
                        price=pro.product.price*(int(coupen_obj.coupen_offer)/100)
                        pro.product.offer_price=pro.product.price-price
                        pro.product.save()
                    else:
                        price=pro.product.offer_price*(int(coupen_obj.coupen_offer)/100)  
                        pro.product.offer_price=pro.product.offer_price-price
                        pro.product.save()
                used_offer=UsedOffer(coupen=coupen_obj,user=request.user)
                used_offer.save()
                messages.success(request,'your coupen is applied')
                return redirect('payments') 
                     

        else:
            messages.error(request,'coupen is invalid ')
            return redirect('payments')


                


        







            

