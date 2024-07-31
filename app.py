import os
import jsons
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest


from model.emotion import Emotion
from model.recomm import recommandMusics
from model.musicgen import generate_music
import model.chatbot as ko_electra

import boto3
from flask_cors import CORS  # Install flask-cors package
import threading  # 이 줄을 추가합니다.


app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False #UTF-8 설정하려고 추가한 부분! 이거 없으면 스프링으로 응답 보낼 때 유니코드로 나옴

emotion = Emotion()


@app.route('/')
def isRunning():
    return "server is running"


@app.route('/chatbot/<int:chat_id>', methods=['POST']) #chat_id에 맞게 채팅방 생성, 밑에 매개변수에 꼭 있어야 함
# def reactKobertChatBot(chat_id):
def reactKoElectraChatBot(chat_id):

    # POST 요청의 본문을 추출
    message_data = request.json

    if message_data and 'messageFromFlutter' in message_data:
        message = message_data['messageFromFlutter']

        print(f"\n😀 사용자 : {message}\n")

    sentence = request.args.get("s")
    if message is None or len(message) == 0 or sentence == '\n':
        return jsonify({
            "response": "듣고 있어요. 더 말씀해주세요~"
        })

    chatbot_answer, category = ko_electra.chat(message)
    
    return jsonify({
        "response": chatbot_answer,
        "category": category
        })


# music recommand & aws comprehend

def comprehend_sentiment(text):
    # AWS CLI에서 구성된 자격 증명을 사용하여 Comprehend 클라이언트 생성
    comprehend = boto3.client('comprehend')

    # # 텍스트 감정 분석
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['SentimentScore']

    return sentiment


@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.json['text']  # Get the text from the JSON request body
    # flutter 에서 json 형식으로 key 'text', value 일기 내용 으로 넘어와야 함
    sentiment = comprehend_sentiment(text)
    result = sentiment
    return jsonify(result)



@app.route('/music/recommendation', methods=["POST"])
def recommendMusic():
    # 감정이 상수 혹은 string으로 들어와야 함(emotion.py 참고)
    data = request.json
    emotionI = data['emotion']
    
    memberID = data['memberId']
    emotionI = data['afterEmotion']
    print(f"\n📍 ID : {memberID}")
    print(f"\n📍 감정 : {emotionI}")
    
    if emotionI is None:        # 입력 베이스 감정이 없을 때
        print(emotionI)
        return None

    # bgm 생성 py 연결
    generate_music(memberID, emotionI)


    # 전체 결과 (데이터 전송용)
    # return jsonify({
    #     'empathy': empathy_results,
    #     'overcome' : overcome_results
    # })

    # 데이터 전송 형태 json -> { 키 : 리스트[{ 키 : 밸류 }, ...], 키 : 리스트[{ 키 : 밸류 }, ... ] }

if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0",port=int(os.environ.get("PORT", 5000)))
