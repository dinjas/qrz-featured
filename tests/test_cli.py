import json

import qrz_featured.cli as cli


def test_cli_json_output(monkeypatch, capsys):
    monkeypatch.setattr(
        cli,
        "get_featured_member",
        lambda username, password: {
            "callsign": "EA7ISN",
            "name": "JOSE SALAS",
            "fetched_at": "2026-06-03T21:00:00Z",
        },
    )
    monkeypatch.delenv("QRZ_USERNAME", raising=False)
    monkeypatch.delenv("QRZ_PASSWORD", raising=False)
    exit_code = cli.main(["--json"])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert json.loads(out)["callsign"] == "EA7ISN"


def test_cli_human_output(monkeypatch, capsys):
    monkeypatch.setattr(
        cli,
        "get_featured_member",
        lambda username, password: {
            "callsign": "EA7ISN",
            "name": "JOSE SALAS",
            "fetched_at": "2026-06-03T21:00:00Z",
        },
    )
    exit_code = cli.main([])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "EA7ISN" in out
    assert "JOSE SALAS" in out


def test_cli_fetch_failure_returns_nonzero(monkeypatch, capsys):
    def boom(username, password):
        raise RuntimeError("Could not determine featured callsign")

    monkeypatch.setattr(cli, "get_featured_member", boom)
    exit_code = cli.main(["--json"])
    assert exit_code != 0
