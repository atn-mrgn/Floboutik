from django.urls import path
from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='homepage'),
    path('inscription/', views.Inscription.as_view()),
    path('boutique/', views.Boutique.as_view(), name='boutique'),
    path('contact/', views.Contact.as_view()),
    path('connexion/', views.Connexion.as_view(), name='connexion'),
    path('mentions_legales/', views.mentions_legales),
    path('deconnexion/', views.deconnexion),
    path('cart/', views.Cart.as_view()),
    path('commande/', views.Order.as_view(), name='commande'),
    path('tableau_bord/', views.tableau_bord),
    path('adresse/', views.Adresse.as_view()),
    path('profile/', views.Profile.as_view()),
    path('boutique/search/', views.Search.as_view(), name = 'search'),
    path('boutique/detail/<str:prd_id>', views.Detail.as_view(), name = 'detail')
]
