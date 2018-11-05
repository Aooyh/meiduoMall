# to define my own exception handler function

import logging

from django.db import DatabaseError
from rest_framework import status
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exc, context):
    """
    :param exc: exception
    :param context: context
    :return: response(error_message and status_code)
    """
    logger = logging.getLogger('meiduo')
    response = drf_exception_handler(exc, context)
    if not response:
        view = context.get('view')
        if isinstance(exc, DatabaseError) or isinstance(exc, RedisError):
            logger.error('[%s] %s' % (view, exc))
            response = Response(data={'error_message: database error or redis error'},
                                status=status.HTTP_507_INSUFFICIENT_STORAGE)
    return response
