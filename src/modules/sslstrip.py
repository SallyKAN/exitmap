import subprocess
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

from util import exiturl

import stem.descriptor.server_descriptor as descriptor
import sys
import logging
import requests

log = logging.getLogger(__name__)

destinations = [("grc.com", 443)]
TEST_URL = "http://login.yahoo.com"


def check_sslstrip(exit_desc):
    exit_url = exiturl(exit_desc.fingerprint)
    log.debug("Probing exit relay %s." % exit_url)
    output = None
    try:
        output = requests.get(TEST_URL)
        url = output.url
    except Exception as err:
        log.warning("urllib2.urlopen for %s says: %s." %
                    (exit_desc.fingerprint, err))
        return
    if not output:
        log.warning("Exit relay %s did not return data." % exit_url)
        return
    if "https" not in url:
        log.warning("Possible SSL Strip attacks by %s: %s." % (exit_url, output))
    else:
        log.debug("Exit relay %s worked fine." % exit_url)


def probe(exit_desc, run_python_over_tor, run_cmd_over_tor, **kwargs):
    """
    Attempts to fetch a decoy SSH server public key fingerprint and yells if this fails.
    """

    run_python_over_tor(check_sslstrip, exit_desc)

def main():
    """
    Entry point when invoked over the command line.
    """

    desc = descriptor.ServerDescriptor("")
    desc.fingerprint = "bogus"
    check_sslstrip(desc)

    return 0


if __name__ == "__main__":
    sys.exit(main())