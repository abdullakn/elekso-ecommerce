from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .models import *
from accounts.models import *
from django.contrib.auth import authenticate,login,logout
from .forms import AddProductForm
from django.views.decorators.cache import cache_control

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

class AddCategory(View):
    def get(self,request):
        if request.session.has_key('admin'):
            return render(request,'admin/add_category.html')
        else:    
            return redirect('admin_login')    

    def post(self,request):
        data=request.POST    
        category=data['category']
        slug=data['slug']
        Category.objects.create(name=category,slug=slug)
        return redirect('admin_home')



class AddBrand(View):
    def get(self,request):
         if request.session.has_key('admin'):
            category=Category.objects.all()
            return render(request,'admin/add_brand.html',{'categories':category}) 
         return redirect('admin_login')       


    def post(self,request):
        data=request.POST
        category=data['category']

        brand=data['brand']  
        category_obj=Category.objects.get(id=category)
        print(category_obj)
        b=Brand(category=category_obj,brand=brand)
        b.save()   
        return redirect('admin_home')
        
      

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_product(request):
    form = AddProductForm()
    # print(form.as_p())
    if request.method == 'POST':
        form = AddProductForm(request.POST,request.FILES)
        if form.is_valid():
            cat=form.cleaned_data['category']
            brand=form.cleaned_data['brand']
            product_name=form.cleaned_data['product_name']
            price=form.cleaned_data['price']
            stock=form.cleaned_data['stock']
            description=form.cleaned_data['description']
            ram=form.cleaned_data['ram']
            storage=form.cleaned_data['storage']
            processor=form.cleaned_data['processor']
            screen_size=form.cleaned_data['screen_size']
            color=form.cleaned_data['color']
            slug=form.cleaned_data['slug']
            image1=form.cleaned_data['image1']
            image2=form.cleaned_data['image2']
            image3=form.cleaned_data['image3']
            image4=form.cleaned_data['image4']
            product=Product_Table(category=cat,brand=brand,product_name=product_name,price=price,stock=stock,description=description,processor=processor,ram=ram,storage=storage,screen_size=screen_size,color=color,slug=slug,image1=image1,image2=image2,image3=image3,image4=image4)

            product.save()
            print(form.data['price'])
            # print(form.data['image1'])
            category=form.data['category']
            item=Category.objects.get(id=category)
            print(item.name)
            print(product.id)
           
           

           
            return redirect('view_products')
    if request.session.has_key('admin'):        
        return render(request, 'admin/add_products.html', {'form': form})
    return redirect('admin_login')    


# class Add_Product(View):
#     def get(self,request):
#         form = AddProductForm()
#         return render(request, 'admin/add_products.html', {'form': form})

#     def post(self, request):
#         form = AddProductForm(request.POST)

#         if form.is_valid():
#             name = myform.cleaned_data['name']
#             email = myform.cleaned_data['email']
#             password = myform.cleaned_data['password']
#             s1 = Registration(name=name, email=email, password=password)
#             s1.save()
#             return HttpResponse("successfully Registered")




def load_brand(request):
    category_id = request.GET.get('category_id')
    brands = Brand.objects.filter(category_id=category_id).all()
    return render(request, 'admin/brand_dropdown_list.html', {'brands': brands})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)



class User_Management(View):
    def get(self,request):
        users=UserData.objects.all().order_by('id')

        if request.session.has_key('admin'):
        
       
            return render(request,'admin/user_mangement.html',{'users':users})
        return redirect('admin_login')    



# class User_Management(View):
#     def get(self,request):
#         users=UserData.objects.all().order_by('id')

#         if request.session.has_key('admin'):
        
       
#             return render(request,'admin/user_mangement.html',{'users':users})
#         return redirect('admin_login') 


def user_block(request,id):
    user=UserData.objects.get(id=id)
    user.is_active=False
    user.save()   
    return redirect('user_management')   


def user_unblock(request,id):
    user=UserData.objects.get(id=id)
    user.is_active=True
    user.save()   
    return redirect('user_management')    



class ViewProducts(View):
    def get(self,request):
        if request.session.has_key('admin'):
            products=Product_Table.objects.all()
            return render(request,'admin/view_products.html',{'products':products})
            
        return redirect('admin_login')    



def edit_products(request,slug):
    product=Product_Table.objects.get(slug=slug)
    form=AddProductForm(instance=product)
    if request.method == "POST":
        form=AddProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('view_products')

    return render(request,'admin/edit_products.html',{'form':form})



def delete_user(request,id):
    UserData.objects.get(id=id).delete()
    return redirect('user_management') 


def delete_products(request,id):
    Product_Table.objects.get(id=id).delete()
    return redirect('view_products')
           













   
                  
        
