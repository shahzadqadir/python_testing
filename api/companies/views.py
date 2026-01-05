from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from api.companies.models import Company
from .serializers import CompanySerializer


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by("last_update")
