from configuration import db, ma
from entities import User, Preference


class User_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        session = db.session


class Prefence_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Preference
        load_instance = True
        session = db.session


user_schema = User_schema()
users_schema = User_schema(many=True)
preference_schema = Prefence_schema()
preferences_schema = Prefence_schema(many=True)
