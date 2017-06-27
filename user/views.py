from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.conf import settings
from django.shortcuts import render
from datetime import timedelta

from .lib.PostHandler import PostHandler, ERR, dprint
from .models import User

debug = settings.DEBUG

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

def loginStateMaintainer(func):
    def wrapper(request, *args):
        if User.isLoggedIn(request):
            request.session['loginState'] = True # Refresh login state
        return func(request, *args)
    return wrapper

def requireLogin(func):
    def wrapper(request, *args):
        if User.isLoggedIn(request):
            return func(request, *args)
        else:
            return HttpResponseUnauthorized(ERR.REQUIRE_LOGIN)
    return wrapper

@loginStateMaintainer
def state(request):
    res = '1' if User.isLoggedIn(request) else '0'
    dprint('Login state check: ' + res)
    return HttpResponse(res)

def register(request, query = ''):
    return HttpResponse('<h1>Register</h1>')

@loginStateMaintainer
def login(request, query = ''):
    if(request.method == 'GET' or request.method == 'get'):
        return render(request, 'user/login.html')
    else:
        postHandler = PostHandler(request)
        if postHandler.getData('json'):
            dprint('Post string: ' + postHandler.str)
            if postHandler.checkKey('login2'):
                if User.isLoggedIn(request): # Already logged in
                    dprint('Already logged in.')
                    return HttpResponseNotAllowed(ERR.ALREADY_LOGGED_IN)
                if 'dynamicSalt' in request.session: # Start login validating
                    try:
                        user = User.objects.get(username=postHandler.json['username'])
                        if user.checkPassword(postHandler.json['password'], request.session['dynamicSalt']): # Check password here
                            res = HttpResponse('Logged in.')
                            request.session['loginState'] = True
                            if postHandler.json['remember']:
                                request.session.set_expiry(timedelta(days=30))
                            else:
                                request.session.set_expiry(0)
                        else:
                            dprint('Password incorrect.')
                            res = HttpResponseBadRequest(ERR.USERNAME_OR_PASSWORD_INCORRECT)
                        return res
                    except User.DoesNotExist:
                        dprint('User not found.')
                        return HttpResponseBadRequest(ERR.USERNAME_OR_PASSWORD_INCORRECT)
                else:
                    dprint('Attempt to login without generating dynamicSalt.')
                    return HttpResponseBadRequest(ERR.SESSION_EXPIRED)
            elif postHandler.checkKey('login1'):
                dynamicSalt = User.mksalt()
                request.session['dynamicSalt'] = dynamicSalt
                staticSalt = ''
                try:
                    user = User.objects.get(username=
                                            postHandler.json['username'])
                    dprint('User found.')
                    staticSalt = user.password_salt
                except User.DoesNotExist: # Generate fake static salt
                    dprint('User not found.')
                    staticSalt = User.mksalt()
                return HttpResponse('{"staticSalt":"' + staticSalt + '","dynamicSalt":"' + dynamicSalt + '"}')
            else:
                res = HttpResponseBadRequest(ERR.MISSING_DATA)
                return res
        else:
            res =  HttpResponseBadRequest(ERR.MISSING_JSON)
            return res

@loginStateMaintainer
@requireLogin
def reset(request, query = ''):
    return HttpResponse('<h1>reset</h1>')
