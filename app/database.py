from .models import db


def get_all(model):
    data = model.query.all()
    return data


def add_instance(model, **kwargs):
    instance = model(**kwargs)
    db.session.add(instance)
    commit_changes()
    return instance


def delete_instance(model, _id):
    model.query.filter_by(id=_id).delete()
    commit_changes()


def edit_instance(model, _id, **kwargs):
    instance = model.query.filter_by(id=_id).all()[0]
    for attr, new_value in kwargs.items():
        setattr(instance, attr, new_value)
    commit_changes()
    return instance


def commit_changes():
    db.session.commit()
