from audiocraft.models import MusicGen
from audiocraft.models import MultiBandDiffusion
import math
import torchaudio
import torch
from audiocraft.data.audio import audio_write
import boto3
import sys

# Slack
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# Slack 클라이언트 초기화
SLACK_TOKEN = "YOUR_SLACK_TOKEN"  
SLACK_CHANNEL_MUSIC = "YOUR_SLACK_CHANNEL_ID"
slack_client = WebClient(token=SLACK_TOKEN)

def send_slack_message(message):
    try:
        response = slack_client.chat_postMessage(
            channel=SLACK_CHANNEL_MUSIC,
            text=message
        )
    except SlackApiError as e:
        print(f"Error sending message: {e}")

def print_and_slack(message):
    print(message)
    send_slack_message(message)



# MultiBandDiffusion 디코더 사용 여부 설정
USE_DIFFUSION_DECODER = False

# MusicGen 모델 초기화 (large 모델 사용)
model = MusicGen.get_pretrained('facebook/musicgen-large')
if USE_DIFFUSION_DECODER:
    mbd = MultiBandDiffusion.get_mbd_musicgen()

# 오디오 생성 파라미터 설정
model.set_generation_params(
    use_sampling=True,  # 샘플링 기반 생성 방식 사용
    top_k=250,  # 상위 250개 토큰만 고려
    duration=30  # 생성할 오디오 길이 30초
)

# AWS S3 클라이언트 초기화 및 버킷 이름 설정
s3 = boto3.client('s3')
bucket_name = 'YOUR_BUCKET_NAME'  # S3 버킷 이름

# 440Hz 비프 소리 생성 함수
def get_bip_bip(bip_duration=0.125, frequency=440,
                duration=0.5, sample_rate=32000, device="cuda"):
    t = torch.arange(int(duration * sample_rate), device="cuda", dtype=torch.float) / sample_rate
    wav = torch.cos(2 * math.pi * 440 * t)[None]
    tp = (t % (2 * bip_duration)) / (2 * bip_duration)
    envelope = (tp >= 0.5).float()
    return wav * envelope

# 감정에 따른 프롬프트 딕셔너리
emotion_prompts = {
    'joy': 'Joyful upbeat music with cheerful melodies and harmonies',
    'hope': 'Inspirational music with uplifting melodies and motivational lyrics',
    'neutrality': 'Calm and serene ambient music for relaxation and meditation',
    'sadness': 'Melancholic and emotional ballads with heartfelt lyrics',
    'anger': 'Intense and aggressive rock music with heavy riffs and powerful drums',
    'anxiety': 'Atmospheric and unsettling ambient music with tense and suspenseful vibes',
    'tiredness': 'Soothing and gentle lullabies with calming melodies and soft harmonies',
    'regret': 'Melancholic and introspective music with somber melodies and reflective lyrics'
}

# memberID와 afterEmotion 값을 받아 파일 이름 생성
def generate_file_name(memberID, emotionI):
    return f"{memberID}_{emotionI}"

def generate_music(memberID, emotionI):
    prompt = emotion_prompts.get(emotionI, "Calm and serene ambient music for relaxation and meditation")
    res = model.generate_continuation(
        get_bip_bip(0.125).expand(1, -1, -1),  # prompt의 길이는 1
        32000, [prompt],
        progress=True
    )

    # 생성된 오디오 파일 저장 및 S3 업로드
    file_name = generate_file_name(memberID, emotionI)
    audio_write(file_name, res[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)


    # 파일 존재 여부 확인
    import os
    if os.path.isfile(f"{file_name}.wav"):
        # S3에 WAV 파일 업로드
        s3.upload_file(f"{file_name}.wav", bucket_name, f"{file_name}.wav")
        print_and_slack(f'\n🎵 {file_name}.wav 파일이 S3 버킷에 업로드되었습니다.\n')  
    else:
        print_and_slack(f'\n{file_name}.wav 파일이 존재하지 않습니다.\n')
