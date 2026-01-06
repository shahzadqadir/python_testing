import requests


def pretty_print(data: list[dict]):
    for item in data:
        for key, value in item.items():
            print(key, value)
        print("-----")


def get_companies_list():
    response = requests.get(url="http://127.0.0.1:8000/companies/")
    return response.json()


def add_company(
    name: str, status: str = "Hiring", application_link: str = "", notes: str = ""
):
    response = requests.post(
        url="http://127.0.0.1:8000/companies/",
        json={
            "name": name,
            "status": status,
            "application_link": application_link,
            "notes": notes,
        },
    )
    return response


def main():
    pretty_print(get_companies_list())


if __name__ == "__main__":
    main()
