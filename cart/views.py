from django.http.response import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from products.models import Product_Table
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import UserAddress
from django.http import JsonResponse
import json


# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

# def add_cart(request,product_id):
#     product=Product_Table.objects.get(id=product_id)    
#     try:
#         cart=Cart.objects.get(cart_id=_cart_id(request))
#     except Cart.DoesNotExist:
#         cart=Cart.objects.create(cart_id=_cart_id(request))  

#     cart.save()  

#     try:
#         cart_item=CartItem.objects.get(product=product,cart=cart)  
#         cart_item.quantity +=1
#         cart_item.save()
#     except CartItem.DoesNotExist:
#         cart_item=CartItem.objects.create(product=product,quantity=1,cart=cart) 
#         cart_item.save()  
#         print(cart_item.product)

#     return redirect('cart')    


# def add_cart(request,product_id):
#     product=Product_Table.objects.get(id=product_id)
#     if request.user.is_authenticated:

#         is_cart_item_exists=CartItem.objects.filter(product=product,user=request.user).exists()

#         if is_cart_item_exists:
#             cart_item=CartItem.objects.get(product=product,user=request.user)
#             cart_item.quantity+=1
#             cart_item.save()
#         else:
#             cart_item=CartItem.objects.create(product=product,quantity=1,user=request.user) 
#             cart_item.save()   

        

#         return redirect('cart') 



#     else:


        


#         try:
#             cart=Cart.objects.get(cart_id=_cart_id(request))
#         except Cart.DoesNotExist:
#             cart=Cart.objects.create(cart_id=_cart_id(request))  

#         cart.save()  

#         is_cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()

#         if is_cart_item_exists:
#             cart_item=CartItem.objects.get(product=product,cart=cart)
#             cart_item.quantity+=1
#             cart_item.save()
#         else:
#             cart_item=CartItem.objects.create(product=product,quantity=1,cart=cart) 
#             cart_item.save()   

        

#         return redirect('cart') 

        



def add_cart(request, product_id):
    current_user = request.user
    product = Product_Table.objects.get(id = product_id)
    if current_user.is_authenticated:

        is_cart_item_exists = CartItem.objects.filter(product = product, user = current_user).exists()
        if is_cart_item_exists:

            cart_item= CartItem.objects.filter(product= product, user= current_user)
        try:
            cart_item= CartItem.objects.get(product= product, user= current_user)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user 
            )
            cart_item.save()
        return redirect('cart')

    else:
        try:
            cart = Cart.objects.get(cart_id= _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id= _cart_id(request))
        cart.save()
        try:
            cart_item= CartItem.objects.get(product= product, cart= cart)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )
            cart_item.save()
        return redirect('cart')




def remove_cart(request,product_id):    
    

#     product = get_object_or_404(Product_Table, id = product_id)
#     try:
#         if request.user.is_authenticated:

#             cart_item = CartItem.objects.get(product = product, user=request.user)
#         else:
#             cart = Cart.objects.get(cart_id = _cart_id(request))    
#             cart_item = CartItem.objects.get(product = product, cart=cart)
#         if cart_item.quantity >1:
#             cart_item.quantity -= 1
#             cart_item.save()
#         else:
#             cart_item.delete()
#     except:
#         pass
#     return redirect('cart')


    # cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product_Table,id=product_id)
    try:
        if request.user.is_authenticated:

           cart_item=CartItem.objects.get(product=product,user=request.user)
        else:  
           cart=Cart.objects.get(cart_id=_cart_id(request)) 
           cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity > 1:
           cart_item.quantity -= 1
           cart_item.save()
        else:
           cart_item.delete()
    except:
        pass       
    return redirect('cart') 



def remove_cart_item(request,product_id): 
    # cart=Cart.objects.get(cart_id=_cart_id(request))
    # product=get_object_or_404(Product_Table,id=product_id)
    # cart_item=CartItem.objects.get(product=product,cart=cart)  
    # cart_item.delete()
    # return redirect('cart')  
    # 
    product = get_object_or_404(Product_Table, id = product_id)

    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product = product ,user = request.user)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product = product,cart=cart)

    cart_item.delete()
    return redirect('cart')  






def cart(request,total=0,quantity=0,cart_items=None):
    tax=0
    grand_total=0
    try:
        if request.user.is_authenticated:
            print(request.user)
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:    
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            if cart_item.product.offer_price == None:
                total += (cart_item.product.price * cart_item.quantity)
            else:
                total += (cart_item.product.offer_price * cart_item.quantity)
            quantity += cart_item.quantity
            tax = total*(18/100)
            grand_total= tax+total
    except ObjectDoesNotExist:
        pass

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    return render(request,'accounts/cart.html',context)


@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):

    

    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:    
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            # tax = 450
            # grand_total= tax+total
    except ObjectDoesNotExist:
        pass

    addresses=UserAddress.objects.filter(user=request.user)

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'addresses':addresses,
        
        # 'grand_total':grand_total
    }
    return render(request,'accounts/checkout.html',context)    




def add_cart_ajax(request):
    product_id = int(request.POST['product_id'])
    print(product_id)
    total=0
    tax=0
    grand_total=0
    product=Product_Table.objects.get(id=product_id)
    print(product)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product=product,user=request.user)
        cart_item.quantity+=1
        cart_item.save()
        sub_total=cart_item.sub_total()
        cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        for cart_item in cart_items:
            if cart_item.product.offer_price == None:
                total += (cart_item.product.price * cart_item.quantity)
            else:
                total += (cart_item.product.offer_price * cart_item.quantity)
        tax = total*(18/100)
        grand_total= tax+total        
        data={'id': product_id,'quantity':cart_item.quantity,'sub_total':sub_total,'total':total,'tax':tax,'grand_total':grand_total}
        
        return JsonResponse(data=data)
    # return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        try:
            cart = Cart.objects.get(cart_id= _cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id= _cart_id(request))
        cart.save()
        try:
            cart_item= CartItem.objects.get(product= product, cart= cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )
            cart_item.save()
        sub_total=cart_item.sub_total()
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            if cart_item.product.offer_price == None:
                total += (cart_item.product.price * cart_item.quantity)
            else:
                total += (cart_item.product.offer_price * cart_item.quantity)
        tax = total*(18/100)
        grand_total= tax+total        
        data={'id': product_id,'quantity':cart_item.quantity,'sub_total':sub_total,'total':total,'tax':tax,'grand_total':grand_total}
        
        return JsonResponse(data=data)    








def remove_cart_ajax(request):  
    product_id = int(request.POST['product_id'])
    print(product_id)
    total=0
    tax=0
    grand_total=0
    product=Product_Table.objects.get(id=product_id)
    print(product)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product=product,user=request.user)
        # if cart_item.quantity<=0:
        #     cart_item.delete()
        # else:  
        if cart_item.quantity >= 1:
            if cart_item.quantity == 1:     
                cart_item.delete()
            else:
                cart_item.quantity-=1
                cart_item.save()   
            
        # if cart_item.quantity < 1:
        #     cart_item.quantity=0
        #     cart_item.delete()  
        # cart_item.quantity-=1
        # cart_item.save()
        sub_total=cart_item.sub_total()
        cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        for cart_item in cart_items:
            if cart_item.product.offer_price == None:
                total += (cart_item.product.price * cart_item.quantity)
            else:
                total += (cart_item.product.offer_price * cart_item.quantity)
        tax = total*(18/100)
        grand_total= tax+total        
        data={'id': product_id,'quantity':cart_item.quantity,'sub_total':sub_total,'total':total,'tax':tax,'grand_total':grand_total}
        
        return JsonResponse(data=data) 


    else:
        cart=Cart.objects.get(cart_id=_cart_id(request)) 
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity > 1:
           cart_item.quantity -= 1
           cart_item.save()
        else:
           cart_item.delete()

        sub_total=cart_item.sub_total()
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            if cart_item.product.offer_price == None:
                total += (cart_item.product.price * cart_item.quantity)
            else:
                total += (cart_item.product.offer_price * cart_item.quantity)
        tax = total*(18/100)
        grand_total= tax+total        
        data={'id': product_id,'quantity':cart_item.quantity,'sub_total':sub_total,'total':total,'tax':tax,'grand_total':grand_total}
        
        return JsonResponse(data=data) 
   
        





