from django import template
from site_models.models import Order

register = template.Library()


@register.filter
def cart_product_count(user)->int:
    if user.is_authenticated:
        qs = Order.objects.filter(customer=user, ordered=False)
        # print(qs)
        if qs.exists():
            return qs[0].product.count()

    return 0