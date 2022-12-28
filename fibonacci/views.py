import json

from flask import Blueprint, Response, request
from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError

import tasks
from extensions.celery import celery_app
from extensions.sqlalchemy import db

from .models import Fibonacci

bp = Blueprint('fibonacci', __name__)


class FibonacciSchema(Schema):
    n = fields.Integer(required=True)


@bp.route('/fibonacci', methods=['POST'])
def create_fibonacci():
    try:
        request_data = FibonacciSchema().load(request.json)
        ordinal = request_data.get('n')
        fibonacci = db.session.execute(
            db.select(Fibonacci).filter_by(ordinal=ordinal)).scalar()

        if fibonacci is None:
            # look for pending tasks with same arguments
            i = celery_app.control.inspect()
            active_tasks = i.active()
            in_progress = False
            if active_tasks is not None:
                for _, tasks_ in active_tasks.items():
                    for task in tasks_:
                        if task['name'] != tasks.async_create_fibonacci.name:
                            continue
                        if ordinal in task['args']:
                            in_progress = True
                            break
                    if in_progress:
                        break

            if not in_progress:
                tasks.async_create_fibonacci.delay(request_data.get('n'))

            content = {"status": "pending"}
            return Response(json.dumps(content), 202,
                            content_type='application/json')
        else:
            content = {"status": "success", "nth": str(fibonacci.nth)}
            return Response(json.dumps(content), status=200,
                            content_type='application/json')
    except ValidationError as e:
        return Response(json.dumps(e.messages), status=400,
                        content_type='application/json')
