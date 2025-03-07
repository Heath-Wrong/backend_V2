import os
class Config:
    API_KEY, API_SECRET = 'YOUR_API_KEY', 'YOUR_API_SECRET'

    basedir = 'd:/SV/SV_sys/backend_V2'
    
    # 数据库连接池配置
    DB_POOL_SIZE = 5
    DB_MAX_OVERFLOW = 2
    DB_POOL_TIMEOUT = 30  # 秒
    DB_URI = 'sqlite:///' + os.path.join(basedir, 'database/voiceprint.db')
    
    # 模型配置
    MODEL_PATH = os.path.join(basedir, 'pretrained_models/ecapa_tdnn.pth')

    #
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

    # 识别阈值
    THRESHOLD = 0.5  # 根据实际测试调整
