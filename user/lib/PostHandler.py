from django.conf import settings
import json

def dprint(content):
    if settings.DEBUG:
        print('[DEBUG] ' + content)

class PostHandler():
    request = None # static member variable
    str = None #static member variable
    json = None # static member variable
    check_list = {
        "login1": ["username"],
        "login2": ["username", "password", "remember"],
        "register": ["username", "password"]
    }

    def __init__(self, request):
        self.request = request

    def getData(self, key):
        try:
            self.str = self.str or self.request.POST[key]
            return self.str
        except (KeyError):
            dprint('Key "json" not found')
            return

    def getJson(self):
        self.getData('json')
        if self.str:
            self.json = self.json or json.loads(self.str)
            return self.json
        else:
            return

    def checkKey(self, method):
        self.getJson()
        if not self.json:
            dprint('No json is get.')
            return False
        for i, v in enumerate(self.check_list[method]):
            if not (v in self.json):
                dprint('Check method "' + method + '" failed, key "' + v + '" not found.')
                return False
        dprint('Method "' + method + '" data check passed.')
        return True

    def __del__(self):
        self.request = None
        return


class ERR():
    MISSING_JSON = 'No required json.'
    MISSING_DATA = 'No required data.'
    USERNAME_OR_PASSWORD_INCORRECT = 'Username or password incorrect.'
    SESSION_EXPIRED = 'Session expired.'
    ALREADY_LOGGED_IN = 'Already logged in. Logout before logging in.'
    REQUIRE_LOGIN = 'Require login.'