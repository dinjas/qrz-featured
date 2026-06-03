from pathlib import Path

from qrz_featured.parse import (
    parse_featured_callsign,
    parse_session_key,
    parse_callsign_name,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_featured_callsign():
    html = (FIXTURES / "homepage.html").read_text()
    assert parse_featured_callsign(html) == "EA7ISN"


def test_parse_featured_callsign_missing():
    assert parse_featured_callsign("<html><body>nothing</body></html>") is None


def test_parse_session_key():
    xml = (FIXTURES / "session.xml").read_text()
    assert parse_session_key(xml) == "abc123sessionkey"


def test_parse_callsign_name():
    xml = (FIXTURES / "callsign.xml").read_text()
    assert parse_callsign_name(xml) == "JOSÉ ANTONIO SALAS CABRERA"


def test_parse_callsign_name_missing():
    xml = (
        '<QRZDatabase xmlns="http://xmldata.qrz.com">'
        "<Session><Key>k</Key></Session></QRZDatabase>"
    )
    assert parse_callsign_name(xml) is None
