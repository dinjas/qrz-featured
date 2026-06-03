"""Network client for QRZ: homepage fetch + official XML API name lookup."""
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from .parse import parse_callsign_name, parse_featured_callsign, parse_session_key

USER_AGENT = "qrz-featured (+https://github.com/dinjas/qrz-featured)"
_TIMEOUT = 15


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as response:
        return response.read().decode("utf-8", errors="replace")


def get_featured_callsign():
    """Fetch the QRZ homepage and return the current featured callsign, or None."""
    return parse_featured_callsign(_get("https://www.qrz.com"))


def get_qrz_session(username, password):
    """Authenticate to the QRZ XML API and return a session key, or None."""
    url = (
        "https://xmldata.qrz.com/xml/current/"
        f"?username={urllib.parse.quote(username)}"
        f"&password={urllib.parse.quote(password)}"
        "&agent=qrz-featured"
    )
    return parse_session_key(_get(url))


def lookup_name(session_key, callsign):
    """Look up a callsign's name via the QRZ XML API, or return None."""
    url = (
        "https://xmldata.qrz.com/xml/current/"
        f"?s={session_key}&callsign={urllib.parse.quote(callsign)}"
    )
    return parse_callsign_name(_get(url))


def get_featured_member(username=None, password=None):
    """Return {'callsign', 'name', 'fetched_at'} for the current featured member.

    Raises RuntimeError if the featured callsign cannot be determined. When
    credentials are supplied, attempts an official-API name lookup; any failure
    there is non-fatal and leaves name as None.
    """
    callsign = get_featured_callsign()
    if not callsign:
        raise RuntimeError("Could not determine featured callsign")

    name = None
    if username and password:
        try:
            session_key = get_qrz_session(username, password)
            if session_key:
                name = lookup_name(session_key, callsign)
        except Exception:
            name = None

    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"callsign": callsign, "name": name, "fetched_at": fetched_at}
