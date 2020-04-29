from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


class JsonUnicodeResponse(JsonResponse):

    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True,
                    json_dumps_params=None, **kwargs):
        if json_dumps_params:
            json_dumps_params = {}
        json_dumps_params = {'ensure_ascii': False}
        super().__init__(data, encoder, safe, json_dumps_params, **kwargs)