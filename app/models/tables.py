from asyncio.windows_events import NULL
from sqlalchemy import ForeignKey
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False, unique=True)
    CPF = db.Column(db.String(11), nullable=False, unique=True)
    login = db.Column(db.String(45), nullable=False, unique=True)
    hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.relationship("Course_per_client")

    def __init__(self, name, email, CPF, login, password, is_admin):
        self.name = name
        self.email = email
        self.CPF = CPF
        self.login = login
        self.hash = generate_password_hash(password)
        self.is_admin = is_admin
    
    def verify_password(self, pwd):  # Checando se a senha confere
        return check_password_hash(self.hash, pwd)

    @classmethod
    def user_exists(self, email, cpf, login):  # Checando se já existe algum usuário com o mesmo email, cpf ou login
        if self.query.filter((self.email == email) | (self.CPF == cpf) | (self.login == login)).first():
            return True
        return False
    


class User_Data(db.Model):
    __tablename__ = 'users_data'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False, unique=True)
    tel = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(15), nullable=False)
    marital_status = db.Column(db.String(15), nullable=False)
    birth = db.Column(db.String(15), nullable=False)
    already_works = db.Column(db.Boolean, nullable=False, default=False)
    adress = db.Column(db.String(45), nullable=False)
    district = db.Column(db.String(45), nullable=False)
    city = db.Column(db.String(45), nullable=False)
    state= db.Column(db.String(2), nullable=False)
    country = db.Column(db.String(45), nullable=False)
    cep = db.Column(db.String(10), nullable=False)

    def __init__(self, user_id, tel, gender, marital_status, birth, already_works, adress, district, city, state, country, cep):
        self.user_id = user_id
        self.tel = tel
        self.gender = gender
        self.marital_status = marital_status
        self.birth = birth
        self.already_works = already_works
        self.adress = adress
        self.district = district
        self.city = city
        self.state = state
        self.country = country
        self.cep = cep


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    price = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=False)
    level = db.Column(db.String(15), nullable=False)
    creation_date = db.Column(db.String(40), nullable=False)
    last_update = db.Column(db.String(40))
    workload = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    banner_1 = db.Column(db.String(20))
    banner_2 = db.Column(db.String(20))
    video_1 = db.Column(db.String(20))
    video_2 = db.Column(db.String(20))
    course_id_rel = db.relationship("Module")
    class_course = db.relationship("Class")
    course_id = db.relationship("Course_per_client")

    def __init__(self, name, price, description, level, creation_date, is_active, banner_1, banner_2, video_1, last_update=NULL, video_2=NULL, workload=NULL):
        self.name = name
        self.price = price
        self.description = description
        self.level = level
        self.creation_date = creation_date
        self.last_update = last_update
        self.workload = workload
        self.is_active = is_active
        self.banner_1 = banner_1
        self.banner_2 = banner_2
        self.video_1 = video_1
        self.video_2 = video_2


class Module(db.Model):
    __tablename__ = 'modules'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, unique=True)
    course_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    teacher = db.Column(db.String(20), nullable=False)
    workload = db.Column(db.Integer, nullable=False, default=0)
    creation_date = db.Column(db.String(40), nullable=False)
    last_update = db.Column(db.String(40))
    banner_1 = db.Column(db.String(50))
    banner_2 = db.Column(db.String(50))
    video_1 = db.Column(db.String(500))
    video_2 = db.Column(db.String(500))
    index = db.Column(db.Integer, nullable=False)
    class_module = db.relationship("Class")

    def __init__(self, course_id, name, description, teacher, creation_date, banner_1, video_1, index, last_update=NULL, workload=NULL, banner_2=NULL, video_2=NULL):
        self.course_id = course_id
        self.name = name
        self.description = description
        self.teacher = teacher
        self.workload = workload
        self.creation_date = creation_date
        self.last_update = last_update
        self.banner_1 = banner_1
        self.banner_2 = banner_2
        self.video_1 = video_1
        self.video_2 = video_2
        self.index = index


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, unique=True)
    module_id = db.Column(db.Integer, db.ForeignKey(Module.id), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(20))
    teacher = db.Column(db.String(50))
    creation_date = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=False)
    banner_1 = db.Column(db.String(50))
    banner_2 = db.Column(db.String(50))
    video_1 = db.Column(db.String(600))
    video_2 = db.Column(db.String(600))
    index = db.Column(db.Integer, nullable=False)

    def __init__(self, module_id, course_id, name, duration, teacher, creation_date, description, banner_1, video_1, index, banner_2=NULL, video_2=NULL):
        self.module_id = module_id
        self.course_id = course_id
        self.name = name
        self.duration = duration
        self.teacher = teacher
        self.creation_date = creation_date
        self.description = description
        self.banner_1 = banner_1
        self.banner_2 = banner_2
        self.video_1 = video_1
        self.video_2 = video_2
        self.index = index


class Cupons(db.Model):
    __tablename__ = 'cupons'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    discount = db.Column(db.Integer, nullable=False)

    def __init__(self, name, discount):
        self.name = name
        self.discount = discount


class Course_per_client(db.Model):
    __tablename__ = 'courses_per_client'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
    date_of_add = db.Column(db.String(20), nullable=False)
    last_access = db.Column(db.String(20))
    expiration_date = db.Column(db.String(20), nullable=False, default='perpetual')
    current_module_id = db.Column(db.Integer, nullable=False, default=0)
    current_class_id = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, user_id, course_id, date_of_add, last_access, expiration_date, current_module_id, current_class_id):
        self.user_id = user_id
        self.course_id = course_id
        self.date_of_add = date_of_add
        self.last_access = last_access
        self.expiration_date = expiration_date
        self.current_module_id = current_module_id
        self.current_class_id = current_class_id


class Access(db.Model):
    __tablename__ = 'access'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    module_id = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey(Class.id), nullable=False)
    datetime = db.Column(db.String(20), nullable=False)

    def __init__(self, user_id, course_id, module_id, class_id, datetime):
        self.user_id = user_id
        self.course_id = course_id
        self.module_id = module_id
        self.class_id = class_id
        self.datetime = datetime