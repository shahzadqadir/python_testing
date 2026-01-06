import json
import pytest
from unittest import TestCase

from django.test import Client
from django.urls import reverse_lazy

from companies.models import Company

companies_url = reverse_lazy("companies-list")
client = Client()


@pytest.mark.django_db
def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


@pytest.mark.django_db
def test_one_company_exists_should_succeed(client):
    amazon = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    response_content = response.json()[0]
    assert response.status_code == 200
    assert response_content.get("name") == "Amazon"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""
    amazon.delete()


# Post Request Related Tests

@pytest.mark.django_db
def test_create_company_without_arguments_should_fail(client) -> None:
    response = client.post(
        path=companies_url
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_existing_company_should_fail(client) -> None:
    Company.objects.create(name="apple")
    response = client.post(
        path=companies_url, data={"name": "apple"}
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_company_with_only_name_all_other_fields_default(client):
    response = client.post(
        path=companies_url, data={"name": "blank"}
    )
    assert response.status_code == 201
    response_content = response.json()
    assert response_content.get("name") == "blank"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("notes") == ""


@pytest.mark.django_db
def test_create_company_with_wrong_status_should_fail(client):
    response = client.post(
        path=companies_url, data={"name": "newCompany", "status": "wrongStatus"}
    )
    assert response.status_code == 400
    assert "is not a valid choice" in str(response.content)


@pytest.mark.xfail
def test_known_bug_ok_to_fail():
    assert 1 == 2


@pytest.mark.skip
def test_known_bug_should_be_skipped():
    pass
