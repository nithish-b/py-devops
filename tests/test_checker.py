import pytest
import requests

from py_devops.checker import check_urls

URL = "https://example.com"


def test_check_urls_success(mocker):
    mock_get = mocker.patch("py_devops.checker.requests.get")
    mock_get.return_value.ok = True
    mock_get.return_value.status_code = 200

    assert check_urls([URL]) == {URL: "200 OK"}
    mock_get.assert_called_once_with(URL, timeout=5)


def test_check_urls_failure(mocker):
    mock_get = mocker.patch("py_devops.checker.requests.get")
    mock_get.return_value.ok = False
    mock_get.return_value.status_code = 401
    mock_get.return_value.reason = "FAILED"

    assert check_urls([URL]) == {URL: "401 FAILED"}


def test_check_urls_client_error(mocker):
    mock_get = mocker.patch("py_devops.checker.requests.get")
    mock_get.return_value.ok = False
    mock_get.return_value.status_code = 404
    mock_get.return_value.reason = "Not Found"

    assert check_urls([URL]) == {URL: "404 Not Found"}
    mock_get.assert_called_once_with(URL, timeout=5)


@pytest.mark.parametrize(
    "error_exception, expected_status",
    [
        (requests.exceptions.Timeout, "TIMEOUT"),
        (requests.exceptions.ConnectionError, "CONNECTION_ERROR"),
        (requests.exceptions.RequestException, "REQUEST_ERROR"),
    ],
)
def test_check_urls_exception(mocker, error_exception, expected_status):
    mock_get = mocker.patch("py_devops.checker.requests.get")
    mock_get.side_effect = error_exception(f"{expected_status}")

    results = check_urls([URL])
    assert results == {URL: expected_status}


def test_check_urls_multiple(mocker):
    mock_get = mocker.patch("py_devops.checker.requests.get")

    # First Call: OK
    success_response = mocker.Mock(ok=True, status_code=200, reason="OK")

    # Second Call: Timeout
    timeout_exception = requests.exceptions.Timeout("Simulated Timeout")

    # Third Call: 500 Server Error
    error_response = mocker.Mock(
        ok=False, status_code=500, reason="Server Error"
    )

    mock_get.side_effect = [
        success_response,
        timeout_exception,
        error_response,
    ]

    URL1 = "https://success.com"
    URL2 = "https://timeout.com"
    URL3 = "https://failure.com"

    urls = [URL1, URL2, URL3]
    result = check_urls(urls)

    assert len(result) == 3
    assert mock_get.call_count == 3
    assert result[URL1] == "200 OK"
    assert result[URL2] == "TIMEOUT"
    assert result[URL3] == "500 Server Error"
