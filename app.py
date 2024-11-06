from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import yfinance as yf
from datetime import datetime
import json
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def generate_message(system_prompt, message):
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        aws_access_key_id='--',
        aws_secret_access_key='--',
        region_name='us-east-1'
    )
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    max_tokens = 1000
    user_message = {"role": "user", "content": message['message']}
    messages = [user_message]

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": messages
    })

    response = bedrock_runtime.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get('body').read())

    return response_body

@app.route('/getStockPrice', methods=['POST'])
def get_stock_price():
    message = request.get_json()
    system_prompt = ( "답변을 할때는 당시의 뉴스 기사 등을 참고해서 정확한 숫자 값을 알려줘, "
                     "무조건 답을 주고, 주가만 숫자로 알려줘, "
                     "다른 설명은 필요없고 숫자만 반환해"
                     "너의 정보는 주가에 *10 되는 경향이 있어, 이를 주의해줘, 반드시 정확한 당시의 주식 가격을 알아야해")

    try:
        result = generate_message(system_prompt, message)
        return jsonify(result.get('content')[0].get('text'))
    except (BotoCoreError, ClientError) as e:
        app.logger.error(e)
        return jsonify({"error": str(e)}), 500

@app.route('/getStockGoodEvent', methods=['POST'])
def get_stock_good_event():
    message = request.get_json()
    system_prompt = ("모든 내용에서 어떤 종목인지를 알려서는 안돼 기업이라고 바꿔서 애기해줘,"
                     " 예를 들면 엔비디아라는 걸 한글로도 영어로도 모르게 해줘"
                     "답변을 할때는 당시의 뉴스 기사 등을 참고해서 정확한 내용을 알려줘, "
                     "무조건 답을 주고 좋은 뉴스만 숫자 매겨서 최대 3건을 알려줘"
                     "앞뒤로 사족은 필요없어 숫자 부분만 답변해줘"
                     "항목별로 줄간격 추가")

    try:
        result = generate_message(system_prompt, message)
        return jsonify(result.get('content')[0].get('text'))
    except (BotoCoreError, ClientError) as e:
        app.logger.error(e)
        return jsonify({"error": str(e)}), 500

@app.route('/getStockBadEvent', methods=['POST'])
def get_stock_bad_event():
    message = request.get_json()
    system_prompt = ("모든 내용에서 어떤 종목인지를 알려서는 안돼 기업이라고 바꿔서 애기해줘,"
                     " 예를 들면 엔비디아라는 걸 한글로도 영어로도 모르게 해줘"
                     "답변을 할때는 당시의 뉴스 기사 등을 참고해서 정확한 내용을 알려줘, "
                     "무조건 답을 주고 나쁜 뉴스 안좋은 내용만 숫자 매겨서 최대 3건을 알려줘"
                     "앞뒤로 사족은 필요없어 숫자 부분만 답변해줘"
                     "항목별로 줄간격 추가")

    try:
        result = generate_message(system_prompt, message)
        return jsonify(result.get('content')[0].get('text'))
    except (BotoCoreError, ClientError) as e:
        app.logger.error(e)
        return jsonify({"error": str(e)}), 500

def get_date_14_days_before(date_str):
    date_format = "%Y-%m-%d"
    given_date = datetime.strptime(date_str, date_format)
    date_7_days_before = given_date - timedelta(days=14)
    return date_7_days_before.strftime(date_format)

def get_date_2_days_after(date_str):
    date_format = "%Y-%m-%d"
    given_date = datetime.strptime(date_str, date_format)
    date_2_days_after = given_date + timedelta(days=2)
    return date_2_days_after.strftime(date_format)

def get_historical_stock_prices(symbol, date):
    result=yf.download(symbol, start = get_date_14_days_before(date), end = get_date_2_days_after(date))
    return result

@app.route('/getStockPrices', methods=['POST'])
def get_stock_prices():
    data = request.get_json()
    symbol = data['symbol']
    date = data['date']
    result = get_historical_stock_prices(symbol, date)
    print(result)
    prices = result['Close'].round(2).values.tolist()
    flattened_prices = [price for sublist in prices for price in sublist]
    return flattened_prices

@app.route('/buyAdvice', methods=['POST'])
def buy_advice():
    message = request.get_json()
    system_prompt = ("무조건 답을 주고 다음 4가지를 항목별로 1개씩만 반드시 알려줘"
                     "good: 사야되는 이유 bad: 사면 안되는 이유 cost: 적정 주가 buy: 산다 안산다"
                     "특히 적정주가에 대해서는 말 돌리지말고 틀려도되니까 꼭 숫자로 알려주고 근거만 대줘"
                     "buy는 산다, 안산다로만 답해줘"
                     "앞뒤로 사족은 제거하고 json 형식으로 답해줘")

    try:
        result = generate_message(system_prompt, message)
        return jsonify(result.get('content')[0].get('text'))
    except (BotoCoreError, ClientError) as e:
        app.logger.error(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
