from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, CHAR
from datetime import datetime


class ISODateTime(TypeDecorator):
    impl = CHAR(19)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.strftime('%Y-%m-%dT%H:%M:%S')

    def process_result_value(self, value, dialect):
        if value is not None:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    password = db.Column(db.String(80))
    avatar_url = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean)
    last_mod = db.Column(ISODateTime, default=datetime.now)

    # project = db.relationship('project', cascade='all, delete-orphan')

    def __repr__(self):
        return '<User {},{},{},{}>'.format(self.id, self.name, self.password, self.avatar_url)


class OriginalImage(db.Model):
    __tablename__ = 'original_image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    img_url = db.Column(db.String(80), unique=True, nullable=False)
    # style = db.Column(db.JSON)
    # type = db.Column(db.JSON)
    user_id = db.Column(db.ForeignKey('user.id'), name='user_id')
    last_mod = db.Column(ISODateTime, default=datetime.now)

    def __repr__(self):
        return '<Image {},{},style={},type={}>'.format(self.id, self.img_url, self.style, self.type)


class Image_Type(db.Model):
    __tablename__ = 'image_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_id = db.Column(db.ForeignKey('original_image.id'), name='original_image_id')
    type = db.Column(db.String(20))
    category = db.Column(db.String(20))

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Image_Style(db.Model):
    __tablename__ = 'image_style'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_id = db.Column(db.ForeignKey('original_image.id'), name='original_image_id')
    style = db.Column(db.String(20))


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    style = db.Column(db.JSON)
    type = db.Column(db.JSON)
    user_id = db.Column(db.ForeignKey('user.id'), name='user_id')
    last_mod = db.Column(ISODateTime, default=datetime.now)
    thumbnail_url = db.Column(db.String(80))

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class ProcessedImage(db.Model):
    __tablename__ = 'processed_image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pos_x = db.Column(db.Integer)
    pos_y = db.Column(db.Integer)
    layer = db.Column(db.Integer)
    rotate_deg = db.Column(db.Integer)  # 旋转的度数
    width = db.Column(db.Integer)  # 缩放后的x方向长度，宽度
    height = db.Column(db.Integer)  # 缩放后的y方向长度，高度
    w_pos = db.Column(db.DECIMAL(2, 1))
    w_neg = db.Column(db.DECIMAL(2, 1))
    t_i = db.Column(db.DECIMAL(2, 1))
    project_id = db.Column(db.ForeignKey('project.id'), name='project_id')
    img_id = db.Column(db.ForeignKey('original_image.id'), name='img_id')
    last_mod = db.Column(ISODateTime, default=datetime.now)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class OutputImage(db.Model):
    __tablename__ = 'output_image'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    img_url = db.Column(db.String(80), unique=True, nullable=False)
    project_id = db.Column(db.Integer)
    user_id = db.Column(db.ForeignKey('user.id', name='user_id'))
    last_mod = db.Column(ISODateTime, default=datetime.now)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
