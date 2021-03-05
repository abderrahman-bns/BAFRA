from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from faceApp import db, login_manager, app


@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(50), default='default.jpg', nullable=False)
    video_file = db.Column(db.String(50), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False, unique=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User :'{self.matricule}', '{self.username}', '{self.email}', '{self.profil}'"


class Agent(db.Model):
    __tablename__ = 'agent'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nom = db.Column(db.String(25), nullable=False)
    prenom = db.Column(db.String(25), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    tel = db.Column(db.Unicode(10), nullable=False)
    fonction = db.Column(db.String(50), nullable=False)
    departement_id = db.Column(db.Integer, db.ForeignKey("departement.id"), nullable=False)
    user = db.relationship('User', backref='agent', uselist=False)  # one-to-one

    def __repr__(self):
        return f"Agent : '{self.nom}', '{self.prenom}', '{self.age}', '{self.sex}', '{self.fonction}'"


class Departement(db.Model):
    __tablename__ = 'departement'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nom = db.Column(db.String(50), nullable=False, unique=True)
    agent = db.relationship('Agent', backref='departement', lazy=True)

    def __repr__(self):
        return f"Departement : '{self.nom}'"
