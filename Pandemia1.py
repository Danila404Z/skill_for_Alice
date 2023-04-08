import json
import random

from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

count = -5


def offer_class(user_id, req, res, count):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = "Пожалуйста, выберите действие"
        return

    if answer:
        res['response']['text'] = "Сколько будет игроков от 2 до 4?"
        print(count)
        count = -5
        # offer_adventure(user_id, req, res, count)
        session_state[user_id] = {
            'state': 2
        }
        return
    else:
        rules(user_id, req, res)


def offer_adventure(user_id, req, res, count):
    for i in req['request']['nlu']['entities']:
        if i['type'] == 'YANDEX.NUMBER':
            if couth := i['value']:
                session_state[user_id]['integer'] = couth
                print(couth)
                for i in range(couth):
                    res['response']['text'] = f'Назовите имя игрока под номером {i + 1}'
                    session_state[user_id] = {
                                     'state': 3
                                 }
                    return
    else:
        res['response']['text'] = 'Повторите, пожалуйста.'


def offer_fight(user_id, req, res, count):
    print(count)
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            if name := entity['value'].get('first_name'):
                name = name.capitalize()
                session_state[user_id]['first_name'] = name
                res['response']['text'] = f"Приятно познакомиться {name}"
                session_state[user_id] = {
                    'state': 2
                }
                return
                

def end_game(user_id, req, res):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = "Пожалуйста, выбери действие"
        return
    if not answer:
        res['response']['text'] = "Ваше приключение закончилось, не успев начаться"
    else:
        res['response']['text'] = "Вы победили противника, о вашем подвиге не забудут"
    res['response']['end_session'] = True


@app.route('/post', methods=['POST'])
def get_alice_request():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)
    return jsonify(response)


def rules(user_id, req, res):
    res['response'] = {
        "text": "О чем вы хотите узнать больше? \n ход игрока, роли, карточки,  конец игры",
        "buttons": [
            {
                "title": "Ход игрока",
                "payload": {'text': "1"},
                'hide': True
            },
            {
                "title": "Профессии",
                "payload": {'text': "2"},
                'hide': True
            },
            {
                "title": "Карточки",
                "payload": {'text': "3"},
                'hide': True
            },
            {
                "title": "Конец игры",
                "payload": {'text': "4"},
                'hide': True
            }
        ]
    }
    session_state[user_id] = {
        'state': 5
    }
    return


def dil(user_id, req, res, count):
    if req['request']['payload']['text'] == "1":
        res['response'] = {
            "text": "Ход игрока состоит из нескольких шагов: \n *каждый ход у игрока есть  4 действия;\n *добрать карты игроков;\n *обнаружить болезнь",
            "buttons": [
                {
                    "title": "4 действия",
                    "payload": {'text': "4 действия"},
                    'hide': True
                },
                {
                    "title": "добор карт",
                    "payload": {'text': "добор карт"},
                    'hide': True
                },
                {
                    "title": "Обнаружение болезни",
                    "payload": {'text': "Обнаружение болезни"},
                    'hide': True
                }
            ]
        }
        session_state[user_id] = {
            'state': 6
        }
        return
    elif req['request']['payload']['text'] == "2":
        res['response']['text'] = "лучший"
    elif req['request']['payload']['text'] == "3":
        res['response']['text'] = "человек"
    elif req['request']['payload']['text'] == "4":
        res['response']['text'] = "на свеете"


def player_turn(user_id, req, res, count):
    if req['request']['payload']['text'] == "добор карт":
        res['response']['text'] = "В игральную руку добавляются 2 карты городов, но их должно быть не больше 6"
    elif req['request']['payload']['text'] == "4 действия":
        pass
    elif req['request']['payload']['text'] == "Обнаружение болезни":
        res['response']['text'] = "Вы обнаруживаете болезни в некоторых городах, осторожно, могут возникнуть вспышки"
    res['response'] = {
        "text": "Назад?",
        "buttons": [
            {
                "title": "Назад",
                "payload": {'text': "1"},
                'hide': True
            }
        ]
    }
    session_state[user_id] = {
        'state': 5
    }
    return


def handle_dialog(req, res):
    count = -5
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response'] = {
            "text": "Привет! Добро пожаловать в навык 'Пандемия'. Как будешь готов скажи: 'Я готов!'  и мы начнём игру. Если ты не знаком с правилами игры, то скажи 'Правила'",
            "buttons": [
                {
                    "title": "Я готов!",
                    "payload": {'fight': True},
                    'hide': True
                },
                {
                    "title": "Правила",
                    "payload": {'fight': False},
                    'hide': True
                },

            ]
        }
        session_state[user_id] = {
            'state': 1
        }
        return
    states[session_state[user_id]['state']](user_id, req, res, count)


states = {
    1: offer_class,
    2: offer_adventure,
    3: offer_fight,
    4: end_game,
    5: dil,
    6: player_turn
}
session_state = {}

if __name__ == '__main__':
    app.run()
