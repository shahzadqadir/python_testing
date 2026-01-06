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

    def tearDown(self):
        pass


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


class TestPostCompanies(BasicCompanyAPITestCase):

    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(
            path=self.companies_url
        )
        self.assertEqual(response.status_code, 400)

    def test_create_existing_company_should_fail(self) -> None:
        Company.objects.create(name="apple")
        response = self.client.post(
            path=self.companies_url, data={"name": "apple"}
        )
        self.assertEqual(response.status_code, 400)

    def test_create_company_with_only_name_all_other_fields_default(self):
        response = self.client.post(
            path=self.companies_url, data={"name": "blank"}
        )
        self.assertEqual(response.status_code, 201)
        response_content = response.json()
        self.assertEqual(response_content.get("name"), "blank")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_wrong_status_should_fail(self):
        response = self.client.post(
            path=self.companies_url, data={"name": "newCompany", "status": "wrongStatus"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("is not a valid choice", str(response.content))

    @pytest.mark.xfail
    def test_known_bug_ok_to_fail(self):
        self.assertEqual(1, 2)

    @pytest.mark.skip
    def test_known_bug_should_be_skipped(self):
        pass