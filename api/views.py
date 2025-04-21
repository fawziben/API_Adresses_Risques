from django.shortcuts import render
from django.http import JsonResponse
import requests
from .models import Address


def form(request):
    return render(request, "api/form.html")


def search(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Méthode non autorisée"},
            status=405
        )

    query = request.POST.get('address', '').strip()

    if not query:
        context = {
            'status_code': 400,
            'status_message': "Le champ de recherche est requis et doit être une chaîne non vide."
        }
        return render(request, "api/sortie.html", context, status=400)

    try:
        api_url = f"https://api-adresse.data.gouv.fr/search/?q={requests.utils.quote(query)}&limit=1"
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not data.get('features'):
            context = {
                'status_code': 404,
                'status_message': "Adresse non trouvée. Aucun résultat ne correspond à votre recherche."
            }
            return render(request, "api/sortie.html", context, status=404)

        feature = data['features'][0]
        properties = feature['properties']
        geometry = feature['geometry']

        address_data = {
            'label': properties.get('label'),
            'housenumber': properties.get('housenumber'),
            'street': properties.get('street'),
            'postcode': properties.get('postcode'),
            'citycode': properties.get('citycode'),
            'latitude': geometry['coordinates'][1],
            'longitude': geometry['coordinates'][0]
        }

        # Utilisation de l'ORM Django
        existing_address = Address.objects.filter(
            postcode=address_data['postcode'],
            citycode=address_data['citycode'],
            street=address_data['street'],
            housenumber=address_data['housenumber']
        ).first()

        if existing_address:
            address_data = {
                'id': existing_address.id,
                'label': existing_address.label,
                'housenumber': existing_address.housenumber,
                'street': existing_address.street,
                'postcode': existing_address.postcode,
                'citycode': existing_address.citycode,
                'latitude': existing_address.latitude,
                'longitude': existing_address.longitude
            }
        else:
            new_address = Address.objects.create(**address_data)
            address_data['id'] = new_address.id

        context = {
            'status_code': 200,
            'status_message': 'OK',
            'address_data': address_data
        }
        # Choisir un des deux retours selon l’usage
        # Pour affichage HTML
        return render(request, "api/sortie.html", context)
        # return JsonResponse(context, status=200) -> cette ligne pour afficher l'objet sous format json sans ui

    except requests.exceptions.RequestException:
        context = {
            'status_code': 500,
            'status_message': "Erreur serveur : impossible de contacter l'API externe."
        }
        return render(request, "api/sortie.html", context, status=500)
    except Exception as e:
        context = {
            'status_code': 500,
            'status_message': "Erreur serveur interne"
        }
        return render(request, "api/sortie.html", context, status=500)


def get_risks(request, id):
    if request.method != "GET":
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)

    try:
        try:
            address = Address.objects.get(id=id)
        except Address.DoesNotExist:
            return JsonResponse(
                {"error": "Adresse non trouvée."},
                status=404
            )
        georisques_url = f"https://georisques.gouv.fr/api/v1/resultats_rapport_risque?code_insee={address.citycode}"
        response = requests.get(georisques_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Choisir un des deux retours selon l’usage
        # Pour affichage HTML
        return render(request, 'api/risks.html', {'data': data})
        # return JsonResponse(data, status=200, safe=False)        # Pour API JSON brute

    except requests.exceptions.RequestException:
        return JsonResponse(
            {"error": "Erreur serveur : échec de la récupération des données de Géorisques."},
            status=500
        )
    except Exception:
        return JsonResponse(
            {"error": "Erreur serveur interne."},
            status=500
        )
