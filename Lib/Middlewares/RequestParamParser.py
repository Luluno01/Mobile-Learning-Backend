import json
from json.decoder import JSONDecodeError
from django.utils.deprecation import MiddlewareMixin
from django.http import QueryDict

class RequestParamParser(MiddlewareMixin):
    def process_request(self, request):
        params = {}
        try:
            params = json.loads(request.body)  # JSON
        except JSONDecodeError:
            params = dict(QueryDict(request.body))  # Form
            for paramName in params:
                if len(params[paramName]) == 1:
                    params[paramName] = params[paramName][0]
            if 'json' in params:  # JSON in form
                if type(params['json']) == list:
                    _json = {}
                    for _mJson in params['json']:
                        try:
                            _json.update(json.loads(_mJson))  # Unpack `json`
                        except JSONDecodeError:
                            pass
                    del params['json']
                    params.update(_json)
                else:  # type(params['json']) == str
                    _json = params['json']
                    try:
                        _json = json.loads(_json)  # Unpack `json`
                        del params['json']
                        params.update(_json)
                    except JSONDecodeError:
                        pass
        request.params = params

    def process_response(self, request, response):
        return response