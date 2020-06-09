from .main import db
from app.constants import ROLES
from app.main.model.ticket import UserRoles

__all__ = ("Seed",)


class Seed(object):
    def seed(self, app):
        with app.app_context():
            db.session.add_all([*self._setup_roles(),])
            db.session.commit()

    def _setup_roles(self):
        roles = []
        db_actions = db.session.query(UserRoles) \
            .filter(UserRoles.role.in_(ROLES)).all()

        if len(db_actions) == 0:
            for action in ROLES:
                roles.append(UserRoles(role=action))
        return roles


