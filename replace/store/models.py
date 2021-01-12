from django.db import models
import datetime

class Categorie(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

    @staticmethod
    def get_all_ctgrs():
        return Categorie.objects.all()

class Sous_categorie(models.Model):
    name = models.CharField(max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.name

class Produit(models.Model): 
    name = models.CharField(max_length=300)
    prix = models.IntegerField()
    short_description = models.TextField(default=None)
    description = models.TextField(blank=True, default=None)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, default=1)
    sous_categorie = models.ForeignKey(Sous_categorie, on_delete=models.CASCADE, default=1)
    image_1 = models.ImageField(upload_to = 'upload/produit/')
    image_2 = models.ImageField(upload_to = 'upload/produit/', blank=True)
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def get_products(id):
        return Produit.objects.get(id=id)
    
    @staticmethod
    def get_filter_products(categorie_id):
        return Produit.objects.filter(categorie=categorie_id)
        
    @staticmethod
    def get_products_by_id(ids):
        return Produit.objects.filter(id__in=ids)
        
    @staticmethod
    def get_all_products():
        return Produit.objects.all()

class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    user = models.CharField(max_length=100, default=None)
    password = models.CharField(max_length=200)
    pays = models.CharField(max_length=200)
    adresse_1 = models.CharField(max_length=200)
    adresse_2 = models.CharField(max_length=200,default=None, blank=True)
    code_postal = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def register(self):
        self.save()
    
    @staticmethod
    def get_customer_by_id(id):
        return Customer.objects.get(id=id)

    @staticmethod
    def get_customer_by_user(user):
        return Customer.objects.get(user=user)

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email= email)
        except:
            return False

    def emailExist(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False
    
    def userExist(self):
        if Customer.objects.filter(user=self.user):
            return True
        return False

class BestSeller(models.Model):
    name = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
    
    @staticmethod
    def get_all_bestseller():
        return BestSeller.objects.all()

class NewProduit(models.Model):
    name = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
    
    @staticmethod
    def get_all_newproduit():
        return NewProduit.objects.all()

class Commande(models.Model):
    product = models.ForeignKey(Produit, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField() 
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    @staticmethod
    def get_commande_by_customer(customer):
        return Commande.objects.filter(customer=customer).order_by('-date')

class Message(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    sujet = models.CharField(max_length=100, null=True)
    message = models.TextField()

    def __str__(self):
        return self.name