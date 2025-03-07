import pickle
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': Config.DB_POOL_SIZE,
        'max_overflow': Config.DB_MAX_OVERFLOW,
        'pool_timeout': Config.DB_POOL_TIMEOUT
    }

class Group(db.Model):
    __tablename__ = 'groups'
    group_id = db.Column(db.String(32), primary_key=True, unique=True, nullable=False)  # 添加 primary_key=True
    group_name = db.Column(db.String(256))
    group_info = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Feature(db.Model):
    __tablename__ = 'features'
    group_id = db.Column(db.String(255), db.ForeignKey('groups.group_id'), nullable=False)
    feature_id = db.Column(db.String(32), primary_key=True, unique=True, nullable=False)  # 添加 primary_key=True
    feature_info = db.Column(db.String(256))
    feature = db.Column(db.LargeBinary)  # 声纹向量（pickle序列化）
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    @classmethod
    def get_all_vectors(cls):
        """获取所有存储的声纹向量（自动反序列化）"""
        return [(pickle.loads(v.vector), v.id) for v in cls.query.all()]

    @staticmethod
    def serialize_vector(vector):
        """序列化numpy数组"""
        return pickle.dumps(vector)

    @staticmethod
    def deserialize_vector(binary_data):
        """反序列化二进制数据为numpy数组"""
        return pickle.loads(binary_data)