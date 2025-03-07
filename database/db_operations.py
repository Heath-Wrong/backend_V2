from flask import jsonify, g  # 补充g对象导入
import json
import base64
from config import Config
from sqlalchemy.exc import SQLAlchemyError
from .init_db import Group, Feature, db
from utils import VoiceProcessor
import tempfile
import pickle

def build_response(code, message, payload):
    # 新增响应构建器
    return jsonify({
        "header": {
            "code": code,
            "message": message,
            "sid": g.sid  # 从全局请求上下文获取
        },
        "payload": payload
    })

def createGroup(data):
    # 处理createGroup请求
    try:
        parameter = data['parameter']['s782b4996']
        new_group = Group(
            group_id   = parameter['groupId'],
            group_name = parameter['groupName'],
            group_info = parameter.get('groupInfo')
        )
        db.session.add(new_group)
        db.session.commit()
        message = "success"
        code = 0
        text_origin = {
            "groupId": parameter['groupId'],
            "groupName": parameter['groupName'],
            "groupInfo": parameter.get('groupInfo')
        }
        text = base64.b64encode(json.dumps(text_origin).encode('utf-8')).decode('utf-8')
        payload = {
            "createGroupRes": {
                "text": text
            }
        }
        return build_response(code, message, payload)
    except SQLAlchemyError as e:
        db.rollback()
        message = "fail"
        code    = 1
        return jsonify({'error': str(e)}), 500

def createFeature(data):
    try:
        parameter = data['parameter']['s782b4996']
        load_data    = data['payload']['resource']
        #以下的参数留作后用
        encoding     = load_data['encoding']#暂时固定为lame
        sample_rate  = load_data['sample_rate']#暂时固定为16000
        channels     = load_data['channels']#暂时固定为1
        bit_depth    = load_data['bit_depth']
        audio_data   = load_data['audio']

        audio_bytes  = base64.b64decode(load_data['audio'])
        # 将 audio_bytes 保存为临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            temp_audio_path = temp_audio_file.name
        
        feature = VoiceProcessor(Config.MODEL_PATH).extract_feature(temp_audio_path)
        new_feature = Feature(
            group_id     = parameter['groupId'],
            feature_id   = parameter['featureId'],
            feature_info = parameter.get('featureInfo'),
            feature      = pickle.dumps(feature)
        )
        db.session.add(new_feature)
        db.session.commit()

        message = "success"
        code = 0
        text_origin = {
            "groupId": parameter['groupId'],
            "featureId": parameter['featureId'],
            "featureInfo": parameter.get('featureInfo')
        }
        text = base64.b64encode(json.dumps(text_origin).encode('utf-8')).decode('utf-8')
        payload = {
            "createFeatureRes": {
                "text": text
            }
        }
        return build_response(code, message, payload)
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    


def updateFeature(data):
    try:
        parameter = data['parameter']['s782b4996']
        load_data    = data['payload']['resource']
        #以下的参数留作后用
        encoding     = load_data['encoding']#暂时固定为lame
        sample_rate  = load_data['sample_rate']#暂时固定为16000
        channels     = load_data['channels']#暂时固定为1
        bit_depth    = load_data['bit_depth']
        audio_data   = load_data['audio']

        # 查询要更新的特征记录
        existing_feature = Feature.query.filter_by(
            group_id=parameter['groupId'],
            feature_id=parameter['featureId']
        ).first()

        if existing_feature:
            # 更新特征记录的属性

            audio_bytes  = base64.b64decode(load_data['audio'])
            # 将 audio_bytes 保存为临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
                temp_audio_file.write(audio_bytes)
                temp_audio_path = temp_audio_file.name
        
            feature = VoiceProcessor(Config.MODEL_PATH).extract_feature(temp_audio_path)

            existing_feature.feature_info = parameter.get('featureInfo')
            existing_feature.feature = pickle.dumps(feature)
            
            db.session.commit()

            message = "success"
            code = 0
            text_origin = {"msg":"success"}
            text = base64.b64encode(json.dumps(text_origin).encode('utf-8')).decode('utf-8')
            payload = {
                "createFeatureRes": {
                    "text": text
                }
            }
            return build_response(code, message, payload)
        else:
            return jsonify({'error': 'Feature not found'}), 500
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    
def queryFeatureList(data):
    try:
        group_id = data['parameter']['s782b4996']['groupId']
        features = Feature.query.filter_by(group_id=group_id).all()
        features = [{'featureInfo': f.feature_info, 'featureId': f.feature_id} for f in features]

        message = "success"
        code = 0
        text = base64.b64encode(json.dumps(features).encode('utf-8')).decode('utf-8')
        payload = {
            "queryFeatureListRes": {
                "text": text
            }
        }
        return build_response(code, message, payload)
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500



def searchScoreFea(data): # 特征比对1:1
    try:
        parameter = data['parameter']['s782b4996']
        load_data    = data['payload']['resource']
        #以下的参数留作后用
        encoding     = load_data['encoding']#暂时固定为lame
        sample_rate  = load_data['sample_rate']#暂时固定为16000
        channels     = load_data['channels']#暂时固定为1
        bit_depth    = load_data['bit_depth']
        audio_data   = load_data['audio']
        audio_bytes  = base64.b64decode(load_data['audio'])
        # 将 audio_bytes 保存为临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            temp_audio_path = temp_audio_file.name

        feature = VoiceProcessor(Config.MODEL_PATH).extract_feature(temp_audio_path)
        # 查询目标特征
        target_feature = Feature.query.filter_by(
            group_id=parameter['groupId'],
            feature_id=parameter['dstFeatureId']
        ).first()
        if target_feature:
            embedding1 = pickle.loads(target_feature.feature)
            embedding2 = feature
            similarity = VoiceProcessor.cacul_similarity(embedding1, embedding2)
            
            message = "success"
            code = 0
            text_origin = {
                "score": similarity,
                "featureInfo": target_feature.feature_info,
                "featureId": target_feature.feature_id
            }
            text = base64.b64encode(json.dumps(text_origin).encode('utf-8')).decode('utf-8')
            payload = {
                "searchScoreFeaRes": {
                    "text": text
                }
            }
            return build_response(code, message, payload)
        else:
            return jsonify({'error': 'Feature not found'}), 500
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
    
def searchFea(data):
    try:
        parameter = data['parameter']['s782b4996']
        load_data = data['payload']['resource']
        #以下的参数留作后用
        encoding     = load_data['encoding']#暂时固定为lame
        sample_rate  = load_data['sample_rate']#暂时固定为16000
        channels     = load_data['channels']#暂时固定为1
        bit_depth    = load_data['bit_depth']
        audio_data   = load_data['audio']
        audio_bytes  = base64.b64decode(load_data['audio'])
        # 将 audio_bytes 保存为临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio_file:
            temp_audio_file.write(audio_bytes)
            temp_audio_path = temp_audio_file.name
        feature = VoiceProcessor(Config.MODEL_PATH).extract_feature(temp_audio_path)
        

        group_id = parameter['groupId']
        features = Feature.query.filter_by(group_id=group_id).all()
        if not features:
            return jsonify({'error': 'No features found for the given group_id'}), 505

        #此处最好使用向量数据库进行查询
        most_similar_feature = searchVector(feature,group_id)
        if most_similar_feature:
            similarity = VoiceProcessor.cacul_similarity(feature, pickle.loads(most_similar_feature.feature))
            message = "success"
            code = 0
            text_origin = {
                "score": similarity,
                "featureInfo": most_similar_feature.feature_info,
                "featureId": most_similar_feature.feature_id
            }
            text = base64.b64encode(json.dumps(text_origin).encode('utf-8')).decode('utf-8')
            payload = {
                "searchFeaRes": {
                    "text": text
                }
            }
            return build_response(code, message, payload)
        else:
            return jsonify({'error': 'Feature not found'}), 500

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

def deleteFeature(data):
    try:
        parameter = data['parameter']['s782b4996']
        group_id=parameter['groupId']
        feature_id = parameter['featureId']
        Feature.query.filter_by(feature_id=feature_id, group_id=group_id).delete()
        db.session.commit()
        code = 0
        message = "success"
        text_origin = {"msg":"success"}
        text = base64.b64encode(json.dumps(text_origin).encode('utf-8')).decode('utf-8')
        payload = {
            "deleteFeatureRes": {
                "text": text
            }
        }
        return build_response(code, message, payload)
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

def deleteGroup(data):
    try:
        
        group_id = data['parameter']['s782b4996']['groupId']

        group = Group.query.filter_by(group_id=group_id).first()
        if not group:
            code = 0
            message = "success"
            text_origin = {"msg":"no group found"}
            text = base64.b64encode(json.dumps(text_origin).encode('utf-8')).decode('utf-8')
            payload = {
                "deleteGroupRes": {
                    "text": text
                }
            }
            return build_response(code, message, payload)

        Feature.query.filter_by(group_id=group_id).delete()
        Group.query.filter_by(group_id=group_id).delete()
        db.session.commit()
        code = 0
        message = "success"
        text_origin = {"msg":"success"}
        text = base64.b64encode(json.dumps(text_origin).encode('utf-8')).decode('utf-8')
        payload = {
            "deleteGroupRes": {
                "text": text
            }
        }
        return build_response(code, message, payload)
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

def searchVector(vector,group_id):
    # 获取指定 group_id 的所有特征
    features = Feature.query.filter_by(group_id=group_id).all()
    # 计算每个特征与输入向量的相似度
    max_similarity = -1
    most_similar_feature = None
        
    for feature in features:
        stored_feature = pickle.loads(feature.feature)
        similarity = VoiceProcessor.cacul_similarity(vector, stored_feature)
            
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_feature = feature
        
    return most_similar_feature
