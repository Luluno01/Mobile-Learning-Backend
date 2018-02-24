import json
from json.decoder import JSONDecodeError

def RequestParamParser(request, urlParams, *args, **kwargs):
    parsers = [
        (int, ValueError),
        (float, ValueError),
        (json.loads, JSONDecodeError)
    ]
    request.params.update(urlParams)
    for paramName in request.params:
        if type(request.params[paramName]) == str:
            parsed = None
            for parser in parsers:
                try:
                    parsed = parser[0](request.params[paramName])
                    break
                except parser[1]:
                    pass
            if parsed != None:
                request.params[paramName] = parsed