import requests

from random import uniform


def print_response(res: requests.Response) -> None:
    print(f"status code: {res.status_code}\njson out: {res.json()}", end="\n\n")


response = requests.get("http://localhost:8000")
print_response(response)

response = requests.post(
    url="http://localhost:8000/predict",
    json={
        "sepal_length": uniform(6.0, 7.0),
        "sepal_width": uniform(2.8, 3.5),
        "petal_length": uniform(4.0, 6.0),
        "petal_width": uniform(1.2, 2.8)
    }
)
print_response(response)

response = requests.post(
    url="http://localhost:8000/predict",
    json={
        "sepal_length": uniform(6.0, 7.0),
        "sepal_width": uniform(2.8, 3.5),
        "petal_length": uniform(4.0, 6.0),
        "petal_width": uniform(1.2, 2.8)
    }
)
print_response(response)


