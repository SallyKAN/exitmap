import sys
import re
import logging
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

from util import exiturl

import stem.descriptor.server_descriptor as descriptor
import ssl
from M2Crypto import X509

log = logging.getLogger(__name__)

destinations = [("grc.com", 443)]


def fetch_cert(exit_desc):

    expected = "159A76C5AEF4901579E6A49996C1D6A1D93B0743"
    exit_url = exiturl(exit_desc.fingerprint)
    log.debug("Probing exit relay %s." % exit_url)

    data = None
    try:
        hostname = "grc.com"
        port = 443
        conn = ssl.create_connection((hostname,port))
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sock = context.wrap_socket(conn, server_hostname=hostname)
        certificate = ssl.DER_cert_to_PEM_cert(sock.getpeercert(True))
        x509 = X509.load_cert_string(certificate, X509.FORMAT_PEM)
        data = x509.get_fingerprint('sha1')

    except Exception as err:
        log.warning("urllib2.urlopen for %s says: %s." %
                    (exit_desc.fingerprint, err))
        return

    if not data:
        log.warning("Exit relay %s did not return data." % exit_url)
        return

    # data = data.strip()

    if not re.match(expected, data):
        log.warning("Possible HTTPS MitM attack by %s: %s." % (exit_url, data))
    else:
        log.debug("Exit relay %s worked fine." % exit_url)


def probe(exit_desc, run_python_over_tor, run_cmd_over_tor, **kwargs):
    """
    Attempts to fetch a small web page and yells if this fails.
    """

    run_python_over_tor(fetch_cert, exit_desc)


def main():
    """
    Entry point when invoked over the command line.
    """

    desc = descriptor.ServerDescriptor("")
    desc.fingerprint = "bogus"
    fetch_cert(desc)

    return 0

if __name__ == "__main__":
    sys.exit(main())
