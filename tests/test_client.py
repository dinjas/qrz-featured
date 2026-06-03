import qrz_featured.client as client


def test_get_featured_member_without_credentials(monkeypatch):
    monkeypatch.setattr(client, "get_featured_callsign", lambda: "EA7ISN")
    result = client.get_featured_member()
    assert result["callsign"] == "EA7ISN"
    assert result["name"] is None
    assert "fetched_at" in result and result["fetched_at"].endswith("Z")


def test_get_featured_member_with_credentials(monkeypatch):
    monkeypatch.setattr(client, "get_featured_callsign", lambda: "EA7ISN")
    monkeypatch.setattr(client, "get_qrz_session", lambda u, p: "key")
    monkeypatch.setattr(client, "lookup_name", lambda k, c: "JOSE SALAS")
    result = client.get_featured_member(username="u", password="p")
    assert result["callsign"] == "EA7ISN"
    assert result["name"] == "JOSE SALAS"


def test_get_featured_member_name_lookup_failure_is_nonfatal(monkeypatch):
    monkeypatch.setattr(client, "get_featured_callsign", lambda: "EA7ISN")

    def boom(u, p):
        raise RuntimeError("api down")

    monkeypatch.setattr(client, "get_qrz_session", boom)
    result = client.get_featured_member(username="u", password="p")
    assert result["callsign"] == "EA7ISN"
    assert result["name"] is None


def test_get_featured_member_fetch_failure_raises(monkeypatch):
    monkeypatch.setattr(client, "get_featured_callsign", lambda: None)
    try:
        client.get_featured_member()
    except RuntimeError:
        return
    raise AssertionError("expected RuntimeError when callsign cannot be found")
