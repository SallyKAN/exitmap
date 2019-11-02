import error
import torsocks

TARGET_DOMAIN = "whoami.akamai.net"

def main():
    sock = torsocks.torsocket()
    sock.settimeout(10)

    # Resolve the domain using Tor's SOCKS extension.
    try:
        ipv4 = sock.resolve(TARGET_DOMAIN)
        print ipv4
    except error.SOCKSv5Error as err:

    # This is expected because all domains resolve to 127.0.0.1.
        print ("SOCKSv5 error while resolving domain: %s" % err)

if __name__ == '__main__':
    main()