#!/usr/bin/env python2

# Copyright 2013-2017 Philipp Winter <phw@nymity.ch>
#
# This file is part of exitmap.
#
# exitmap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# exitmap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with exitmap.  If not, see <http://www.gnu.org/licenses/>.

"""
Module to detect false negatives for <https://check.torproject.org>.
"""

import sys
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from util import exiturl

log = logging.getLogger(__name__)

HOST = "bobsblog.australia.ai"
USER = "bob"
PASS = "f=~uzR]hz*mpZQtStTuXLQti("

# exitmap needs this variable to figure out which relays can exit to the given
# destination(s).

destinations = [(HOST, 80)]


def fetch_page(exit_fpr):
    """
    Fetch check.torproject.org and see if we are using Tor.
    """

    exit_url = exiturl(exit_fpr)

    with webdriver.Firefox() as driver:
        driver.get("http://{}/wp-login.php".format(HOST))

        if "WordPress" not in driver.title:
            log.critical("%s gave login page title: %s", exit_url, driver.title)
            return

        time.sleep(1)

        elem = driver.find_element_by_id("user_login")
        if not elem:
            log.critical("%s login page does not have login field", exit_url)
            return
        elem.send_keys(USER)

        time.sleep(1)

        elem = driver.find_element_by_id("user_pass")
        if not elem:
            log.critical("%s login page does not have password field", exit_url)
            return
        elem.send_keys(PASS)

        time.sleep(1)
        elem.send_keys(Keys.RETURN)

        time.sleep(10)

        if "WordPress" not in driver.title or "Dashboard" not in driver.title:
            log.warning("%s did not load dashboard page, title: %s", exit_url, driver.title)
            return


def probe(exit_desc, run_python_over_tor, run_cmd_over_tor, **kwargs):
    """
    Probe the given exit relay and look for check.tp.o false negatives.
    """

    run_python_over_tor(fetch_page, exit_desc.fingerprint)


def main():
    """
    Entry point when invoked over the command line.
    """

    fetch_page("bogus-fingerprint")

    return 0


if __name__ == "__main__":
    sys.exit(main())
