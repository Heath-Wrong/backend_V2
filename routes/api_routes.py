from flask import Blueprint, request, jsonify
from database.db_operations import createFeature, createGroup, deleteFeature, queryFeatureList, searchFea, searchScoreFea, updateFeature, deleteGroup, queryGroupList
from config import Config
from auth.verify import verify_auth

api_bp = Blueprint('api', __name__)

@api_bp.route('/v1/private/s782b4996', methods=['POST'])
def handle_request():

    print('request.headers:', request.headers)
    # 验证请求
    auth_result = verify_auth(request)
    if auth_result != 'success':
        # 根据不同的错误类型返回不同状态码
        error_mapping = {
            'success': 200,
            'Unauthorized': 401,
            'HMAC signature cannot be verified': 401,
            'HMAC signature does not match': 401,
            'HMAC signature cannot be verified, a valid date or x-date header is required for HMAC Authentication': 403
        }
        status_code = error_mapping[auth_result]
        return jsonify({'message': auth_result}), status_code
    # 处理请求体
    data = request.get_json()
    api_name = data['parameter']['s782b4996']['func']
    if api_name == 'createFeature':
        return createFeature(data)
    elif api_name == 'createGroup':
        return createGroup(data)
    elif api_name == 'deleteFeature':
        return deleteFeature(data)
    elif api_name == 'queryFeatureList':
        return queryFeatureList(data)
    elif api_name == 'searchFea':
        return searchFea(data)
    elif api_name == 'searchScoreFea':
        return searchScoreFea(data)
    elif api_name == 'updateFeature':
        return updateFeature(data)
    elif api_name == 'deleteGroup':
        return deleteGroup(data)
    elif api_name == 'verifyKey':
        return jsonify({'message': 'success'}), 200
    elif api_name == 'queryGroupList':
        return queryGroupList(data)
    else:
        return jsonify({'error': 'Unsupported API'}), 400