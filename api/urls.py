from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("form/", views.form, name="form"),
    path("addresses/", views.search, name="addresses"),
    path("addresses/<int:id>/risks", views.get_risks, name="risks"),
]
