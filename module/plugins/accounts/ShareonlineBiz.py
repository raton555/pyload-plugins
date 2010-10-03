# -*- coding: utf-8 -*-

"""
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License,
    or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, see <http://www.gnu.org/licenses/>.
    
    @author: mkaay
"""

from module.plugins.Account import Account
from time import strptime, mktime
import re

class ShareonlineBiz(Account):
    __name__ = "ShareonlineBiz"
    __version__ = "0.2"
    __type__ = "account"
    __description__ = """share-online.biz account plugin"""
    __author_name__ = ("mkaay")
    __author_mail__ = ("mkaay@mkaay.de")
    
    def loadAccountInfo(self, user):
        req = self.getAccountRequest(user)
        src = req.load("http://www.share-online.biz/members.php?setlang=en")
        validuntil = re.search(r'<td align="left"><b>Package Expire Date:</b></td>\s*<td align="left">(\d+/\d+/\d+)</td>', src).group(1)
        validuntil = int(mktime(strptime(validuntil, "%m/%d/%y")))

        tmp = {"validuntil":validuntil, "trafficleft":-1}
        return tmp
        
    def login(self, user, data):
        req = self.getAccountRequest(user)
        post_vars = {
                        "act": "login",
                        "location": "index.php",
                        "dieseid": "",
                        "user": user,
                        "pass": data["password"],
                        "login": "Login"
                    }
        req.lastURL = "http://www.share-online.biz/"
        req.load("https://www.share-online.biz/login.php", cookies=True, post=post_vars)
