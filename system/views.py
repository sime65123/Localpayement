from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import *
# Dans vos vues Django
from django.shortcuts import render, redirect
from .forms import ClientForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ajout_client(request):
    # Remplacez request.is_ajax() par la vérification de l'en-tête HTTP ci-dessous
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            return JsonResponse({'status': 'ok' }, status=200)
        else:
            print("1")
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
        print("2")
    return JsonResponse({'status': 'error', 'message': 'Requête invalide'}, status=400)


        
def home(request):
    agences=Agence.objects.all()
    clients=Client.objects.all()
    types_lavage=TypeL.objects.all()
    context={'agences':agences,'clients':clients,'types_lavage':types_lavage}

    return render(request,'home.html',context)
def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Retourner un message d'erreur si la connexion échoue
            return render(request, 'login.html', {'error': 'Email ou mot de passe incorrect.'})
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from .forms import ClientForm

def ajouter_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ClientForm()
    return render(request, 'ajouter_client.html', {'form': form})


from django.shortcuts import render
from .models import Ticket
from .forms import TicketForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generer_facture(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.vendeur = request.user  # Récupérer le vendeur actuel
            ticket.save()
            # Générer l'aperçu PDF
            context = {'ticket': ticket}
            template = get_template('facture_pdf.html')
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="facture.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('Des erreurs <pre>' + html + '</pre>')
            return response
    else:
        form = TicketForm()
    return render(request, 'generer_facture.html', {'form': form})


from django.shortcuts import render



def logout_view(request):
    logout(request)  # Utilisez logout pour déconnecter l'utilisateur
    return render(request,"login.html")

@csrf_exempt
def get_client(request):
    # Récupérer toutes les chambres libres
    client_libres = Client.objects.all()

    # Créer une liste de dictionnaires contenant les informations des chambres libres
    client_data = [
        {'id': client.id, 'nom': client.nom,'numero':client.numero_telephone,'agence':client.agence.adresse_agence,'adresse':client.adresse}
        for client in client_libres
    ]
    return JsonResponse(client_data, safe=False)






@csrf_exempt
def get_ticket(request):
    # Récupérer toutes les chambres libres
    tickets = Ticket.objects.all().order_by('-date')

    # Créer une liste de dictionnaires contenant les informations des chambres libres
    ticket_data = [
        {'id': ticket.id, 'numero': ticket.numero,'date':ticket.date,'est_utilise':ticket.est_utilise,'client':ticket.client.nom}
        for ticket in tickets
    ]
    # Renvoyer les données au format JSON
    return JsonResponse(ticket_data, safe=False)


from django.http import JsonResponse
from django.utils import timezone

def somme_client_du_jour(request):
    today2 = timezone.now().date()
    clients = Client.objects.filter(date=today2)
    somme=0
    for client in clients:
        somme =somme + 1
    return JsonResponse({'somme': somme})

def somme_souscription_du_jour(request):
    today = timezone.now().date()
    tickets = Ticket.objects.filter(date=today)
    somme=0
    for ticket in tickets:
        somme =somme + 1
    return JsonResponse({'somme': somme})




@csrf_exempt
def rechercher_clients(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Récupérer le terme de recherche et le numéro de page depuis les données POST
        searchTerm = request.POST.get('searchTerm')
    # Utiliser 1 comme valeur par défaut si 'page' n'est pas fourni

        # Filtrer les clients par le terme de recherche
        clients_query = Client.objects.filter(nom__icontains=searchTerm)

        # Configurer la pagination
       
        # Préparer les données des clients pour la réponse JSON
        clients_data = [
            {
                'nom': client.nom,
                'id':client.id,
                'adresse': client.adresse,
                'tel': client.numero_telephone,
                'matricule': client.matricule,
                'date':client.date,
            } for client in clients_query
        ]

        response_data = {
            'clients': clients_data,
            
        }



        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Requête invalide'}, status=400)





from django.shortcuts import render
from fpdf import FPDF
import base64

# Dans votre vue Django (par exemple, views.py)

from django.shortcuts import render
from fpdf import FPDF
import base64

class InvoicePDF(FPDF):
    def header(self):
        # En-tête de la facture
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Facture", 0, 1, "C")

    def footer(self):
        # Pied de page (facultatif)
        pass

    def generate_invoice(self):
        # Génération du contenu de la facture
        self.add_page()
        self.set_font("Arial", size=12)
        self.cell(0, 10, "Numéro de facture : 12345", ln=True)
        self.cell(0, 10, "Montant dû : $100", ln=True)
        # Ajoutez d'autres détails de la facture ici

# Vue pour afficher la facture dans un modal
def invoice_preview(request):
    pdf = InvoicePDF()
    pdf.generate_invoice()

    # Convertissez le contenu du PDF en base64
    pdf_content_base64 = base64.b64encode(pdf.output(dest='S').encode('latin1')).decode('utf-8')

    # Renvoyez le contenu du PDF au template
    context = {
        'invoice_content_base64': pdf_content_base64
    }
    return render(request, 'invoice_preview.html', context)




# views.py
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse  # Importez JsonResponse
from .models import Ticket
from .forms import TicketForm  # Assurez-vous d'avoir un formulaire pour la saisie des données
import json



from fpdf import FPDF

def generate_invoice(ticket):
    # Créez un objet FPDF
    pdf = FPDF()
    pdf.add_page()

    # Ajoutez du contenu à votre facture (par exemple, le numéro de ticket)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Numéro de ticket : {ticket.numero}", ln=True, align="L")

    # Générez le contenu de la facture (ajoutez d'autres informations ici)

    # Sauvegardez le PDF dans un buffer
    buffer = io.BytesIO()
    pdf.output(buffer)
    pdf_content_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return pdf_content_base64

@csrf_exempt
def create_ticket(request):
    if request.method == 'POST':
        client = request.POST.get('client')
        type_lavage = request.POST.get('type_lavage')
        vendeur = request.POST.get('vendeur')
        print(f"-----------------------{client}----------------------")
        print(f"-----------------------{type_lavage}----------------------")
        print(f"-----------------------{vendeur}----------------------")
    
        form = TicketForm(request.POST)
        if form.is_valid():
            # Récupérez les données du formulaire
           
            print("-------------------------------------------1------------------------------------------")
            # Créez un nouvel objet Ticket
            ticket=form.save()
            # Créez un dictionnaire avec les données à renvoyer au format JSON
            response_data = {
                #'invoice_content_base64': pdf_content_base64,
                'ticket_numero': ticket.numero,
                'nom':ticket.client.nom,
                'type_lavage':ticket.type_lavage.nom,
                'vendeur':ticket.vendeur.email,
                'est_utilise':ticket.est_utilise,
                'date':ticket.date       
            }

            # Renvoyez les données au format JSON en utilisant JsonResponse
            return JsonResponse(response_data)
  




import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def generate_invoice_pdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, "Hello world.")  # Remplacez par votre contenu de facture
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="invoice.pdf")
import base64

def encode_to_base64(content):
    return base64.b64encode(content).decode("utf-8")




















import datetime
import os

def generate_invoice2(invoice_number, customer_name, customer_address,  payment_method, due_date, logo_path=None, structure_number=None):
    """
    Génère une facture moderne et imprimable au format (150mm, 100mm) avec un arrière-plan transparent "Echangeur Hotel".

    Args:
        invoice_number (str): Le numéro de la facture.
        customer_name (str): Le nom du client.
        customer_address (str): L'adresse du client.
        items (list): Une liste d'objets de produits. Chaque objet doit avoir les propriétés suivantes :
            - name (str): Le nom du produit.
            - quantity (int): La quantité du produit.
            - price (float): Le prix unitaire du produit.
        payment_method (str): Le mode de paiement.
        due_date (datetime.date): La date d'échéance du paiement.
        logo_path (str, optional): Le chemin d'accès au logo. Defaults to None.
        structure_number (str, optional): Le numéro de la structure. Defaults to None.
    """

    # Configuration des polices
    font_family = "Arial"
    font_size = 7  # Réduire la taille de la police

    # Créer un nouveau document PDF
    from fpdf import FPDF
    width = 150  # Largeur du document
    height = 100  # Hauteur du document
    pdf = FPDF(unit='mm', format=[width, height]) 
    pdf.set_font(font_family, size=font_size)
    pdf.add_page()

    # Arrière-plan transparent "Echangeur Hotel"
    pdf.set_fill_color(255, 255, 255)  # Couleur blanche avec opacité
    pdf.rect(0, 0, width, height, style="F")  # Remplissage de la page
    pdf.set_text_color(0, 0, 0)  # Noir pour le texte
    pdf.set_xy(width * 0.1, 5)  # Position du texte
    pdf.set_font(font_family, size=10, style="B")
    pdf.cell(w=0, h=7, txt="Echangeur Hotel", align="C", ln=True)

    # Logo (si fourni)
    if logo_path:
        pdf.image(logo_path, x=width * 0.05, y=10, w=width * 0.1, h=width * 0.1)

    # En-tête de la facture
    pdf.set_font(font_family, size=7, style="B")
    pdf.set_xy(width * 0.03, 23)  # Position du texte
    pdf.cell(w=0, h=10, txt="Enrollement Client", align="C", ln=True)
    pdf.set_font(font_family, size=font_size)
    pdf.set_xy(width * 0.05, 27)  # Position du texte
    pdf.cell(w=0, h=10, txt=f"Numéro de Client : {invoice_number}", align="L", ln=True)
    pdf.set_xy(width * 0.05, 32)  # Position du texte
    pdf.cell(w=0, h=10, txt=f"Numéro de Réservation : {invoice_number}", align="L", ln=True)
    if structure_number:
        pdf.set_xy(width * 0.05, 37)  # Position du texte
        pdf.cell(w=0, h=10, txt=f"Nom : {structure_number}", align="L", ln=True)
    pdf.set_xy(width * 0.05, 40)  # Position du texte
    pdf.cell(w=0, h=10, txt=f"Date : {datetime.date.today().strftime('%Y-%m-%d')}", align="L", ln=True)


    col_width_1 = 130 / 3  # Largeur de la première colonne
    col_width_2 = col_width_1 * 2  # Largeur de la deuxième colonne

    # En-têtes du tableau
    pdf.set_font("Arial", size=8, style="B")
    pdf.cell(w=col_width_1, h=5, txt="Département", border=1, align="C")
    pdf.cell(w=col_width_2, h=5, txt="Dépenses", border=1, align="C", ln=True)

    # Contenu du tableau
    pdf.set_font("Arial", size=8)
    pdf.cell(w=col_width_1, h=6, txt="Bar", border=1, align="C")
    pdf.cell(w=col_width_2, h=6, border=1, align="C", ln=True)  # Cellule [0, 1]
    pdf.cell(w=col_width_1, h=6, txt="Réservation", border=1, align="C")
    pdf.cell(w=col_width_2, h=6,  border=1, align="C", ln=True)  # Cellule [1, 1]
    pdf.cell(w=col_width_1, h=6, txt="Cuisine", border=1, align="C")
    pdf.cell(w=col_width_2, h=6,  border=1, align="C", ln=True)  # Cellule [2, 1]


    pdf.set_xy(width * 0.4, 75)  
    pdf.cell(w=0, h=4, txt="Votre Satisfaction , notre priorité !", align="L")

    # Enregistrer le PDF
    filename = f"facture_{invoice_number}.pdf"
    pdf.output(filename)

    # Ouvrir le fichier PDF
    os.startfile(filename)







from django.shortcuts import render
from django.http import JsonResponse
from .models import Ticket

def analytics(request):
    # Récupérer les lavages de la dernière semaine
    # (Ajustez la durée si besoin)
    lavages = Ticket.objects.filter(date__gte=datetime.date.today() - datetime.timedelta(days=7))

    # Groupé par heure du jour
    lavages_par_heure = lavages.annotate(heure=TruncHour('date')).values('heure').annotate(count=Count('id')).order_by('heure')

    # Groupé par mois
    lavages_par_mois = lavages.annotate(mois=TruncMonth('date')).values('mois').annotate(count=Count('id')).order_by('mois')

    # Formater les données pour Chart.js
    data_heure = [{'x': str(l['heure']), 'y': l['count']} for l in lavages_par_heure]
    data_mois = [{'x': l['mois'].strftime('%Y-%m'), 'y': l['count']} for l in lavages_par_mois]

    return JsonResponse({'data_heure': data_heure, 'data_mois': data_mois})