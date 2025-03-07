import os
import torch
import soundfile as sf
import numpy as np
from models_code.ecapa_tdnn import ECAPA_TDNN
from models_code.ECAPAModel import ECAPAModel
import warnings
from torchaudio.transforms import MelSpectrogram
import subprocess

warnings.filterwarnings('ignore')

class VoiceProcessor:
    def __init__(self, model_path):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self._load_model(model_path)
        
    def _load_model(self, model_path):
        """加载预训练模型"""
        model = ECAPAModel(lr=0.001, lr_decay=0.95, C=1024, n_class=5994, m=0.2, s=30, test_step=10)
        # 加载模型参数
        model.load_parameters(model_path)
        # 将模型设置为评估模式
        model.eval()
        return model.to(self.device)

    def extract_feature(self, audio_path):
        """提取声纹特征向量"""
        # 转换音频文件格式
        converted_audio_path = audio_path.replace('.wav', '_converted.wav')
        ffmpeg_command = f'ffmpeg -y -i "{audio_path}" -ac 1 -vn -acodec pcm_s16le -ar 16000 "{converted_audio_path}"'
        result = subprocess.run(ffmpeg_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"ffmpeg command failed with exit code {result.returncode}")
            print(f"ffmpeg stdout: {result.stdout.decode('utf-8')}")
            print(f"ffmpeg stderr: {result.stderr.decode('utf-8')}")
            raise RuntimeError(f"ffmpeg command failed with exit code {result.returncode}")

        # 读取音频文件
        audio, _ = sf.read(converted_audio_path)

        # 处理音频数据
        max_audio = 300 * 160 + 240
        if audio.shape[0] <= max_audio:
            shortage = max_audio - audio.shape[0]
            audio = np.pad(audio, (0, shortage), 'wrap')
        feats = []
        startframe = np.linspace(0, audio.shape[0] - max_audio, num=5)
        for asf in startframe:
            feats.append(audio[int(asf):int(asf) + max_audio])
        feats = np.stack(feats, axis=0).astype(float)

        # 转换为张量
        data = torch.FloatTensor(feats).to(self.device)

        # 提取嵌入向量
        with torch.no_grad():
            embedding = self.model.speaker_encoder.forward(data, aug=False)
            embedding = torch.nn.functional.normalize(embedding, p=2, dim=1)

        return embedding.cpu().numpy()

    @staticmethod
    def cacul_similarity(embedding1, embedding2):
        # 确保输入是 Tensor 类型
        if not isinstance(embedding1, torch.Tensor):
            embedding1 = torch.tensor(embedding1)
        if not isinstance(embedding2, torch.Tensor):
            embedding2 = torch.tensor(embedding2)
        
        similarity = torch.mean(torch.matmul(embedding1, embedding2.T))
        return similarity.item()
