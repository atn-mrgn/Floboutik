from django.shortcuts import redirect

def auth_middleware(get_response):

    def middleware(request):
        links = ['/tableau_bord/', '/commande/','/adresse/','/profile/','/deconnexion/']
        returnUrl = request.META['PATH_INFO']
        if  links.count(request.path)>=1:
            if not request.session.get('customer'):
                return redirect(f'/connexion/?return_url={returnUrl}')
        response = get_response(request)
        return response

    return middleware