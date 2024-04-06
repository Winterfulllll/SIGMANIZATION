from configuration import db, ma


class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(25), primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    surname = db.Column(db.String(50))
    name = db.Column(db.String(50))
    patronymic = db.Column(db.String(50))


class User_schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        session = db.session


user_schema = User_schema()
users_schema = User_schema(many=True)
db.create_all()
