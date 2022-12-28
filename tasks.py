from extensions.celery import celery_app
from extensions.sqlalchemy import db
from fibonacci.models import Fibonacci
from lib import create_fibonacci


@celery_app.task(ignore_result=True)
def async_create_fibonacci(n):
    fibonacci_n = create_fibonacci(n)
    fibonacci = db.session.execute(db.select(Fibonacci).filter_by(ordinal=n))\
        .scalar()
    if fibonacci is None:
        fibonacci = Fibonacci(ordinal=n)
        db.session.add(fibonacci)
    fibonacci.nth = fibonacci_n
    db.session.commit()
    return fibonacci_n
