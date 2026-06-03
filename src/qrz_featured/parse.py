"""Pure parsing functions for QRZ data. No network access."""
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

_NS = {"q": "http://xmldata.qrz.com"}


class _FeaturedMemberParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._in_featured_strong = False
        self._found_featured_section = False
        self._link_depth = 0
        self.featured_callsign = None

    def handle_starttag(self, tag, attrs):
        if tag == "strong":
            self._in_featured_strong = True
        if self._found_featured_section and tag == "a":
            self._link_depth += 1

    def handle_endtag(self, tag):
        if tag == "strong":
            self._in_featured_strong = False
        if self._found_featured_section and tag == "a":
            self._link_depth -= 1

    def handle_data(self, data):
        if self._in_featured_strong and "Featured Member" in data:
            self._found_featured_section = True
        if (
            self._found_featured_section
            and self._link_depth > 0
            and self.featured_callsign is None
        ):
            callsign = data.strip()
            if callsign:
                self.featured_callsign = callsign


def parse_featured_callsign(html):
    """Return the featured callsign from QRZ homepage HTML, or None."""
    parser = _FeaturedMemberParser()
    parser.feed(html)
    return parser.featured_callsign


def parse_session_key(xml_text):
    """Return the session Key from a QRZ XML API session response, or None."""
    root = ET.fromstring(xml_text)
    session = root.find("q:Session", _NS)
    if session is None:
        return None
    key = session.find("q:Key", _NS)
    return key.text if key is not None else None


def parse_callsign_name(xml_text):
    """Return 'fname name' from a QRZ XML API callsign response, or None."""
    root = ET.fromstring(xml_text)
    record = root.find("q:Callsign", _NS)
    if record is None:
        return None
    fname = record.find("q:fname", _NS)
    name = record.find("q:name", _NS)
    parts = [p.text for p in (fname, name) if p is not None and p.text]
    return " ".join(parts) if parts else None
