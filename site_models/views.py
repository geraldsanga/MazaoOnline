from .models import Category, Product, Order, OrderProduct, BillingAddress, Payment, Contact
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, DetailView
from django.contrib import messages
from django.utils import timezone
from .forms import CheckoutForm
from django.db.models import Q
from functools import reduce
import operator
import stripe
# from _functools import reduce


stripe.api_key = "sk_test_51HItOtLilkzwV54uwf5LfpsQp6302tMZS2bOMjb9S9XaqOmuJNPQEmUseDupisP55UOV3knPneAVOaZXsqQlqKjR00CdeIMoqO"


@login_required(login_url="login_view")
def checkout_page(request, pk):
    category_list = Category.objects.all()
    user = request.user
    item_to_checkout = Product.objects.get(id=pk)
    context = {
        'Item': item_to_checkout,
        'categories': category_list,
        'user': user,
        'form': CheckoutForm()
    }

    if request.method == "POST":
        form = CheckoutForm(request.POST or None)
        try:
            order = Order.objects.get(customer=request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get("street_address")
                country = form.cleaned_data.get("country")
                phone = form.cleaned_data.get("phone")
                city = form.cleaned_data.get("city")

                billing_address = BillingAddress(
                    customer = request.user,
                    country = country,
                    city = city,
                    street_address = street_address,
                    phone = phone
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
        
        except ObjectDoesNotExist:
            messages.warning(request, "You do not have an active order.", fail_silently=False)
            return redirect("checkout_page")
    return render(request, 'checkout.html', context)


def home_page(request):
    category_list = Category.objects.all()
    product_list = Product.objects.all().order_by('-date_created')
    sample_products = product_list[:3]
    context = {
        'products': product_list,
        'categories': category_list,
        'sample_products': sample_products,
        # 'latest_products': Product.objects.order_by('-id')[:3]
    }
    return render(request, 'home.html', context)


@login_required(login_url="login_view")
def save_order(request):
    pass


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.error(
                self.request, "You do not have an active order.",
                fail_silently=False
            )
            return redirect("/")

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail.html"


@login_required(login_url="login_view")
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(
        customer=request.user,
        product=product,
        ordered=False
    )
    # Order Queryset
    order_qs = Order.objects.filter(customer=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order product is in the order
        if order.product.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            # messages.success(
            #     request, "This Item quantity is updated successfully.", fail_silently=False
            # )
            return redirect("order-summary")
        
        else:
            order.product.add((order_product))
            messages.success(request,
            "You have successfully added an item to the cart.", fail_silently=False
            )
            return redirect("order-summary")

    else:
        order = Order.objects.create(customer=request.user, ordered_date=timezone.now())
        order.product.add(order_product)
    
    return redirect("order-summary")


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        return render(self.request, "checkout-page.html", {
            "form": CheckoutForm(),
            "order": Order.objects.get(customer=self.request.user, ordered=False)
        })
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get("street_address")
                country = form.cleaned_data.get("country")
                phone = form.cleaned_data.get("phone")
                city = form.cleaned_data.get("city")
                payment_option = form.cleaned_data.get("payment_option")

                billing_address = BillingAddress(
                    customer = self.request.user,
                    country = country,
                    city = city,
                    street_address = street_address,
                    phone = phone
                )
                
                # if len(street_address) < 2:
                #     for value in street_address:
                #         if value in ["#", "@", "!", "/", ")","%","_","-",","]:
                #             messages.error(self.request, "Bad input for street address")
                #             return redirect("checkout")
                #     else:
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # else:
                #     messages.error(self.request, "Bad input for street address")
                #     return redirect("checkout")
                # print("Checked Out.")
                
                if payment_option == 'S':
                    return redirect("payment", payment_option="stripe")
                elif payment_option == 'P':
                    return redirect("cash-delivery", payment_option="cash")
                else:
                    messages.warning(self.request, "Invalid payment option.", fail_silently=False)
                    return redirect("checkout")

        except ObjectDoesNotExist:
            
            messages.warning(self.request, "You do not have an active order.", fail_silently=False)
            return redirect("order-summary")


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        return render(self.request,"payment.html",{
            "order": Order.objects.get(customer=self.request.user, ordered=False)
        })

    def post(self, *args, **kwargs):
        order = Order.objects.get(customer=self.request.user, ordered=False)

        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100 ) # Values are in Cents:

        try:
            charge = stripe.Charge.create(
                amount=amount, 
                currency="tzs",
                source=token
                # description="My First Test Charge (created for API docs)",
            )

            # Create The Payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.customer = self.request.user
            payment.amount = int(order.get_total())
            payment.save()

            # Assign Payment to the Order
            order_products = order.product.all()
            order_products.update(ordered=True)
            for product in order_products:
                product.save()

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order is successfully!", fail_silently=False)
            return redirect("/")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

            # print('Status is: %s' % e.http_status)
            # print('Type is: %s' % e.error.type)
            # print('Code is: %s' % e.error.code)
            # # param is '' in this case
            # print('Param is: %s' % e.error.param)
            # print('Message is: %s' % e.error.message)
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Rate limit error.")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            messages.error(self.request, "Invalid Parameters.{}".format(e))
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Failed to authenticate with Stripe.")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Failed Stripe API connection. Check out network connection.")
            return redirect("/")
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong.")
            return redirect("/")
        except Exception as e:
            # Send an email to myself
            messages.error(self.request, "A serious error occured. We've emailed you instructions.")
            return redirect("/")

@login_required(login_url="login_view")
def remove_single_item_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # print(item.slug)

    order_qs = Order.objects.filter(
        customer=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        # print(order.item.filter(item__slug=item.slug))
        if order.product.filter(product__slug=product.slug).exists():
            order_item = OrderProduct.objects.filter(
                product=product,
                customer=request.user,
                ordered=False
            )[0]
            # print("Exists.")
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.product.remove(order_item)
            # messages.success(
            #     request, "This item quantity was updated.", fail_silently=False
            #     )
            return redirect("order-summary")

        else:
            # Adding a message saying that the order doesn't contain this OrderItem
            messages.info(request, "Your Order doesn't contains an Item.", fail_silently=False)
            return redirect("order-summary", slug=slug)

    else:
        # Adding a message saying a user doesnt have an order
        messages.info(request, "You don't seems to have an Order yet!.", fail_silently=False)
        return redirect("product", slug=slug)

    return redirect("product", slug=slug)


@login_required(login_url="login_view")
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # print(item.slug)

    order_qs = Order.objects.filter(
        customer=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        # print(order.item.filter(item__slug=item.slug))
        if order.product.filter(product__slug=product.slug).exists():
            order_item = OrderProduct.objects.filter(
                product=product,
                customer=request.user,
                ordered=False
            )[0]
            # print("Exists.")

            order.product.remove(order_item)
            messages.success(
                request, "You have successfully removed an item from the cart.", fail_silently=False
                )
            return redirect("order-summary")
        
        else:
            # Adding a message saying that the order doesn't contain this OrderItem
            messages.info(request, "Your Order doesn't contains an Item.", fail_silently=False)
            return redirect("product", slug=slug)

    else:
        # Adding a message saying a user doesnt have an order
        messages.info(request, "You don't seems to have an Order yet!.", fail_silently=False)
        return redirect("product", slug=slug)

    return redirect("product", slug=slug)


class ContactView(View):

    def get(self, *args, **kwargs):

        return render(self.request, "contact.html",{
            
        })
    
    def post(self, *args, **kwargs):
        if self.request.method == "POST":
            phone = self.request.POST.get("phone")
            message = self.request.POST.get("message")

            contact = Contact(
                phone = phone,
                message = message
            )
            contact.save()

            messages.success(self.request, "Thanks for contacting us!",fail_silently=False)
            return redirect("contact")
        

class CashDeliveryView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):

        return render(self.request, "cash-delivery.html",{
            "delivery_address": BillingAddress.objects.first()
        })
    
    def post(self, *args, **kwargs):
        try:
            order = Order.objects.get(customer=self.request.user, ordered=False)
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

            messages.success(self.request, "Your order is successfully!", fail_silently=False)
            return redirect("/")
        except Exception:
            payment_option="cash"
            messages.info(self.request, "Failed to clear order!", fail_silently=False)
            return redirect("cash-delivery", payment_option)


class OrdersView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        # Get all orders of the requested user
        orders = Order.objects.filter(customer=self.request.user)

        return render(self.request, 'all_orders.html',{
            'orders': orders
        })
    
    def post(self, *args, **kwargs):
        pass


@login_required(login_url="login_view")
def search_view(request):
    context = dict()
    queryset = Product.objects.all().order_by("name")
    results = list()
    q = request.POST.get("q")
    if q is not None:
        words = q.split()
        for w in words:
            results.append(queryset.filter(
                Q(name__icontains=w) | Q(description__icontains=w) | Q(price__icontains=w)
            ).distinct())
        context["results"] = results
    return render(request, "results.html", context)

