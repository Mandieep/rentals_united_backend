from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rental_properties_app.rental_properties import pull_list_of_properties_from_ru
# Create your views here.


class RuPropertyListing(APIView):

    def get(self, request):
        data_dicts = pull_list_of_properties_from_ru()
        return Response(data_dicts)
