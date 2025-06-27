# from dotenv import load_dotenv
## .env 파일에 있는 OpenAI API 키 등을 환경 변수로 불러오기 위해 사용
# load_dotenv()  # .env 내용을 읽어서 환경변수로 설정

# streamlit-cloud에서는 .env를 사용할 수 없으므로
# secrets설정(TOML)에 OPENAI_API_KEY를 설정해야 한다.
# OPENAI_API_KEY="키"

from openai import OpenAI
import os
import base64

client = OpenAI()

# STT (음성을 텍스트로 변환)
def stt(audio):
    # 파일로 변환
    filename = 'prompt.mp3'
    audio.export(filename, format='mp3') # 사용자가 녹음한 음성을 mp3로 저장

    # whisper-1 모델로 stt, mp3 파일을 텍스트로 변환
    with open(filename, 'rb') as f:
        transcription = client.audio.transcriptions.create(
            model='whisper-1',
            file=f
        )
    # 음원파일 삭제
    os.remove(filename)
    return transcription.text

#ChatGPT로 질의 및 응답 받기
def ask_gpt(messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        top_p=1,
        max_tokens=4096
    )
    return response.choices[0].message.content

# TTS (텍스트를 음성으로 변환)
def tts(response):
    filename = 'voice.mp3'
    with client.audio.speech.with_streaming_response.create(
            model='tts-1',
            voice='alloy',
            input=response
    ) as stream:
        stream.stream_to_file(filename)

    # 음원을 base64문자열로 인코딩 처리
    with open(filename, 'rb') as f:
        data = f.read()
        base64_encoded = base64.b64encode(data).decode()
    # 음원파일 삭제
    os.remove(filename)
    return base64_encoded