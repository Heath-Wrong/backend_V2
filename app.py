from flask import Flask, g
from routes.api_routes import api_bp
from config import Config
import uuid
import os
from database.init_db import db
from database.init_db import init_db


app = Flask(__name__)
app.config.from_object(Config)
init_db(app)
db.init_app(app)

with app.app_context():
    db.create_all()
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 注册蓝图
app.register_blueprint(api_bp)

@app.before_request
def generate_sid():
    # 每次请求生成唯一会话ID
    g.sid = str(uuid.uuid4())

if __name__ == '__main__':
    app.run(debug=True)