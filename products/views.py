from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .models import *
from accounts.models import *
from django.contrib.auth import authenticate,login,logout
from .forms import AddProductForm, OfferForm
from django.views.decorators.cache import cache_control

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from order.models import OrderProduct
from  accounts.decorator import login_required
from accounts.utils import is_logged_in
from django.core.files.base import ContentFile
import base64


from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.

# class AddCategory(View):
#     def get(self,request):
#         if request.session.has_key('admin'):
#             return render(request,'admin/add_category.html')
          
#         return redirect('admin_login')    

#     def post(self,request):
#         data=request.POST    
#         category=data['category']
#         slug=data['slug']
#         Category.objects.create(name=category,slug=slug)
#         return redirect('admin_home')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_category(request):
    if request.method=='POST':
        data=request.POST    
        category=data['category']
        slug=data['slug']
        Category.objects.create(name=category,slug=slug)
        return redirect('admin_home')
    else:
        if is_logged_in(request):
            return render(request,'admin/add_category.html')
          
        return redirect('admin_login')   

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_brand(request):
    if request.method=='POST':
        data=request.POST
        category=data['category']

        brand=data['brand']  
        category_obj=Category.objects.get(id=category)
        print(category_obj)
        b=Brand(category=category_obj,brand=brand)
        b.save()   
        return redirect('admin_home')

    else:
        if is_logged_in(request):
            category=Category.objects.all()
            return render(request,'admin/add_brand.html',{'categories':category}) 
        return redirect('admin_login')


def edit_category(request,id):
    cat=Category.objects.get(id=id)
    if request.method=="POST":
        category=request.POST['category']
        cat.name=category
        cat.save()
        return redirect('view_category')


def delete_category(request,id):
    Category.objects.get(id=id).delete() 
    return redirect('view_category')       





# class AddBrand(View):
#     def get(self,request):
#          if request.session.has_key('admin'):
#             category=Category.objects.all()
#             return render(request,'admin/add_brand.html',{'categories':category}) 
#          return redirect('admin_login')       


#     def post(self,request):
#         data=request.POST
#         category=data['category']

#         brand=data['brand']  
#         category_obj=Category.objects.get(id=category)
#         print(category_obj)
#         b=Brand(category=category_obj,brand=brand)
#         b.save()   
#         return redirect('admin_home')
        
def view_category(request):
    cat=Category.objects.all()
    brand=Brand.objects.all()
    context={
        'cat':cat,
        'brand':brand
    }
    return render(request,'admin/view_category.html',context)      

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
            image1 = request.POST['pro_img1']
            image2 = request.POST['pro_img2']
            image3 = request.POST['pro_img3']
            image4 = request.POST['pro_img4']

            format, img1 = image1.split(';base64,')
            ext = format.split('/')[-1]
            img_data1 = ContentFile(base64.b64decode(img1), name=product_name + '1.' + ext)
            format, img2 = image2.split(';base64,')
            ext = format.split('/')[-1]
            img_data2 = ContentFile(base64.b64decode(img2), name=product_name + '2.' + ext)
            format, img3 = image3.split(';base64,')
            ext = format.split('/')[-1]
            img_data3 = ContentFile(base64.b64decode(img3), name=product_name + '3.' + ext)
            format, img4 = image4.split(';base64,')
            ext = format.split('/')[-1]
            img_data4 = ContentFile(base64.b64decode(img4), name=product_name + '4.' + ext)
            
            product=Product_Table(category=cat,brand=brand,product_name=product_name,price=price,stock=stock,description=description,processor=processor,ram=ram,storage=storage,screen_size=screen_size,color=color,slug=slug,image1=img_data1,image2=img_data2,image3=img_data3,image4=img_data4)
            product.save()
            print(form.data['price'])
            # print(form.data['image1'])
            category=form.data['category']
            item=Category.objects.get(id=category)
            print(item.name)
            print(product.id)
           
           

           
            return redirect('view_products')
    if is_logged_in(request):        
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



# class User_Management(View):
#     def get(self,request):
       

#         if request.session.has_key('admin'):
        
       
#             return render(request,'admin/user_mangement.html',{'users':users})
#         return redirect('admin_login')    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_management(request):
    user=UserData.objects.all().order_by('id')
    paginator=Paginator(user,8)
    page=request.GET.get('page')
    paged_user=paginator.get_page(page)
    if request.session.has_key('admin'):
         
         return render(request,'admin/user_mangement.html',{'users':paged_user})
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



# class ViewProducts(View):
#     def get(self,request):
#         if request.session.has_key('admin'):
#             products=Product_Table.objects.all()

#             paginator=Paginator(products,7)
#             page=request.GET.get('page')
#             paged_product=paginator.get_page(page)
#             return render(request,'admin/view_products.html',{'products':paged_product})
            
#         return redirect('admin_login')    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_products(request):  
    if request.session.has_key('admin'):
        product=Product_Table.objects.all()

        paginator=Paginator(product,5)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
        return render(request,'admin/view_products.html',{'products':paged_product})      

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



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_order(request):
    if request.session.has_key('admin'): 

        order=OrderProduct.objects.all().order_by('id')
        paginator=Paginator(order,8)
        page=request.GET.get('page')
        paged_order=paginator.get_page(page)

        context={'orders':paged_order}

        return render(request,'admin/view_order.html',context)   

    return redirect('admin_login')      

def edit_order_status(request,id):
    order=OrderProduct.objects.get(id=id)
    context={'order':order}

    if request.method== 'POST':
        status=request.POST['status']
        order.status=status
        order.save()
        return redirect('view_order')
    return render(request,'admin/edit_order_status.html',context)     



def view_detailed_order(request,id):
    order=OrderProduct.objects.get(id=id)
    context={'order':order}
    return render(request,'admin/view_order_detailed.html',context)  



def monthly_report(request):
    if request.method == 'POST':
        month = request.POST['month']
        x=[]
        x = month.split("-")
        mo=int(x[1])
        deliver=OrderProduct.objects.filter(status='Delivered',created_at__month=mo)
        total=0
        for delive in deliver:
            total+=delive.product_price
        context={
            'ordered':deliver,
            'total':total
        }
        
        return render(request,'admin/monthly_report.html',context)
    total_order=OrderProduct.objects.filter(status='Delivered') 
    total=0 
    for delive in total_order:
            total+=delive.product_price
    context={
            'ordered':total_order,
             'total':total
        }
         
    return render(request,'admin/monthly_report.html',context)  



def yearly_report(request):
    if request.method=='GET':
        year=request.GET['year']
        total_order=OrderProduct.objects.filter(created_at__year=year,status='Delivered')
        total=0
        for delive in total_order:
            total+=delive.product_price
        context={
            'ordered':total_order,
             'total':total
        }
        return render(request,'admin/monthly_report.html',context)     



def datewise_report(request):
    if request.method=="GET":
        start=request.GET['start']           
        end=request.GET['end']   
        total_order=OrderProduct.objects.filter(created_at__range=[start,end],status='Delivered')
        print(total_order)
        print(start,end) 
        total=0
        for delive in total_order:
            total+=delive.product_price
        context={
            'ordered':total_order,
             'total':total
        }

        return render(request,'admin/monthly_report.html',context)     



def add_offer(request):
    product=Product_Table.objects.all()
    context={'product':product}
    
    return render(request,'admin/add_offer.html',context)  


def category_offer(request):
    if request.method=='POST':
        cat=request.POST['category']
        offer=request.POST['offer']
        start=request.POST['start']
        end=request.POST['end']
        category=Category.objects.get(name=cat)
        if CategoryOffer.objects.filter(category__name=category).exists():
            cats=CategoryOffer.objects.get(category=category)
            cats.category=category
            cats.offer=offer
            cats.offer_start=start
            cats.offer_end=end
            cats.save()
            print("saved")
        else:    
            category=CategoryOffer(category=category,offer=offer,offer_start=start,offer_end=end) 
            category.save()

        product=Product_Table.objects.filter(category=category.id)
        for pro in product:
            pro.offer_price=(pro.price/100)*int(offer)
            pro.offer_percentage=offer        
            pro.save(update_fields=['offer_price','offer_percentage'])
            
            
            
        return redirect('admin_home')



def product_offer(request):
    if request.method == 'POST':
        prod=int(request.POST['product'])
        offer=request.POST['offer']
        start=request.POST['start']
        end=request.POST['end']
        print(prod,offer,start,end)
        product=Product_Table.objects.get(id=prod)
        print(product)
        
        if ProductOffer.objects.filter(product__id=prod).exists():
            pro=ProductOffer.objects.get(product=prod)
            print(pro)
            pro.product=product
            pro.offer=offer
            pro.offer_start=start
            pro.offer_end=end
            pro.save()
            print("saved")
        else: 
            product=ProductOffer(product=product,offer=offer,offer_start=start,offer_end=end)   
            product.save()

        prod=Product_Table.objects.get(id=prod) 
        print(prod)
        prod.offer_price=(prod.price/100)*int(offer)
        prod.offer_percentage=offer 
        prod.save()
        return redirect('admin_home')       



def view_offer(request):
    pro_off=ProductOffer.objects.all()
    cat_off=CategoryOffer.objects.all()
    context={
        'pro_off':pro_off,
        'cat_off':cat_off
    }
    return render(request,'admin/viewoffer.html',context)   


def delete_cat_offer(request,id):
    offer=CategoryOffer.objects.get(id=id)
    print(offer)
    pro=Product_Table.objects.filter(category=offer.category)
    for pro in pro:
        pro.offer_price=None
        pro.offer_percentage=None
        pro.save(update_fields=['offer_price','offer_percentage'])
    offer.delete()    
        
    return redirect('view_offer')



def delete_pro_offer(request,id):
    offer=ProductOffer.objects.get(id=id)
    print(offer)
    pro=Product_Table.objects.get(product_name=offer.product)
    print(pro)
    pro.offer_price=None
    pro.offer_percentage=None
    pro.save()
    offer.delete()  
    return redirect('view_offer') 


def review_rating_view(request):
    review=ReviewRating.objects.all().order_by('id')
    paginator=Paginator(review,3)
    page=request.GET.get('page')
    page_review=paginator.get_page(page)
    context={
        'review':page_review
    }
    return render(request,'admin/view_review.html',context)   




def review_block(request,id):
    review=ReviewRating.objects.get(id=id)
    review.status=False
    review.save()   
    return redirect('view_review')   


def review_unblock(request,id):
    review=ReviewRating.objects.get(id=id)
    review.status=True
    review.save()   
    return redirect('view_review')   

def add_coupen(request):
    if request.method=='POST':
        title=request.POST['coupen_title']
        code=request.POST['code']
        offer=request.POST['offer']
        print(title,code,offer)
        coupen=NormalCoupen(coupen_title=title,coupen_code=code,coupen_offer=offer)
        coupen.save()
        return redirect('admin_home')
    return render(request,'admin/add_coupen.html')      



  



    


           













   
                  
        
