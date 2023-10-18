from fastapi.testclient import TestClient
import pytest
from src.homework.main import app, check_json_header
from fastapi import HTTPException
from typing import Dict

client = TestClient(app)


@pytest.mark.parametrize('headers', [
    {'user-agent': 'my-app/0.0.1'},
    {'content-type': 'application/json'},
    {}
])
@pytest.mark.parametrize('params', [
    {'tinkoff': 'academy'},
    {'backend': 'top'},
    {}
])
def test_read_hello(headers: Dict[str, str], params: Dict[str, str]) -> None:
    response = client.get("/hello", params=params, headers=headers)
    assert 'Content-Type' in response.headers
    assert 'text/plain' in response.headers['Content-Type']
    assert response.status_code == 200
    assert response.text == "HSE One Love!"


@pytest.mark.parametrize('endpoint', ['/hello', '/divide', '/set', '/get/key'])
def test_not_allowed(endpoint: str) -> None:
    response = client.put(endpoint)
    assert response.status_code == 405

    response = client.get("/another_endpoint")
    assert response.status_code == 405


@pytest.mark.parametrize('data', [
    {'key': 'rock', 'value': 'solid'},
    {'key': 'air', 'value': 'gas', 'dummy': 'stub'},
])
def test_save_data(data: Dict[str, str]) -> None:
    response = client.post("/set", json=data)
    assert response.status_code == 200


@pytest.mark.parametrize('headers', [
    'text/plain; charset=utf-8',
    None,
])
def test_check_json_header(headers: str | None) -> None:
    with pytest.raises(HTTPException) as exc:
        check_json_header(headers)
    assert exc.value.status_code == 415


@pytest.mark.parametrize('data', [
    {'key': 'rock'},
    {'value': 'gas'},
    {}
])
def test_save_data_bad_request(data: Dict[str, str]) -> None:
    response = client.post("/set", json=data)
    assert response.status_code == 400


def test_read_key() -> None:
    client.post("/set", json={'key': 'rock', 'value': 'solid'})
    response = client.get("/get/rock")
    assert response.json() == {"key": "rock", "value": "solid"}
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'


def test_read_key_not_found() -> None:
    response = client.get("/get/object")
    assert response.status_code == 404


@pytest.mark.parametrize('data, expected_result', [
    ({'dividend': '5', 'divider': '2'}, '2.5'),
    ({'dividend': '21', 'divider': '7'}, '3.0'),
])
def test_divide(data: Dict[str, str], expected_result: str) -> None:
    response = client.post("/divide", json=data)
    assert 'Content-Type' in response.headers
    assert 'text/plain' in response.headers['Content-Type']
    assert response.status_code == 200
    assert response.text == expected_result


def test_divide_zero_division() -> None:
    response = client.post("/divide", json={'dividend': '5', 'divider': '0'})
    assert response.status_code == 400


@pytest.mark.parametrize('data', [
    {'dividend': '5'},
    {'divider': '7'},
    {}
])
def test_divide_bad_data(data: Dict[str, str]) -> None:
    response = client.post("/divide", json=data)
    assert response.status_code == 400
