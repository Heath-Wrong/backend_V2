import base64
import hmac
import hashlib
from datetime import datetime
from config import Config
from urllib.parse import urlparse, parse_qs
def verify_auth(request):
    # 获取请求头中的必要信息
    query_params = parse_qs(urlparse(request.url).query)
    host = query_params.get('host', [None])[0]
    date = query_params.get('date', [None])[0]
    authorization =query_params.get('authorization', [None])[0]

    if not date:
        return 'HMAC signature cannot be verified, a valid date or x-date header is required for HMAC Authentication'
    try:
        request_time = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S GMT')
        time_diff = (datetime.utcnow() - request_time).total_seconds()
        if abs(time_diff) > 300:
            return 'HMAC signature cannot be verified, a valid date or x-date header is required for HMAC Authentication'
    except Exception as e:
        return 'HMAC signature cannot be verified, a valid date or x-date header is required for HMAC Authentication'

    if not authorization:
        return 'Unauthorized'
    try:
        auth_str = base64.b64decode(authorization).decode('utf-8')
        auth_parts = {}
        for item in auth_str.split(', '):
            key_value = item.split('=', 1)  # 确保只分割一次
            if len(key_value) != 2:
                continue
            key, value = key_value
            auth_parts[key] = value.strip('"')
        api_key = auth_parts['api_key']
        algorithm = auth_parts['algorithm']
        headers = auth_parts['headers']
        signature = auth_parts['signature']

        # auth_parts = dict(item.split('=') for item in auth_str.split(', '))
        # api_key = auth_parts['api_key'].strip('"')
        # algorithm = auth_parts['algorithm'].strip('"')
        # headers = auth_parts['headers'].strip('"')
        # signature = auth_parts['signature'].strip('"')
    except Exception as e:
        return 'HMAC signature cannot be verified'
    # 验证算法
    if algorithm != 'hmac-sha256':
        return 'HMAC signature cannot be verified'
    # 生成签名
    signature_origin = f"host: {host}\ndate: {date}\nPOST /v1/private/s782b4996 HTTP/1.1"
    signature_sha = hmac.new(Config.API_SECRET.encode('utf-8'), signature_origin.encode('utf-8'),
                           digestmod=hashlib.sha256).digest()
    calculated_signature = base64.b64encode(signature_sha).decode('utf-8')
    # 验证签名
    if calculated_signature != signature:
        return 'HMAC signature does not match'
    if api_key != Config.API_KEY:
        return 'HMAC signature cannot be verified'
    return 'success'