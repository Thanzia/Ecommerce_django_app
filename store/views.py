from django.shortcuts import render, redirect
from django.views.generic import View,FormView

from store.models import *
from store.forms import *

import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404

# Create your views here.

#to list all the products
#lh:8000/store/productslist

class ProductListView(View):

    def get(self,request):

        user = request.user

        if user.is_authenticated:
            
            products = Product.objects.all()
             
            return render(request,"all.html",{"products":products})
        
        else:
             
             return redirect("login")


    
class ProductDetailView(View):

    def get(self,request,**kwargs):

        id = kwargs.get("pk")

        user = request.user

        if user.is_authenticated:

            item = Product.objects.get(id = id)  # specific object item = <product object 1>

            return render(request,"productdetail.html",{"item":item})
        
        else:

            return redirect("login")

        # print(item)

# add to cart view
class AddtoCartView(View):

    def post(self,request,**kwargs):

        id = kwargs.get("pk")

        # print("hello world")
        
        quantity = request.POST.get("quantity")

        product_object = Product.objects.get(id = id)

        #print(size_object,quantity)

        user = Cart.objects.get(user = request.user)

        print(user)

        Cartitems.objects.create(cart_object=user,quantity=quantity, product_object=product_object)

        print("item added sucessfully")

        return redirect("cart_summary")
    

# cart summary view
class CartSummaryView(View):

    def get(self,request,**kwargs):

        user = Cart.objects.get(user = request.user)

        items = Cartitems.objects.filter(cart_object = user,is_ordered = False)

        total_sum = sum([i.item_total() for i in items])

        total = items.count()

        print(total)

        return render(request,"cartsummary.html",{"items":items,"total":total,"total_sum":total_sum,"total_price":total_sum+10})

# remove from cart
class CartSummaryRemove(View):

    def get(self,request,**kwargs):

        id = kwargs.get("pk")

        item = Cartitems.objects.get(id = id)

        item.delete()

        return redirect("cart_summary")

# add to wishlist view
class AddWishlistItem(View):

    def post(self,request,**kwargs):

        id = kwargs.get("pk")

        print(id)

        item = Product.objects.get(id = id)

        user = Wishlist.objects.get(user = request.user)

        WishlistItem.objects.create(wishlist_object=user,product_object=item)

        return redirect("wishlist")

# wishlist view
class WishlistView(View):

	def get(self,request,**kwargs):

		user = Wishlist.objects.get(user = request.user)

		items = WishlistItem.objects.filter(wishlist_object = user)

		return render(request,"wishlist.html",{"items":items})
    
# wishlist remove
class WishlistRemoveItem(View):

     def get(self,request,**kwargs):
          
          id = kwargs.get("pk")

          item = WishlistItem.objects.get(id = id)

          item.delete()

          return redirect("wishlist")


class OrderView(FormView):

    form_class = OrderForm

    template_name = "order.html"
    
    def post(self,request,**kwargs):

        form_data = request.POST

        form_instance = self.form_class(form_data)

        if form_instance.is_valid():

            #form_instance.customer=request.user

            order_object = form_instance.save(commit=False)  # creating an order instance

            order_object.user = request.user

            order_object.save()

            print(order_object)

            ordered_user = Cart.objects.get(user=request.user)

            ordered_items = Cartitems.objects.filter(cart_object=ordered_user,is_ordered=False)

            # total_sum = sum([i.item_total for i in ordered_items])
            # total_sum *= 100  # paisa to rupeess convertion
            # print(total_sum)
            # total_price = 0


            for i in ordered_items:

                OrderItem.objects.create(order = order_object,
                                             product = i.product_object,                                        
                                             quantity = i.quantity,
                                             price = i.item_total())
                
                i.is_ordered = True

                i.save()

            items = OrderItem.objects.filter(order = order_object)

            total_sum = sum([float(i.price) for i in items])

            total_sum *= 100

            print(total_sum)
            
            if order_object.payment_method=="ONLINE":

                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

                data = { "amount": int(total_sum), "currency": "INR", "receipt": "order_rcptid_11" }

                payment = client.order.create(data=data) # Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            
                if payment:

                    print(payment)

                    order_object.order_id = payment.get('id')

                    order_object.is_paid = False

                    order_object.save()
      
                    return render(request,"razorpay_checkout.html",{'order':order_object,'order_id':order_object.order_id,'amount':total_sum,'items':items,'razorpay_key_id': settings.RAZORPAY_KEY_ID})
        
            elif order_object.payment_method=="COD":

                order_object.is_paid = True

                order_object.save()

                return render(request,"cod_checkout.html",{'order':order_object,'items':items,'amount': total_sum})
            
class CODSuccessView(View):

    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        order = get_object_or_404(Order, id=id, user=request.user)

        # Template can get items and total from order
        return render(request, "cod_payment_success.html", {
            'order': order
        })

    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        order = get_object_or_404(Order, id=id, user=request.user)

        return render(request, "cod_payment_success.html", {
            'order': order
        })


class PaymentSucessView(View):

    def get(self,request):

        return render(request,"payment_sucess.html")
    
    def post(self,request):

        print(request.POST)

        payment_id = request.POST.get("razorpay_payment_id")

        order_id = request.POST.get("razorpay_order_id")

        order = Order.objects.get(order_id = order_id)

        order.is_paid = True

        order.save()

        return render(request,"payment_sucess.html")

class OrderSummary(View):

    def get(self,request,**kwargs):

        user = Order.objects.filter(customer=request.user)

        orderitems = OrderItem.objects.filter(order_object__in=user)

        return render(request,"ordersummary.html",{"orderitems":orderitems})




# error handlers

# store/views.py
import logging

# Create a logger for errors
logger = logging.getLogger(__name__)

def error_handler(request, exception=None, status=500):
    # Log the error for debugging (only logs if status is 500 or unknown)
    if status == 500 or not exception:
        logger.exception("Server error occurred")
    else:
        logger.warning(f"Error {status}: {exception}")

    context = {
        'status_code': status,
        'message': {
            404: "Oops! The page you are looking for was not found.",
            500: "Something went wrong on our server.",
            403: "You do not have permission to access this page.",
            400: "Bad request. Please check your input and try again."
        }.get(status, "An unexpected error occurred.")
    }
    return render(request, 'error.html', context, status=status)

# Wrappers for Django’s error handlers
def error_404_view(request, exception):
    return error_handler(request, exception, 404)

def error_500_view(request):
    return error_handler(request, status=500)

def error_403_view(request, exception):
    return error_handler(request, exception, 403)

def error_400_view(request, exception):
    return error_handler(request, exception, 400)
