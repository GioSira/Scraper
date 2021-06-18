import hashlib


def _sha_url(self, url):
    m = hashlib.sha256()
    m.update(url.encode('utf-8'))
    return m.hexdigest()
