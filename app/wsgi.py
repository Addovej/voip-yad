from flask_sqlalchemy import models_committed

from . import create_app

app = create_app()


@models_committed.connect_via(app)
def on_models_committed(sender, changes):
    """
    Database signals handler.
    """

    for obj, change in changes:
        if change == 'insert' and hasattr(obj, '__commit_insert__'):
            obj.__commit_insert__()
        elif change == 'update' and hasattr(obj, '__commit_update__'):
            obj.__commit_update__()
        elif change == 'delete' and hasattr(obj, '__commit_delete__'):
            obj.__commit_delete__()


if __name__ == '__main__':
    app.run()
