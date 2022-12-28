from celery import Celery

celery_app = None


def init_celery(app):
    global celery_app
    celery_app = Celery(app.import_name)
    celery_app.conf.update(include=['tasks'])

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
