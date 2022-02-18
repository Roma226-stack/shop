from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
import logging
from .models import Category, Cart, Customer, Notebook, Smartphone

logger = logging.getLogger('main')


class CategoryDetailMixin(SingleObjectMixin):
    CATEGORY_SLUG2PRODUCT_MODEL = {
        'notebooks': Notebook,
        'smartphones': Smartphone,
    }

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_SLUG2PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_categories_for_left_sidebar()
            context['category_products'] = model.objects.all()
            return context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_categories_for_left_sidebar()
        return context


class CartMixin(View):

    # permission_required = 'cart.change_cart'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logger.info('User is auntificated' + " " + str(request.user))
            customer = Customer.objects.filter(user=request.user).first()
            print("Вывод  " + str(customer))
            if not customer:
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            cart_last = Cart.objects.last()
            # if cart:
            #     return cart
            # elif not cart:
            #     cart = Cart.objects.create(id=(cart_last.id + 1), owner=customer)

            if cart == None or cart.id and cart.owner != customer:
                if not cart_last:
                    cart = Cart.objects.create(id=1, owner=customer)
                else:
                    cart = Cart.objects.create(id=(cart_last.id + 1), owner=customer)
            elif not cart:
                cart = Cart.objects.create(id=1, owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            cart_latest = Cart.objects.last()
            if not cart:
                cart = Cart.objects.create(id=(cart_latest.id + 1), for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
