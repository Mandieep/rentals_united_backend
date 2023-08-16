from rest_framework.response import Response
from rest_framework import status
from rental_properties_app.response import Responsehandler

response_handler = Responsehandler()


def access_authorized_users_only(view_func):
    def wrapped_view(request, *args, **kwargs):
        authorization = request.headers.get('Authorization')

        if authorization is None:
            response_dict = response_handler.msg_response(
                "Please provide authorization bearer token in api!", 422)
            return Response(response_dict, status.HTTP_422_UNPROCESSABLE_ENTITY)

        token = authorization.split(' ')
        if not '128a5e3f-60d4-4fc7-92fb-2cd5c4c27e04' == token[1]:
            response_dict = response_handler.msg_response(
                "You are not authorized to access this page !", 422)
            return Response(response_dict, status.HTTP_422_UNPROCESSABLE_ENTITY)
        return view_func(request, *args, **kwargs)

    return wrapped_view
