from django import template
from store.models import Produit

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0

@register.filter(name='price_total')
def price_total(product, cart):
    return product.prix * cart_quantity(product, cart)

@register.filter(name='total_cart_price')
def total_cart_price(product, cart):
    sum = 0
    for p in product:
        sum += price_total(p, cart)
    return sum

@register.filter(name='multiply')
def multiply(nb1, nb2):
    return nb1*nb2

@register.filter(name='sum')
def sum(product, cart):
    nb1 = total_cart_price(product, cart)
    if nb1<100:
        nb2 = 15
    else:
        nb2 = 0
    return nb1 + nb2

@register.filter(name='reduce')
def reduce(prix):
    return prix + 0.35*prix

@register.filter(name='categorie')
def categorie(ctgr, ctgr_id):
    return ctgr.get(id=ctgr_id)

@register.filter(name='index_search')
def index_search(name):
    return Produit.objects.get(name=name).id