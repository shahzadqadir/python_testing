import json
import pytest
from unittest import TestCase

from django.test import Client
from django.urls import reverse_lazy

from companies.models import Company


@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.companies_url = reverse_lazy("companies-list")


class TestGetCompanies(BasicCompanyAPITestCase):

    def test_zero_companies_should_return_empty_list(self) -> None:
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), [])

    def test_one_company_exists_should_succeed(self):
        amazon = Company.objects.create(name="Amazon")
        response = self.client.get(self.companies_url)
        response_content = response.json()[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content.get("name"), "Amazon")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

        amazon.delete()
