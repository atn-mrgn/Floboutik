from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Produit, Categorie, Customer, BestSeller, NewProduit, Commande, Message
from django.views import View
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from replace import settings

class Index(View):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        best_seller = BestSeller.get_all_bestseller()
        new_produit = NewProduit.get_all_newproduit()
        data = {
            'bests':best_seller,
            'news':new_produit
        }
        return render(request, 'store/index.html', data)
    
    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] =  quantity + 1
            else:
                cart[product] = 1
        else:
            cart={}
            cart[product] = 1
        
        request.session['cart'] = cart
        return redirect('homepage')

class Inscription(View):
    def get(self, request):
        return render(request, 'store/inscription.html')
    
    def post(self, request):
        postData = request.POST
        firstname = postData.get("firstname")
        lastname = postData.get('lastname')
        user = postData.get('user')
        password_1 = postData.get('password-1')
        password_2 = postData.get('password-2')
        pays = postData.get('pays')
        adresse_1 = postData.get('numero-nom-rue-1')
        adresse_2 = postData.get('numero-nom-rue-2') 
        code_postal = postData.get('code-postal')
        ville = postData.get('ville')
        phone = postData.get('phone')
        email = postData.get('email')

        customer = Customer(
                firstname=firstname,
                lastname=lastname,
                user=user,
                password=password_1,
                pays=pays,
                adresse_1=adresse_1,
                adresse_2=adresse_2, 
                code_postal=code_postal,
                ville=ville,
                phone=phone,
                email=email
            )

        error_message = None

        if not firstname:
            error_message = "Le champs Prénom est requis !!"
        elif len(firstname)>50:
            error_message = "Le champs Prénom ne doit contenir plus de 50 caractères"

        if not lastname:
            error_message = "Le champs Nom est requis !!"
        elif len(lastname)>50:
            error_message = "Le champs Nom ne doit contenir plus de 50 caractères"

        if not user:
            error_message = "Le champs Nom d'utilisateur est requis !!"
        elif len(user)<4:
            error_message = "Votre nom d'utilisateur doit avoir plus de 4 caractères"
        elif user.count(' ') != 0:
            error_message = "Le nom d'utilisateur ne doit pas contenir d'espace"
        elif customer.userExist():
            error_message = "Ce nom d'utilisateur est existe dejà"

        if not password_1:
            error_message = 'Veuillez entrer un mot de passe'
        elif len(password_1)<6:
            error_message = 'Votre mot de passe doit contenir au moins 6 caractères'
        
        if not password_2:
            error_message = "Veuillez confirmer votre mot de passe"
        elif password_2 != password_1:
            error_message = "Echec de confirmation du mot de passe"
        
        if pays=="0":
            error_message = "Veuillez définir le pays"
        
        if not adresse_1:
            error_message = 'Veuilez entrer le nom et numéro de rue'
        
        if not code_postal:
            error_message = "Veuilez renseigner votre code postal"
        
        if not ville:
            error_message = 'Veuillez renseigner votre ville'
        
        if not phone:
            error_message = 'Entrer votre numéro de télephone'
        elif len(phone)<10:
            error_message = 'Entrer un numéro de téléphone valide'
        
        if not email:
            error_message = 'Veuillez entrer votre email'
        elif customer.emailExist():
            error_message = "Cet email est liée à un compte"
        
        value = {
            'firstname':firstname,
            'lastname':lastname,
            'user':user,
            'password_1':password_1,
            'password_2':password_2,
            'pays':pays,
            'adresse_1':adresse_1,
            'adresse_2':adresse_2, 
            'code_postal':code_postal,
            'ville':ville,
            'phone':phone,
            'email':email
        }

        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            msg = "Votre compte a été crée avec succès!! Connectez-vous à l'aide du formulaire ci-dessous."
            data = {
                'email':email,
                'msg':msg
            }
            return render(request, 'store/connexion.html', data)
        
        else:
            data = {
                'error':error_message,
                'values':value
            }

            return render(request, 'store/inscription.html', data)

class Connexion(View):
    return_url = None
    def get(self, request):
        Connexion.return_url = request.GET.get('return_url')
        return render(request, 'store/connexion.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                user = customer.user
                request.session['customer'] = customer.id
                request.session['user'] = user
                data = {
                    'user':user,
                }
                if Connexion.return_url:
                    return redirect(Connexion.return_url)
                else:
                    return render(request, 'store/tb.html', data)
            else:
                error_message = "L'email ou le mot de passe est invalide !!"
        else:
            error_message = "L'email ou le mot de passe est invalide !!"
        
        return render(request, 'store/connexion.html', {'error':error_message})

def deconnexion(request):
    request.session.clear()
    return redirect('homepage')

class Boutique(View):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        categorie_id = request.GET.get('categorie')
        if categorie_id:
            prds = Produit.get_filter_products(categorie_id)
        else:
            prds = Produit.get_all_products()
        ctgrs = Categorie.get_all_ctgrs()
        nb_prds = len(prds)
        paginator = Paginator(prds, per_page=15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        npage = 'Boutique'
        data = {
            'ctgrs':ctgrs,
            'prds':page_obj.object_list,
            'paginator':paginator,
            'page_number':int(page_number),
            'nb_prds':nb_prds,
            'npage':npage,
            'ctgr_id':categorie_id,
        }
        return render(request, 'store/boutique.html', data)
    
    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        page = request.POST.get('page')
        ctgr_id = request.POST.get('ctgr_id')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] =  quantity + 1
            else:
                cart[product] = 1
        else:
            cart={}
            cart[product] = 1
        request.session['cart'] = cart
        if ctgr_id:
            href = f'/boutique/?categorie={ctgr_id}&page={page}'
        else:
            href = f'/boutique/?page={page}'
        return redirect(href)
    
class Contact(View):
    def get(self, request):
        if request.session.get('user'):
            customer = Customer.get_customer_by_user(request.session.get('user'))
            if customer:
                data = {
                    'customer':customer,
                }
                return render(request, 'store/contact.html', data)
        else:
            return render(request, 'store/contact.html')
    
    def post(self, request):
        name = request.POST.get('nom')
        email = request.POST.get('email')
        sujet = request.POST.get('sujet')
        message = request.POST.get('message')
        error_message = None
        value = {
            "name":name,
            "email":email,
            "sujet":sujet,
            "message":message,
        }

        if not email:
            error_message = "Le champs email est requis !!"
    
        if not name:
            error_message = "Le champs Nom est requis !!"
        elif len(name)>50:
            error_message = "Le champs Nom ne doit contenir plus de 50 caractères"
        
        if not sujet:
            error_message = "Le champs Sujet est requis !!"
        elif len(sujet)>100:
            error_message = "Le champs Sujet ne doit contenir plus de 100 caractères"

        if not message:
            error_message = "Le champs message est requis !!"
        
        if not error_message:
            mail = Message(name=name, email=email, sujet=sujet, message=message)
            mail.save()
            msg = "Votre message a été envoyé avec succès. Merci."
            data = {
                'email':email,
                'msg':msg
            }
            """
            send_mail(
                subject= sujet,
                message= message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list= [email],
                fail_silently=False, 
            )
            """
            html_content = render_to_string("store/commande_mail.html", data_email)
            text_content = strip_tags(html_content)
            email_sent = EmailMultiAlternatives(
                subject="sujet",
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[email]
            )
            email_sent.attach_alternative(html_content, "text/html")
            email_sent.send()
            
            return render(request, 'store/contact.html', data)
        else:
            data = {
                'error':error_message,
                'values':value
            }

            return render(request, 'store/contact.html', data)

def mentions_legales(request):
    return render(request, 'store/mentions-legales.html')

class Cart(View):
    def get(self, request):
        if request.session.get('cart'):
            ids = list(request.session.get('cart').keys())
            products = Produit.get_products_by_id(ids)
            #Informtions
            user = request.session.get('user')
            if user:
                customer = Customer.get_customer_by_user(user)
            else:
                customer = None
            data = {
                'products':products,
                'customer':customer,
            }
            return render(request, 'store/cart.html', data)
        else:
            return render(request, 'store/cart.html')

    def post(self, request):
        valeur = request.POST.get('valeur')
        cart = request.session.get('cart')
        products = Produit.get_products_by_id(list(cart.keys()))
        customer = Customer.get_customer_by_user(request.session.get('user'))
        if int(valeur) == 1:
            for product in products:
                commande = Commande(
                    product=product,
                    customer=customer,
                    quantity=cart.get(str(product.id)),
                    price=product.prix,
                )
                commande.save()
            
            orders = Commande.get_commande_by_customer(customer)
            data_email ={
                'customer':customer, 
                'products':products,
            }

            html_content = get_template("email_templates/commande_mail.html").render(data_email, request)
            email_sent = EmailMessage(
                subject="sujet",
                body=html_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[customer.email],
            )
            email_sent.content_subtype = 'html'
            email_sent.send(fail_silently=False)

            request.session['cart'] = {}
            data={
                "msg":"Votre commande a bien été reçu. Un email de confirmation contenant les modalités de paiement vous a été envoyé. Merci",
                'orders':orders,
            }
            return render(request,'store/commande.html', data)

class Order(View):

    def get(self, request):
        if request.session.get('customer'):
            customer = Customer.get_customer_by_id(request.session.get('customer'))
            order = Commande.get_commande_by_customer(customer)
            data = {
                'orders':order,
            }
            return render(request, 'store/commande.html', data)
        else:
            return render(request, 'store/commande.html')

def tableau_bord(request):
    user = request.session.get('user')
    return render(request,'store/tb.html', {'user':user})

class Adresse(View):
    def get(self, request):
        user = request.session.get('user')
        customer = Customer.get_customer_by_user(user)
        data = {
            'customer':customer
        }
        return render(request, 'store/adresse.html', data)

    def post(self, request):
        adresse_1 = request.POST.get('numero-nom-rue-1')
        adresse_2 = request.POST.get('numero-nom-rue-2')
        code_postal = request.POST.get('code-postal')
        ville = request.POST.get('ville')

        error_message = None
        if not adresse_1:
            error_message = 'Veuilez entrer le nom et numéro de rue'
        
        if not code_postal:
            error_message = "Veuilez renseigner votre code postal"
        
        if not ville:
            error_message = 'Veuillez renseigner votre ville'

        if not error_message:
            msg = "Informations modifiées !!"
            customer = Customer.get_customer_by_id(request.session.get('customer'))
            customer.adresse_1 = adresse_1
            customer.adresse_2 = adresse_2
            customer.code_postal = code_postal
            customer.ville = ville
            customer.save(update_fields=['adresse_1', 'adresse_2', 'code_postal', 'ville'])
            data = {
                'msg':msg,
                'customer':customer
            }
            return render(request, 'store/adresse.html', data)
        else:
            data = {
                'error':error_message,
                'customer':customer
            }
            return render(request, 'store/adresse.html', data)

class Profile(View):
    def get(self, request):
        customer = Customer.get_customer_by_id(request.session.get('customer'))
        data = {
            'customer':customer
        }
        return render(request, 'store/profile.html', data)

    def post(self, request):
        customer = Customer.get_customer_by_id(request.session.get('customer'))
        postData = request.POST
        firstname = postData.get("firstname")
        lastname = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        last_password = postData.get('last-password')
        password_1 = postData.get('password-1')
        password_2 = postData.get('password-2')

        error_message = None

        if not firstname:
            error_message = "Le champs Prénom est requis !!"

        if not lastname:
            error_message = "Le champs Nom est requis !!"
        
        if not phone:
            error_message = 'Entrer votre numéro de télephone'
        elif len(phone)<10:
            error_message = 'Entrer un numéro de téléphone valide'
        
        if not email:
            error_message = 'Veuillez entrer votre email'
        
        if last_password:
            flag = check_password(last_password, customer.password)
            if flag:
                if not password_1:
                    error_message = 'Veuillez entrer le nouveau mot de passe'
                elif len(password_1)<6:
                    error_message = 'Votre nouveau mot de passe doit contenir au moins 6 caractères'
                
                if not password_2:
                    error_message = "Veuillez confirmer votre nouveau mot de passe"
                elif password_2 != password_1:
                    error_message = "Echec de confirmation du nouveau mot de passe"

                if not error_message:
                    msg = 'Information modifiées !!!'
                    customer.firstname = firstname
                    customer.lastname = lastname
                    customer.phone = phone
                    customer.email = email
                    customer.password = make_password(password_1)
                    customer.save(update_fields=['firstname','lastname','phone','email','password'])
                    data = {
                        'customer':customer,
                        'msg':msg
                    }
                    return render(request, 'store/profile.html',data)

                else:
                    data = {
                        'customer':customer,
                        'error':error_message,
                    }
                    return render(request, 'store/profile.html', data)
            else:
                error_message = "Votre ancien mot de passe n'est pas correct !"
                data = {
                        'customer':customer,
                        'error':error_message,
                    }
                return render(request, 'store/profile.html', data)

        else:
            if not error_message:
                msg = 'Information modifiées !!!'
                customer.firstname = firstname
                customer.lastname = lastname
                customer.phone = phone
                customer.email = email
                customer.save(update_fields=['firstname','lastname','phone','email'])
                data = {
                        'customer':customer,
                        'msg':msg,
                    }
                return render(request, 'store/profile.html', data)

            else:
                data = {
                        'customer':customer,
                        'error':error_message,
                    }
                return render(request, 'store/profile.html', data)     

class Search(View):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        param = request.GET.get('search')
        request.session['search'] = param
        prds = Produit.objects.filter(name__contains=param)
        ctgrs = Categorie.get_all_ctgrs()
        nb_prds = len(prds)
        paginator = Paginator(prds, per_page=15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        nom = request.session.get('user')
        npage = 'Resultats'
        data = {
            'ctgrs':ctgrs,
            'prds':page_obj.object_list,
            'paginator':paginator,
            'page_number':int(page_number),
            'nb_prds':nb_prds,
            'nom':nom,
            'npage':npage,
            'param':param,
        }
        return render(request, 'store/boutique.html', data)
    
    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        page = request.POST.get('page')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] =  quantity + 1
            else:
                cart[product] = 1
        else:
            cart={}
            cart[product] = 1
        
        request.session['cart'] = cart
        href = f"/boutique/search/?search={request.session.get('search')}&page={page}"
        return redirect(href)

class Detail(View):
    def get(self, request, prd_id):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        prd = Produit.get_products(prd_id)
        similar = Produit.objects.filter(sous_categorie=prd.sous_categorie)[0:7]
        data = {
            'prd':prd,
            'similar':similar,
        }
        return render(request, 'store/detail.html', data)
    
    def post(self, request, prd_id):
        product = request.POST.get('product')
        cart = request.session.get('cart')
        remove = request.POST.get('remove')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] =  quantity + 1
            else:
                cart[product] = 1
        else:
            cart={}
            cart[product] = 1
        
        request.session['cart'] = cart
        href = f'/boutique/detail/{prd_id}'
        return redirect(href)
