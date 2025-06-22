from typer.testing import CliRunner

from cli.iceyCLI.__main__ import app

runner = CliRunner()


def test_cli_cycle(tmp_path, monkeypatch):
    # isolate ~/.icey
    monkeypatch.setattr("cli.iceyCLI.__main__.STATE_DIR", tmp_path)
    monkeypatch.setattr("cli.iceyCLI.__main__.store.root", tmp_path)
    email = "bob@example.com"
    assert runner.invoke(app, ["create", email]).exit_code == 0
    assert runner.invoke(app, ["save", email]).exit_code == 0
    result = runner.invoke(app, ["load", email])
    assert result.exit_code == 0
    assert '"user_email": "bob@example.com"' in result.stdout
