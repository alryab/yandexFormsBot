import telebot
import time
import json

#----------------------------------------------------------------------------------------------------------------

class Sendler_Yandex_Data:

    def __init__(self, user_id, api_token: str):
        self.user_id = user_id
        self.API_TOKEN = api_token
        self.bot = telebot.TeleBot(api_token, parse_mode='HTML')
        self.WEB_HOOK_URL = f'https://raadigital.ru/yandexFormsBot/{user_id}-{api_token}'

        def webhook(json_string):
            try:
                update = telebot.types.Update.de_json(json_string)
                self.bot.process_new_updates([update])
            except Exception as e:
                pass
            return "OK"
        
        def send_Error(e):
            self.bot.send_message(self.user_id, f'При попытке отправить форму произошла ошибка\nТекст ошибки:\n<blockquote>{e}</blockquote>\n\nПри повторении этой ошибки можете обратиться за помощью (перешлите это сообщение и ссылку на форму): @alryab')

        def send_YandexForm(data):
            try:
                params_dict = json.loads(data)
                text = self.format_data(params_dict["params"])
                self.bot.send_message(user_id, text)
                return 'OK'
            except Exception as e:
                send_Error(e)
                return False

        def you_are_ready_for_forms():
            try:
                self.bot.send_message(self.user_id, f'Вы успешно зарегистрировали бота!')
            except Exception as e:
                return e

        self.webhook = webhook
        self.send_YandexForm = send_YandexForm
        self.you_are_ready_for_forms = you_are_ready_for_forms

    def format_data(self, data, indent=0):
            result = ""
            for key, value in data.items():
                if isinstance(value, dict):
                    if key != "":
                        result += " " * indent + f"{key}:\n"
                        result += self.format_data(value, indent + 2)
                else:
                    # Убираем кавычки внутри значений
                    value = str(value).replace('"', '')
                    bullet = "· " if indent > 0 else ""
                    result += " " * indent + f"{bullet}{key}: {value}\n"
            return result

    def set(self):
        try:
            self.bot.delete_webhook()
            time.sleep(1)
            self.bot.set_webhook(url=self.WEB_HOOK_URL)
        except Exception as e:
            return False
        return "OK"