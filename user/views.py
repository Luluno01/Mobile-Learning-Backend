from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseForbidden
from django.conf import settings
from django.shortcuts import render

from .lib.PostHandler import PostHandler, ERR, dprint
from .models import User, UserInfo, Avatar

debug = settings.DEBUG

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

def loginStateMaintainer(func):
    def wrapper(request, *args):
        if User.isLoggedIn(request):
            request.session['loginState'] = True # Refresh login state
        if 'reset' in request.session:
            request.session['reset'] = False
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
    if request.method == 'GET' or request.method == 'get': # Generate static salt
        staticSalt = User.mksalt()
        request.session['staticSalt'] = staticSalt
        dprint('Register stage 1: generate staticSalt.')
        return HttpResponse(staticSalt)
    else:
        postHandler = PostHandler(request)
        if postHandler.getData('json'):
            dprint('Post string: ' + postHandler.str)
            if postHandler.checkKey('register'):
                if 'staticSalt' in request.session: # Start register
                    try:
                        user = User.objects.get(username=postHandler.json['username'])
                        dprint('Register error: username clashed.')
                        return HttpResponseNotAllowed(ERR.USERNAME_CLASH)
                    except User.DoesNotExist:
                        user = User.newUser(postHandler.json['username'], postHandler.json['password'], request.session['staticSalt'])
                        request.session['userId'] = user.id
                        request.session['loginState'] = True
                        request.session.set_expiry(30 * 24 * 3600)
                        dprint('User created. User id: %d. ' % user.id + 'Username: ' + user.username)
                        return HttpResponse('Registered. Welcome, ' + user.username)
                else:
                    dprint('Attempt to register without a staticSalt on server.')
                    return HttpResponseBadRequest(ERR.SESSION_EXPIRED)
            else:
                return HttpResponseBadRequest(ERR.MISSING_DATA)
        else:
            return HttpResponseBadRequest(ERR.MISSING_JSON)

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
                            dprint('Logged in. User id: %d. ' % user.id + 'Username: ' + user.username)
                            request.session['userId'] = user.id
                            request.session['loginState'] = True
                            if postHandler.json['remember']:
                                request.session.set_expiry(30 * 24 * 3600)
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
                    user = User.objects.get(username=postHandler.json['username'])
                    dprint('User found.')
                    staticSalt = user.password_salt
                except User.DoesNotExist: # Generate fake static salt
                    dprint('User not found.')
                    staticSalt = User.mksalt()
                return HttpResponse('{"staticSalt":"' + staticSalt + '","dynamicSalt":"' + dynamicSalt + '"}')
            else:
                return HttpResponseBadRequest(ERR.MISSING_DATA)
        else:
            return HttpResponseBadRequest(ERR.MISSING_JSON)

@requireLogin
def logout(request, query = ''):
    if (request.method == 'GET' or request.method == 'get'):
        return HttpResponseBadRequest()
    else: # Logout
        request.session['loginState'] = False
        request.session.flush()
        dprint('Logout.')
        return HttpResponse('Logout.')

@requireLogin
def reset(request, query = ''):
    if request.method.lower() == 'get':
        return HttpResponseBadRequest()
    else: # Confirm password
        postHandler = PostHandler(request)
        if postHandler.getData('json'):
            dprint('Post string: ' + postHandler.str)
            if postHandler.checkKey('reset3'):
                if not ('reset' in request.session and request.session['reset']):
                    dprint('Invalid reset operation.')
                    return HttpResponseNotAllowed(ERR.INVALID_OPERATION)
                if 'newStaticSalt' in request.session:
                    if postHandler.json['userId'] != request.session['userId']:
                        # Suspicious behavior detected
                        dprint('User id not match. User id in session: %d.' % request.session['userId'])
                        request.session.flush()
                        return HttpResponseBadRequest(ERR.USER_ID_NOT_MATCH)
                    user = User.objects.get(id=request.session['userId'])
                    user.password_salt = request.session['newStaticSalt']
                    user.password = postHandler.json['newPassword']
                    user.save()
                    dprint('New password set. Require re-login.')
                    request.session.flush()
                    return HttpResponse('New password set. Require re-login.')
                else:
                    dprint('Attempt to reset password without a new static salt.')
                    return HttpResponseBadRequest(ERR.SESSION_EXPIRED)
            elif postHandler.checkKey('reset2'):
                if 'dynamicSalt' in request.session:  # Start old (current) password validating
                    try:
                        user = User.objects.get(username=postHandler.json['username'])
                        if (not 'userId' in request.session) or (request.session['userId'] != user.id):
                            dprint('Attempt to reset another user\' password.')
                            return HttpResponseBadRequest(ERR.USERNAME_NOT_MATCH)
                        if user.checkPassword(postHandler.json['password'],
                                              request.session['dynamicSalt']):  # Check password here
                            newStaticSalt = User.mksalt()
                            request.session['newStaticSalt'] = newStaticSalt
                            res = HttpResponse('{userId:"%d",' % user.id + 'newStaticSalt:"' + newStaticSalt + '"}')
                            dprint('Old password confirmed. User id: %d. ' % user.id + 'Username: ' + user.username)
                            request.session['reset'] = True
                            request.session.set_expiry(0)
                        else:
                            dprint('Password incorrect.')
                            res = HttpResponseBadRequest(ERR.PASSWORD_INCORRECT)
                        return res
                    except User.DoesNotExist:
                        dprint('User not found.')
                        return HttpResponseBadRequest(ERR.USERNAME_NOT_MATCH)
                else:
                    dprint('Attempt to verify old password without generating dynamicSalt.')
                    return HttpResponseBadRequest(ERR.SESSION_EXPIRED)
            elif postHandler.checkKey('reset1'):
                dynamicSalt = User.mksalt()
                request.session['dynamicSalt'] = dynamicSalt
                staticSalt = ''
                try:
                    user = User.objects.get(username=postHandler.json['username'])
                    dprint('User found.')
                    if not ('userId' in request.session) or (user.id != request.session['userId']):
                        dprint('Attempt to reset another user\' password.')
                        staticSalt = User.mksalt() # Fake salt
                    staticSalt = user.password_salt
                except User.DoesNotExist:  # Generate fake static salt
                    dprint('User not found.')
                    staticSalt = User.mksalt()
                return HttpResponse('{"staticSalt":"' + staticSalt + '","dynamicSalt":"' + dynamicSalt + '"}')
            else:
                return HttpResponseBadRequest(ERR.MISSING_DATA)
        else:
            return HttpResponseBadRequest(ERR.MISSING_JSON)
