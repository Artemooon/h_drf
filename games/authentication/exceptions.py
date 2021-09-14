from rest_framework import views
from django.http import JsonResponse


class BaseView(views.APIView):

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return self._response({'error_message': e.args}, status=400)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, status=200):
        return JsonResponse(data, status=status)
