from django.contrib import admin
from .models import Produit, Categorie, Sous_categorie, Customer, BestSeller, NewProduit, Commande, Message

admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Sous_categorie)
admin.site.register(Customer)
admin.site.register(BestSeller)
admin.site.register(NewProduit)
admin.site.register(Commande)
admin.site.register(Message)