#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask
import re
from flask import Flask, send_file
from yandex_forms_bot.send_data_form import Sendler_Yandex_Data

app = Flask(__name__)
USER_BOT = None

def yandex_forms_handler(param1=None, param2=None):
    global USER_BOT
    if param1 is not None and param2 is not None:
        # Обработка /yandexFormsBot/<int:param1>/<path:param2>
        param2 = param2.replace('/', '')
        admin_id = param1
        api_token = param2
        result = yandex_webhook(admin_id, api_token)
        USER_BOT = None
        return result

def register_bot(admin_id, api_token):
    global USER_BOT
    try:
        if not USER_BOT or USER_BOT.user_id != admin_id or USER_BOT.API_TOKEN != api_token:
            USER_BOT = Sendler_Yandex_Data(admin_id, api_token)
            if USER_BOT.set():
                try_send_message = USER_BOT.you_are_ready_for_forms()
                check_error = extract_error_code(str(try_send_message))
                USER_BOT = None
                if not check_error:
                    return "OK"
                else:
                    if check_error == 400:
                        message = 'Вы не нажaли "СТАРТ" в своем боте. Нажмите "СТАРТ"'
                    else: 
                        message = str(try_send_message)
                    return flask.jsonify({'status_code':check_error, 'message':message}), check_error
            USER_BOT = None
            return False
    except Exception as e:
        return False
    return False

def extract_error_code(message):
    """
    Проверяет наличие "Error code" в сообщении и извлекает код ошибки.
    
    Args:
        message (str): Текст сообщения, которое нужно проверить.
        
    Returns:
        int or False: Код ошибки, если найден, иначе False.
    """
    pattern = r"Error code:\s*(\d+)"
    match = re.search(pattern, message)
    if match:
        return int(match.group(1))
    return False

def yandex_webhook(admin_id, api_token):
    global USER_BOT
    try:
        if not USER_BOT or USER_BOT.user_id != admin_id or USER_BOT.API_TOKEN != api_token:
            USER_BOT = Sendler_Yandex_Data(admin_id, api_token)
            json_string = flask.request.get_data().decode('unicode_escape')
            json_string = json_string.replace('"{', '{').replace('}"', '}')
            result = USER_BOT.send_YandexForm(json_string)
            USER_BOT = None
    except Exception as e:
        send_error_message(admin_id, api_token, e)
        return False
    return result

def send_error_message(admin_id, api_token, e):
    global user_bot
    try:
        if not user_bot or user_bot.user_id != admin_id or user_bot.API_TOKEN != api_token:
            user_bot = Sendler_Yandex_Data(admin_id, api_token)
            user_bot.send_Error(e)
            user_bot = None
    except:
        pass

@app.route("/yandexFormsBot/<int:param1>/<path:param2>", methods=['POST'])
def send_data_to_handler(param1, param2):
    return yandex_forms_handler(param1, param2)
        
@app.route("/addYandexFormBot", methods=['GET'])
def create_bot_for_forms_html():
    return send_file('yandex_forms_bot//static/index.html')

@app.route("/addYandexFormBot/<int:param1>/<path:param2>", methods=['POST'])
def create_bot_for_forms_register(param1, param2):
    return register_bot(param1, param2)

if __name__ == "__main__":
    app.run(host='0.0.0.0')