# qrz-featured

Look up the current [QRZ.com](https://www.qrz.com) **Featured Member** — the
ham radio operator highlighted on the QRZ homepage right now.

> **Unofficial.** Not affiliated with or endorsed by QRZ LLC / qrz.com.

## Install

```bash
pip install git+https://github.com/dinjas/qrz-featured
```

## Use

```bash
# Just the current featured callsign:
qrz-featured

# Include the member's name (requires a QRZ XML API subscription):
QRZ_USERNAME=yourcall QRZ_PASSWORD=secret qrz-featured

# Machine-readable:
qrz-featured --json
# {"callsign": "EA7ISN", "name": "JOSÉ ANTONIO SALAS CABRERA", "fetched_at": "..."}
```

As a library:

```python
from qrz_featured import get_featured_member
print(get_featured_member())
```

## How it works

The featured member appears only on the QRZ homepage, so the callsign is read
from the homepage HTML. The optional name lookup uses the official QRZ XML API
with your credentials. One request per run.

## License

MIT
