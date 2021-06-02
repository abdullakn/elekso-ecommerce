from accounts.models import UserAddress
import json
from django.contrib import auth
from django.shortcuts import render,redirect
from cart.models import CartItem
from .forms import OrderForm,Order
import datetime
from django.http import HttpResponse,JsonResponse

from .models import Payment,OrderProduct
from products.models import Product_Table
import json
import razorpay


def razorpay(request):
    order_id=val()
    print(order_id)
    order_data=Order.objects.get(user=request.user,is_ordered=False,order_number=order_id)
    cart_items=CartItem.objects.filter(user=request.user)
    grand_total=0
    tax=0
    total=0
    for cart_item in cart_items:
        total+=(cart_item.product.price * cart_item.quantity) 
    tax = (2*total)/100
    grand_total= total+tax 
    payment=Payment(user=request.user,payment_id=order_id,payment_method="razorpay",amount_paid=grand_total,satus="completed")
    payment.save()
    order_data.payment=payment
    order_data.is_ordered=True
    order_data.save()
    
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order=order_data
        orderproduct.user=request.user
        orderproduct.payment=payment
        orderproduct.product=item.product
        orderproduct.quantity=item.quantity
        if item.product.offer_price == None:
            orderproduct.product_price=item.product.price
        else:
            orderproduct.product_price=item.product.offer_price

        
        
        orderproduct.ordered=True
        orderproduct.save()
        product=Product_Table.objects.get(id=item.product_id)
            
        print(product)
        product.stock -= item.quantity
        product.save()

    # CartItem.objects.filter(user=request.user).delete()   
    cart_prod=CartItem.objects.filter(user=request.user)
    for cart_pro in cart_prod:
        if cart_pro.product.offer_price == None:
            pass
        else:
            if cart_pro.product.offer_percentage == None:
                pass
            else:
                price=cart_pro.product.price
                print(price)
                offer=int(cart_pro.product.offer_percentage)
                print("offer",offer)
                percentage_price=price*(offer/100)
                print(percentage_price)
                cart_pro.product.offer_price = percentage_price
                cart_pro.product.save()
    cart_prod.delete()     

    return redirect('invoice')
  



def payments(request,total=0,quantity=0):
    # order_id=request.session['order_id']
    order_id=val()
    print(order_id)
    order_data=Order.objects.get(user=request.user,is_ordered=False,order_number=order_id)
    cart_items=CartItem.objects.filter(user=request.user)
    grand_total=0
    tax=0
    for cart_item in cart_items:
        if cart_item.product.offer_price == None:
            total+=(cart_item.product.price * cart_item.quantity) 
        else:
            total+=(cart_item.product.offer_price * cart_item.quantity) 

    tax = (2*total)/100
    grand_total= total+tax 
    

    if request.method== 'POST':
        pay=request.POST['payment']
        if pay== "cod":
            payment=Payment(user=request.user,payment_id=order_id,payment_method=pay,satus="completed")
            payment.save()
            order_data.payment=payment
            order_data.is_ordered=True
            order_data.save()

            for item in cart_items:
                orderproduct=OrderProduct()
                orderproduct.order=order_data
                orderproduct.user=request.user
                orderproduct.payment=payment
                orderproduct.product=item.product
                orderproduct.quantity=item.quantity
                if item.product.offer_price == None:
                    orderproduct.product_price=item.product.price
                else:
                    orderproduct.product_price=item.product.offer_price

                
                orderproduct.ordered=True
                orderproduct.save()


                #reduce the quantity

                product=Product_Table.objects.get(id=item.product_id)
                
                print(product)
                product.stock -= item.quantity
                product.save()

            # CartItem.objects.filter(user=request.user).delete() 
            cart_prod=CartItem.objects.filter(user=request.user)
            for cart_pro in cart_prod:
                if cart_pro.product.offer_price == None:
                    pass
                else:
                    if cart_pro.product.offer_percentage == None:
                        pass
                    else:
                        price=cart_pro.product.price
                        print(price)
                        offer=int(cart_pro.product.offer_percentage)
                        print("offer",offer)
                        percentage_price=price*(offer/100)
                        print(percentage_price)
                        cart_pro.product.offer_price = percentage_price
                        cart_pro.product.save()
            cart_prod.delete()            

            return redirect('invoice')



              
            
        else:
            context={'grand_total':grand_total,'order_id':order_id}
            return render(request,'accounts/payment_option.html',context)   
        return HttpResponse("success")



    context={
            'order':order_data,
            'cart_items':cart_items,
            'total':total,
            'tax':tax,
            'grand_total':grand_total,
            'order_id':order_id
          
        }
    
    return render(request,'accounts/payments.html',context)


def pay_option(request):
    body=json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    print(body)
    payment=Payment(user=request.user,payment_id=body['trans_ID'],payment_method=body['payment_method'],amount_paid=order.order_total,satus=body['status'])
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()
    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct=OrderProduct()
        orderproduct.order=order
        orderproduct.user=request.user
        orderproduct.payment=payment
        orderproduct.product=item.product
        orderproduct.quantity=item.quantity
        if item.product.offer_price == None:
            orderproduct.product_price=item.product.price
        else:
            orderproduct.product_price=item.product.offer_price

        orderproduct.ordered=True
        orderproduct.save()
        product=Product_Table.objects.get(id=item.product_id)        
        print(product)
        product.stock -= item.quantity
        product.save()
    # CartItem.objects.filter(user=request.user).delete() 
    cart_prod=CartItem.objects.filter(user=request.user)
    for cart_pro in cart_prod:
        if cart_pro.product.offer_price == None:
            pass
        else:
            if cart_pro.product.offer_percentage == None:
                pass
            else:
                price=cart_pro.product.price
                print(price)
                offer=int(cart_pro.product.offer_percentage)
                print("offer",offer)
                percentage_price=price*(offer/100)
                print(percentage_price)
                cart_pro.product.offer_price = percentage_price
                cart_pro.product.save()
    cart_prod.delete()     

    data={
        'order_number':order.order_number,
        'transID':payment.payment_id
    }   

    return JsonResponse(data)





    


def place_order(request,total=0,quantity=0):
    cart_items=CartItem.objects.filter(user=request.user)
    print(cart_items)
    cart_count=cart_items.count()
    if cart_count < 0 :
        return redirect('user_home')

    grand_total=0
    tax=0
    for cart_item in cart_items:
        if cart_item.product.offer_price == None:
            total+=(cart_item.product.price * cart_item.quantity) 
        else:
            total+=(cart_item.product.offer_price * cart_item.quantity) 

    tax = (2*total)/100
    grand_total= total+tax  
    print(grand_total)     

    if request.method == 'POST':
        data=request.POST
        order=Order()
        
    
        order.first_name=data['firstname']
        
        order.last_name=data['lastname']
        order.phone=data['phonenumber']
        order.email=data['email']
        order.address_line1=data['address1']
        order.address_line2=data['address2']
        order.state=data['state']
        order.city=data['city']
        order.order_note=data['ordernote']
        order.order_total=grand_total
        order.tax=tax
        order.ip=request.META.get('REMOTE_ADDR')
        order.user=request.user
        # order.order=Order(first_name=first_name,last_name=last_name,phone=phone,email=email,address_line1=address_line1,address_line2=address_line2,state=state,city=city,order_note=order_note,ip=ip,tax=tax,order_total=order_total)
        order.save()

        #generate order number



        yr=int(datetime.date.today().strftime('%Y'))
        dt=int(datetime.date.today().strftime('%d'))
        mt=int(datetime.date.today().strftime('%m'))
        d=datetime.date(yr,mt,dt)
        current_date=d.strftime("%Y%m%d")  #generate id with based on date
        order_number=current_date+str(order.id)
        
        order.order_number=order_number
        order.save()

        address=UserAddress(user=request.user,first_name=data['firstname'],last_name=data['lastname'],phone=data['phonenumber'],email=data['email'],address_line1=data['address1'],address_line2=data['address2'],city=data['city'],state=data['state'])
        address.save()


        # order_data=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
        # context={
        #     'order':order_data,
        #     'cart_items':cart_items,
        #     'total':total,
        #     'tax':tax,
        #     'grand_total':grand_total
        # }
        request.session['order_id']=order_number
        global val
        def val():
            return order_number

        return redirect('payments')
    
    else:
        return HttpResponse("false")



def invoice(request):
    

    order_id=val()
    orders_data=Order.objects.get(order_number=order_id)
    
    order=OrderProduct.objects.filter(order=orders_data)

    print(order)
    print("check")
    context={'orders':order,'orders_data':orders_data}
    return render(request,'accounts/invoice.html',context)        


def payment_complete(request):
    order_number=request.GET.get('order_number')
    transID=request.GET.get('payment_id')
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_product=OrderProduct.objects.filter(order_id=order.id)

        sub_total=0
        for pro in ordered_product:
            
            sub_total+=pro.product_price*pro.quantity

        tax = (2*sub_total)/100   
        payment=Payment.objects.get(payment_id=transID)
        context={
            'order':order,
            'ordered_product':ordered_product,
            'payment':payment,
            'order_number':order.order_number,
            'transID':payment.payment_id,
            'sub_total':sub_total,
            'tax':tax
        }
        return render(request,'accounts/payment_complete.html',context)  
    except(Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('user_home')      

