from flask import current_app as app
from flask import url_for, redirect, request, abort
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user, Security, SQLAlchemyUserDatastore

from . import db
from .models import Role, RoleNames, User


class BaseModelView(ModelView):
    create_modal = True
    edit_modal = True
    column_filters = ['created', 'modified']

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role(RoleNames.SUPERUSER)
                )

    def _handle_view(self, name, **kwargs):
        """
            Override builtin _handle_view in order
            to redirect users when a view is not accessible.
        """

        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


class RoleView(BaseModelView):
    column_searchable_list = ['name']
    column_list = [
        'id', 'name', 'created', 'modified'
    ]


class UserView(BaseModelView):
    column_searchable_list = ['first_name', 'last_name', 'email']
    column_list = [
        'id', 'email', 'active', 'first_name',
        'last_name', 'ya_disc_token', 'created', 'modified'
    ]
    form_widget_args = {
        'password': {
            'disabled': True
        }
    }


admin = Admin(
    app,
    name='voip',
    template_mode='bootstrap3',
    base_template='base_admin.html'
)

admin.add_view(RoleView(Role, db.session))
admin.add_view(UserView(User, db.session))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )
