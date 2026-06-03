"""Pytest configuration: stub out qrz_featured.client until it is implemented."""
import sys
import types

# Create a minimal stub so that `from qrz_featured.parse import ...` does not
# fail because __init__.py also imports from .client (a later task).
_stub = types.ModuleType("qrz_featured.client")
_stub.get_featured_callsign = None
_stub.get_qrz_session = None
_stub.lookup_name = None
_stub.get_featured_member = None
sys.modules["qrz_featured.client"] = _stub
