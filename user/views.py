from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render

from .lib.ReqHandler import ReqHandler, ERR, dprint
from .models import User, UserInfo, Avatar

debug = settings.DEBUG

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

class HttpResponseNotFound(HttpResponse):
    status_code = 404

class HttpResponseConflict(HttpResponse):
    status_code = 409

def loginStateMaintainer(func):
    def wrapper(request, *args, **kwargs):
        if User.isLoggedIn(request):
            request.session['loginState'] = True # Refresh login state
        if 'reset' in request.session:
            request.session['reset'] = False
        return func(request, *args, **kwargs)
    return wrapper

def requireLogin(func):
    def wrapper(*args, **kwargs):
        if type(args[0]) == type:  # classmethod
            request = args[1]
        else:
            request = args[0]
        if User.isLoggedIn(request):
            return func(*args, **kwargs)
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
        reqHandler = ReqHandler(request)
        if reqHandler.getData('json'):
            dprint('Post string: ' + reqHandler.str)
            if reqHandler.checkKey('register'):
                if 'staticSalt' in request.session: # Start register
                    try:
                        user = User.objects.get(username=reqHandler.json['username'])
                        dprint('Register error: username clashed.')
                        return HttpResponseConflict(ERR.USERNAME_CLASH)
                    except User.DoesNotExist:
                        user = User.newUser(reqHandler.json['username'], reqHandler.json['password'], request.session['staticSalt'])
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
        return render(request, 'user/csrf.html')
    else:
        reqHandler = ReqHandler(request)
        if reqHandler.getData('json'):
            dprint('Post string: ' + reqHandler.str)
            if reqHandler.checkKey('login2'):
                if User.isLoggedIn(request): # Already logged in
                    dprint('Already logged in.')
                    return HttpResponseConflict(ERR.ALREADY_LOGGED_IN)
                if 'dynamicSalt' in request.session: # Start login validating
                    try:
                        user = User.objects.get(username=reqHandler.json['username'])
                        if user.checkPassword(reqHandler.json['password'], request.session['dynamicSalt']): # Check password here
                            res = HttpResponse('Logged in.')
                            dprint('Logged in. User id: %d. ' % user.id + 'Username: ' + user.username)
                            request.session['userId'] = user.id
                            request.session['loginState'] = True
                            if reqHandler.json['remember']:
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
            elif reqHandler.checkKey('login1'):
                dynamicSalt = User.mksalt()
                request.session['dynamicSalt'] = dynamicSalt
                staticSalt = ''
                try:
                    user = User.objects.get(username=reqHandler.json['username'])
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
    if request.method.lower() != 'post':
        return HttpResponseBadRequest()
    else: # Confirm password
        reqHandler = ReqHandler(request)
        if reqHandler.getData('json'):
            dprint('Post string: ' + reqHandler.str)
            if reqHandler.checkKey('reset3'):
                if not ('reset' in request.session and request.session['reset']):
                    dprint('Invalid reset operation.')
                    request.session.flush()
                    return HttpResponseConflict(ERR.INVALID_OPERATION)
                if 'newStaticSalt' in request.session:
                    if reqHandler.json['userId'] != request.session['userId']:
                        # Suspicious behavior detected
                        dprint('User id not match. User id in session: %d.' % request.session['userId'])
                        request.session.flush()
                        return HttpResponseBadRequest(ERR.USER_ID_NOT_MATCH)
                    user = User.objects.get(id=request.session['userId'])
                    user.password_salt = request.session['newStaticSalt']
                    user.password = reqHandler.json['newPassword']
                    user.save()
                    dprint('New password set. Require re-login.')
                    request.session.flush()
                    return HttpResponse('New password set. Require re-login.')
                else:
                    dprint('Attempt to reset password without a new static salt.')
                    request.session.flush()
                    return HttpResponseBadRequest(ERR.SESSION_EXPIRED)
            elif reqHandler.checkKey('reset2'):
                if 'dynamicSalt' in request.session:  # Start old (current) password validating
                    try:
                        user = User.objects.get(username=reqHandler.json['username'])
                        if (not 'userId' in request.session) or (request.session['userId'] != user.id):
                            dprint('Attempt to reset another user\' password.')
                            return HttpResponseBadRequest(ERR.USERNAME_NOT_MATCH)
                        if user.checkPassword(reqHandler.json['password'],
                                              request.session['dynamicSalt']):  # Check password here
                            newStaticSalt = User.mksalt()
                            request.session['newStaticSalt'] = newStaticSalt
                            res = HttpResponse('{userId:%d,' % user.id + 'newStaticSalt:"' + newStaticSalt + '"}')
                            dprint('Old password confirmed. User id: %d. ' % user.id + 'Username: ' + user.username)
                            request.session['reset'] = True
                            request.session.set_expiry(0)
                        else:
                            dprint('Password incorrect.')
                            res = HttpResponseBadRequest(ERR.PASSWORD_INCORRECT)
                        return res
                    except User.DoesNotExist:
                        dprint('User not found.')
                        request.session.flush()
                        return HttpResponseBadRequest(ERR.USERNAME_NOT_MATCH)
                else:
                    dprint('Attempt to verify old password without generating dynamicSalt.')
                    request.session.flush()
                    return HttpResponseBadRequest(ERR.SESSION_EXPIRED)
            elif reqHandler.checkKey('reset1'):
                dynamicSalt = User.mksalt()
                request.session['dynamicSalt'] = dynamicSalt
                staticSalt = ''
                try:
                    user = User.objects.get(username=reqHandler.json['username'])
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

class Favorite:
    '''Handling users' favorite list.
    '''
    @staticmethod
    @requireLogin
    @loginStateMaintainer
    def getFavorite(request, **kwargs):
        if request.method.lower() != 'get':
            return HttpResponseBadRequest()
        try:
            user = User.objects.get(id=request.session['userId'])
            dprint('User found.')
            return JsonResponse(user.favorites or [], safe=False)
        except User.DoesNotExist:
            dprint('User not found. Login state error.')
            request.session['loginState'] = False
            request.session.flush()
            dprint('Force logout.')
            return HttpResponseUnauthorized('Login state error.')

    @staticmethod
    @requireLogin
    @loginStateMaintainer
    def addFavorite(request, **kwargs):
        if request.method.lower() != 'put':
            return HttpResponseBadRequest()
        try:
            user = User.objects.get(id=request.session['userId'])
            dprint('User found.')
            # reqHandler = ReqHandler(request)
            if 'type' in kwargs and 'id' in kwargs and kwargs['type'] and kwargs['id']:
                if user.addFavorite(int(kwargs['type']), int(kwargs['id'])):
                    return HttpResponse('Question type:%s id:%s was added to favorite list.' % (kwargs['type'], kwargs['id']))
                else:
                    return HttpResponseConflict(ERR.ADD_FAILED)
            else:
                return HttpResponseBadRequest(ERR.MISSING_PARAM)
        except User.DoesNotExist:
            dprint('User not found. Login state error.')
            request.session['loginState'] = False
            request.session.flush()
            dprint('Force logout.')
            return HttpResponseUnauthorized('Login state error.')

    @staticmethod
    @requireLogin
    @loginStateMaintainer
    def delFavorite(request, **kwargs):
        if request.method.lower() != 'delete':
            return HttpResponseBadRequest()
        try:
            user = User.objects.get(id=request.session['userId'])
            dprint('User found.')
            # reqHandler = ReqHandler(request)
            if 'type' in kwargs and 'id' in kwargs and kwargs['type'] and kwargs['id']:
                if user.delFavorite(int(kwargs['type']), int(kwargs['id'])):
                    return HttpResponse('Question type:%s id:%s was deleted from favorite list.' % (kwargs['type'], kwargs['id']))
                else:
                    return HttpResponseNotFound(ERR.DEL_FAILED)
            else:
                return HttpResponseBadRequest(ERR.MISSING_PARAM)
        except User.DoesNotExist:
            dprint('User not found. Login state error.')
            request.session['loginState'] = False
            request.session.flush()
            dprint('Force logout.')
            return HttpResponseUnauthorized('Login state error.')

    @staticmethod
    @csrf_exempt
    def favorite(request, **kwargs):
        methods = {
            'get': __class__.getFavorite,
            'put': __class__.addFavorite,
            'delete': __class__.delFavorite
        }
        method = request.method.lower()
        if method not in methods:
            return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
        dprint('favorite type: ' + (kwargs['type'] or '') + 'id: ' + (kwargs['id'] or ''))
        # if reqHandler.getJson():
        #     if 'csrf' in reqHandler.json:
        #         return render(request, 'user/csrf.html')
        return methods[method](request, **kwargs)

class Flawbook:
    '''Handling users' flawbook.
    '''
    @staticmethod
    @requireLogin
    @loginStateMaintainer
    def getFlawbook(request, **kwargs):
        if request.method.lower() != 'get':
            return HttpResponseBadRequest()
        try:
            user = User.objects.get(id=request.session['userId'])
            dprint('User found.')
            return JsonResponse(user.flawbook or [], safe=False)
        except User.DoesNotExist:
            dprint('User not found. Login state error.')
            request.session['loginState'] = False
            request.session.flush()
            dprint('Force logout.')
            return HttpResponseUnauthorized('Login state error.')

    @staticmethod
    @requireLogin
    @loginStateMaintainer
    def addFlaw(request, **kwargs):
        if request.method.lower() != 'put':
            return HttpResponseBadRequest()
        try:
            user = User.objects.get(id=request.session['userId'])
            dprint('User found.')
            # reqHandler = ReqHandler(request)
            if 'type' in kwargs and 'id' in kwargs and kwargs['type'] and kwargs['id']:
                if user.addFlaw(int(kwargs['type']), int(kwargs['id'])):
                    return HttpResponse('Question type:%s id:%s was added to flaw list.' % (kwargs['type'], kwargs['id']))
                else:
                    return HttpResponseConflict(ERR.ADD_FAILED)
            else:
                return HttpResponseBadRequest(ERR.MISSING_PARAM)
        except User.DoesNotExist:
            dprint('User not found. Login state error.')
            request.session['loginState'] = False
            request.session.flush()
            dprint('Force logout.')
            return HttpResponseUnauthorized('Login state error.')

    @staticmethod
    @requireLogin
    @loginStateMaintainer
    def delFlaw(request, **kwargs):
        if request.method.lower() != 'delete':
            return HttpResponseBadRequest()
        try:
            user = User.objects.get(id=request.session['userId'])
            dprint('User found.')
            # reqHandler = ReqHandler(request)
            if 'type' in kwargs and 'id' in kwargs and kwargs['type'] and kwargs['id']:
                if user.delFlaw(int(kwargs['type']), int(kwargs['id'])):
                    return HttpResponse('Question type:%s id:%s was deleted from flawbook.' % (kwargs['type'], kwargs['id']))
                else:
                    return HttpResponseNotFound(ERR.DEL_FAILED)
            else:
                return HttpResponseBadRequest(ERR.MISSING_PARAM)
        except User.DoesNotExist:
            dprint('User not found. Login state error.')
            request.session['loginState'] = False
            request.session.flush()
            dprint('Force logout.')
            return HttpResponseUnauthorized('Login state error.')

    @staticmethod
    @csrf_exempt
    def flawbook(request, **kwargs):
        methods = {
            'get': __class__.getFlawbook,
            'put': __class__.addFlaw,
            'delete': __class__.delFlaw
        }
        method = request.method.lower()
        if method not in methods:
            return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
        dprint('flawbook type: ' + (kwargs['type'] or '') + 'id: ' + (kwargs['id'] or ''))
        # if reqHandler.getJson():
        #     if 'csrf' in reqHandler.json:
        #         return render(request, 'user/csrf.html')
        return methods[method](request, **kwargs)
