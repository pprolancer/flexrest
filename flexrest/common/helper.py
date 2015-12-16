# -*- coding: utf-8 -*-
import decimal
from functools import wraps
import datetime
from flask import jsonify, json, abort as flask_abort
from flask import make_response
from flask.globals import current_app, request
from flask.ext.login import current_user
from werkzeug.exceptions import HTTPException


def jsonify_status_string(status_code=200, message=None, *args, **kw):
    response = jsonify(*args, **kw)
    response.status_code = response.code = status_code
    if message is not None:
        response.status = '%d %s' % (status_code, str(message))

    return response


def abort(response, status_code=None):
    if isinstance(response, basestring):
        response = make_response(response)
    if status_code:
        response.status_code = status_code
    e = HTTPException(response=response)
    e.code = getattr(response, 'status_code', 0)
    raise e


def abort_jsonify(code, message, *args, **kwargs):
    response = jsonify_status_string(code, message, *args, **kwargs)
    abort(response)


def json_loads_safe(s, none_if_failed=False, **kwargs):
    try:
        return json.loads(s, **kwargs)
    except:
        return None if none_if_failed else s


def model_to_dict(obj, fields=None, fields_map={}, extra_fields=None):
    '''
    convert a sqlalchemy object to a python dict.
    @param fields: list of fields which we want to show in return value.
        if fields=None, we show all fields of sqlalchemy object
    @type fields: list
    @param fields_map: a map converter to show fields as a favorite.
        every field can bind to a lambda function in fields_map.
        if a field was bind to a None value in fields_map, we ignore this field
        to show in result
    @type fields_map: dict
    '''
    data = {}

    if fields is None:
        fields = obj.__table__.columns.keys()
    fields.extend(extra_fields or [])
    for field in fields:
        if field in fields_map:
            if fields_map[field] is None:
                continue
            v = fields_map.get(field)()
        else:
            v = getattr(obj, field, None)
        if isinstance(v, datetime.datetime):
            data[field] = v.isoformat() + 'Z'
        elif isinstance(v, datetime.date):
            data[field] = v.isoformat()
        elif isinstance(v, decimal.Decimal):
            data[field] = float(v)
        else:
            data[field] = v

    return data
