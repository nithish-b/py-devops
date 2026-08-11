from click.testing import CliRunner

from py_devops.cli import main


def test_no_urls():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.exit_code == 0
    assert "Usage: check-urls <URL1> <URL2>" in result.output


def test_main_single_url_success(mocker):
    url = "https://www.example.com"
    mock_check = mocker.patch("py_devops.cli.check_urls")

    mock_check.return_value = {url: "200 OK"}
    runner = CliRunner()
    result = runner.invoke(main, [url])

    assert result.exit_code == 0
    mock_check.assert_called_once_with((url,), 5)
