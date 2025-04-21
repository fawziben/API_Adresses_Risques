from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from requests.exceptions import ConnectionError
from ..models import Address


class SearchAddressViewTest(TestCase):
    def setUp(self):
        self.url = reverse("api:addresses")

    def test_get_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(response.content, {
            "error": "Méthode non autorisée"
        })

    def test_post_missing_address_field(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "api/sortie.html")
        self.assertIn("status_message", response.context)
        self.assertEqual(response.context["status_message"],
                         "Le champ de recherche est requis et doit être une chaîne non vide.")

    @patch("requests.get")
    def test_post_valid_address_not_found(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"features": []}

        response = self.client.post(
            self.url, data={"address": "adresse inconnue"})
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "api/sortie.html")
        self.assertEqual(response.context["status_message"],
                         "Adresse non trouvée. Aucun résultat ne correspond à votre recherche.")

    @patch("requests.get")
    def test_post_valid_address_found_and_created(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "features": [{
                "properties": {
                    "label": "8 boulevard du port 91000 Evry",
                    "housenumber": "8",
                    "street": "boulevard du port",
                    "postcode": "91000",
                    "citycode": "91228"
                },
                "geometry": {
                    "coordinates": [2.445, 48.632]
                }
            }]
        }

        response = self.client.post(self.url, data={"address": "8 bd du port"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/sortie.html")
        self.assertEqual(response.context["status_message"], "OK")
        self.assertIn("address_data", response.context)
        self.assertTrue(Address.objects.filter(postcode="91000").exists())

    @patch("requests.get", side_effect=ConnectionError("Erreur de réseau"))
    def test_post_api_failure(self, mock_get):
        response = self.client.post(
            self.url, data={"address": "n'importe quoi"})
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, "api/sortie.html")
        self.assertEqual(response.context["status_message"],
                         "Erreur serveur : impossible de contacter l'API externe.")
