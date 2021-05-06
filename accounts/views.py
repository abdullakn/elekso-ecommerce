from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .models import *
from products.models import *
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from  django.contrib.sessions.models import Session
from django.views.decorators.cache import cache_control

# Create your views here.


def sample_view(request):
    return render(request,'accounts/signin.html')

def register(request):
    return render(request,'accounts/register.html')

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
       if password != confirm :
           return render(request,'accounts/register.html',{'err':"Password are not same"})
       else:    
            user_data=UserData.objects.create_user(username=username,email=email,phone_number=phone_number,password=password)
            user_data.save()
            

            user=authenticate(request,username=username,password=password)
            if user is not None:
                    login(request,user)
                    
                    return redirect('user_home')
                    
       


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
        print(user.is_active)
        print('abdu')
        if user is not None:
            login(request,user)
            # data = {'status': 'valid'}
            # return JsonResponse(data=data)
            # return register(request,'index.html')   
            return redirect('user_home')

        # elif user.is_active == False:
        #     return render(request,'accounts/signin.html',{'err':"Temperorly Blocked"})   

        else:

            data = {'status': 'invalid'}
            # return JsonResponse(data=data)
            return render(request,'accounts/signin.html',{'err':"Invalid Username or Password"})   




def user_home(request):
    prod=Product_Table.objects.filter(category=1)
    product=Product_Table.objects.filter(category=2)
    # print(prod1)
    
    # Product_Table.objects.all()
    
    
    return render(request,'accounts/index.html',{'products':prod,'prod':product})  


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
      

    elif request.method=="POST":

        admin_name="admin"
        admin_password="12345"
        data=request.POST
        user=data["username"]
        passw=data["password"]    
        if admin_name ==  user and admin_password == passw:
            request.session['admin'] = True
            return redirect('admin_home')
            
        else:
            return render(request,'accounts/admin_login.html')
    else:
        return redirect(request,'accounts/admin_login.html')         





class AdminLogin(View):
    def get(self,request):
        if request.session.has_key('admin'):
           return redirect('admin_home')
        else:
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
            return render(request,'admin/index.html')
       


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_home(request):
    if request.session.has_key('admin'):
        return render(request,'admin/index.html')
    else:
        return redirect('admin_login') 


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
    #  if request.session.has_key('admin'):
        del request.session['admin']
        # request.session.flush()
        return redirect('admin_login')   

     


def product_details(request,slug):
    

        pro=Category.objects.get(slug='llaptop')
        print(pro.name)
        list_pro=Product_Table.objects.filter(category=pro.id)
        print(list_pro)
        product=Product_Table.objects.get(slug=slug)
        print(product.category.slug)
        return render(request,'accounts/product-detail.html',{'products':product})   


def product_store(request,id):
    product=Product_Table.objects.get(id=id)
    print(product.category.slug)
    return render(request,'accounts/store.html')        
        


def check_user(request):
    if request.method == "GET":
        user=request.GET['username']
        if UserData.objects.filter(username=user).exists():
            return HttpResponse(" not available")
        else:
            return HttpResponse("available") 
               

            

