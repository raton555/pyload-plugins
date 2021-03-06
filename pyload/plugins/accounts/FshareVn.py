# -*- coding: utf-8 -*-

import re
import time

from ..internal.Account import Account
from ..internal.misc import parse_html_form


class FshareVn(Account):
    __name__ = "FshareVn"
    __type__ = "account"
    __version__ = "0.20"
    __status__ = "testing"

    __description__ = """Fshare.vn account plugin"""
    __license__ = "GPLv3"
    __authors__ = [("zoidberg", "zoidberg@mujmail.cz"),
                   ("stickell", "l.stickell@yahoo.it"),
                   ("GammaC0de", "nitzo2001[AT]yahoo[DOT]com")]

    VALID_UNTIL_PATTERN = r'</span> Expire: (.+?)</p>'
    LIFETIME_PATTERN = ur'<dt>Lần đăng nhập trước:</dt>\s*<dd>.+?</dd>'
    TRAFFIC_LEFT_PATTERN = r'<p>Used: ([\d.,]+) (?:([\w^_]+)) / ([\d.,]+) (?:([\w^_]+))</p>'

    def grab_info(self, user, password, data):
        html = self.load("https://www.fshare.vn")

        m = re.search(self.TRAFFIC_LEFT_PATTERN, html)
        trafficleft = (self.parse_traffic(m.group(3), m.group(4)) - self.parse_traffic(m.group(1), m.group(2))) if m else None

        if re.search(self.LIFETIME_PATTERN, html):
            self.log_debug("Lifetime membership detected")
            return {'validuntil': -1,
                    'trafficleft': trafficleft,
                    'premium': True}

        m = re.search(self.VALID_UNTIL_PATTERN, html)
        if m is not None:
            premium = True
            validuntil = time.mktime(time.strptime(m.group(1) + " 23:59:59", '%d-%m-%Y %H:%M:%S'))

        else:
            premium = False
            validuntil = None
            trafficleft = None

        return {'validuntil': validuntil,
                'trafficleft': trafficleft,
                'premium': premium}

    def signin(self, user, password, data):
        html = self.load("https://www.fshare.vn/location/en")
        if 'href="/logout"' in html:
            self.skip_login()

        url, inputs = parse_html_form('id="login-form"', html)
        if inputs is None:
            self.fail_login("Login form not found")

        inputs.update({'LoginForm[email]': user,
                       'LoginForm[password]': password,
                       'LoginForm[rememberMe]': 1,
                       'yt0': "Login"})

        html = self.load("https://www.fshare.vn/login", post=inputs)
        if not 'href="/logout"' in html:
            self.fail_login()
