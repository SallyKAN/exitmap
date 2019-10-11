import subprocess
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

from util import exiturl

import stem.descriptor.server_descriptor as descriptor
import sys
import logging

log = logging.getLogger(__name__)

destinations = [("grc.com", 443)]



def fetch_ssh_fingerprint(exit_desc):
    ssh_public_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGf8f/Q51D5WWAsxk26Cegv9DGn/jl4K6If0UnP7z5i9"
    ssh_ip = "52.237.232.233"
    exit_url = exiturl(exit_desc.fingerprint)
    log.debug("Probing exit relay %s." % exit_url)

    output = None
    try:
        output = subprocess.check_output("ssh-keyscan %s 2>&1" % ssh_ip, shell=True)
    except Exception as err:
        log.warning("urllib2.urlopen for %s says: %s." %
                    (exit_desc.fingerprint, err))
        return

    if not output:
        log.warning("Exit relay %s did not return data." % exit_url)
        return

    # data = data.strip()
    output = output.decode("utf-8")
    # print(output)
    if ssh_public_key not in output:
        log.warning("Possible SSH MitM attack by %s: %s." % (exit_url, output))
    else:
        log.debug("Exit relay %s worked fine." % exit_url)


def probe(exit_desc, run_python_over_tor, run_cmd_over_tor, **kwargs):
    """
    Attempts to fetch a decoy SSH server public key fingerprint and yells if this fails.
    """

    run_python_over_tor(fetch_ssh_fingerprint, exit_desc)
    # run_python_over_tor(fetch_cert, exit_desc)


def main():
    """
    Entry point when invoked over the command line.
    """

    desc = descriptor.ServerDescriptor("")
    desc.fingerprint = "bogus"
    fetch_ssh_fingerprint(desc)

    return 0


if __name__ == "__main__":
    sys.exit(main())
