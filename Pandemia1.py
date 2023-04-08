import json
import random

from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

names = []

player_class = {
    'ЭКСПЕРТ ПО ЧС': {
        'name': 'ЭКСПЕРТ ПО ЧС',
        'img': '1540737/5799e9809279fb13040a',
    },
    'ДИСПЕЧЕР': {
        'name': 'ДИСПЕЧЕР',
        'img': '937455/ca2af00e06e35553463f',
    },
    'ВРАЧ': {
        'name': 'ВРАЧ',
        'img': '1540737/d05372b3940e40006578',
    },
    'ИНЖЕНЕР': {
        'name': 'ИНЖЕНЕР',
        'img': '997614/d82a9562cabf518d2f34',
    },
    'СПЕЦИАЛИСТ ПО КАРАНТИНУ': {
        'name': 'СПЕЦИАЛИСТ ПО КАРАНТИНУ',
        'img': '1656841/b74e609ca15422b99a9e',
    },
    'ИССЛЕДОВАТЕЛЬ': {
        'name': 'ИССЛЕДОВАТЕЛЬ',
        'img': '213044/69386cdca43d1506c595',
    },
    'УЧЕНЫЙ': {
        'name': 'УЧЕНЫЙ',
        'img': '1521359/0b9e7ad83c45b1177a6a',
    }

}


def offer_class(user_id, req, res, count=None):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = "Пожалуйста, выберите действие"
        return

    if answer:
        res['response']['text'] = "Сколько будет игроков от 2 до 4?"
        session_state[user_id] = {
            'state': 2
        }
        return
    else:
        rules(user_id, req, res)


def offer_adventure(user_id, req, res, count=None):
    for i in req['request']['nlu']['entities']:
        if i['type'] == 'YANDEX.NUMBER':
            if couth := i['value']:
                session_state[user_id]['integer'] = couth
                dialog(user_id, res, couth)
    else:
        res['response']['text'] = 'Повторите, пожалуйста.'


def dialog(user_id, res, couth):
    res['response']['text'] = "FFFFFFF"
    for i in range(couth):
        res['response']['text'] = f'Назовите имя игрока под номером {i + 1}'
        session_state[user_id] = {
            'state': 3
        }
        return


def offer_fight(user_id, req, res, count):
    print(count)
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            if name := entity['value'].get('first_name'):
                name = name.capitalize()
                session_state[user_id]['first_name'] = name
                res['response']['text'] = f"Приятно познакомиться {name}"
                names.append(name)
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
        res['response']['text'] = "Не ошибись с выбором"
        res['response']['card'] = {
            'type': "ItemsList",
            "header": {
                "text": f"Выбери, чтобы узнать способности"
            },
            "items": [
                # {
                #     "image_id": player_class['ЭКСПЕРТ ПО ЧС']['img'],
                #     "title": player_class['ЭКСПЕРТ ПО ЧС']['name'],
                #     'description': "Может сыграть карту события",
                #     "button": {
                #         "text": "Выбрать экспера по ЧС",
                #         "payload": {'class': "ЭКСПЕРТ ПО ЧС"}
                #     }
                # },
                {
                    "image_id": player_class['ДИСПЕЧЕР']['img'],
                    "title": player_class['ДИСПЕЧЕР']['name'],
                    'description': "Может двигать перемещать других игроков по карте",
                    "button": {
                        "text": "Выбрать Диспечера",
                        "payload": {'class': "ДИСПЕЧЕР"}
                    }
                },
                {
                    "image_id": player_class['ВРАЧ']['img'],
                    "title": player_class['ВРАЧ']['name'],
                    'description': "Уничтожает болезни в городе",
                    "button": {
                        "text": "Выбрать Врача",
                        "payload": {'class': "ВРАЧ"}
                    }
                },
                {
                    "image_id": player_class['ИНЖЕНЕР']['img'],
                    "title": player_class['ИНЖЕНЕР']['name'],
                    'description': "Перемещение, строительство",
                    "button": {
                        "text": "Выбрать Инженера",
                        "payload": {'class': "ИНЖЕНЕР"}
                    }
                },
                {
                    "image_id": player_class['СПЕЦИАЛИСТ ПО КАРАНТИНУ']['img'],
                    "title": player_class['СПЕЦИАЛИСТ ПО КАРАНТИНУ']['name'],
                    'description': "Предотвращает вспышки",
                    "button": {
                        "text": "Выбрать Специалиста по карантину",
                        "payload": {'class': "СПЕЦИАЛИСТ ПО КАРАНТИНУ"}
                    }
                },
                # {
                #     "image_id": player_class['ИССЛЕДОВАТЕЛЬ']['img'],
                #     "title": player_class['ИССЛЕДОВАТЕЛЬ']['name'],
                #     'description': "Может передать карту города",
                #     "button": {
                #         "text": "Выбрать Исследователя",
                #         "payload": {'class': "ИССЛЕДОВАТЕЛЬ"}
                #     }
                # },
                {
                    "image_id": player_class['УЧЕНЫЙ']['img'],
                    "title": player_class['УЧЕНЫЙ']['name'],
                    'description': "Может быстрее изобрести лекарство",
                    "button": {
                        "text": "Выбрать Ученого",
                        "payload": {'class': "УЧЕНЫЙ"}
                    }
                }
            ],
            'footer': {
                "text": "Не ошибись с выбором"
            }
        }
        session_state[user_id] = {
            'state': 7
        }
        return
    elif req['request']['payload']['text'] == "3":
        res['response']['text'] = "человек"
    elif req['request']['payload']['text'] == "4":
        res['response']['text'] = "на свеете"


def adventure(user_id, req, res, count):
    try:
        selected_class = req['request']['payload']['class']
    except KeyError:
        res['response']['text'] = 'Пожалуйста, выберете класс'
        return
    session_state[user_id].update({
        'class': selected_class,
        'state': 8
    })
    res['response'] = {
        'text': f"{selected_class.capitalize()} - прекрассный выбор",
        'card': {
            'type': 'BigImage',
            'image_id': player_class[selected_class]['img'],
            'title': f"{selected_class.capitalize()} - прекрассный выбор"
        },
        'buttons': [
            {
                "title": "В бой",
                "payload": {'fight': True},
                'hide': True
            },
            {
                "title": "Завершить приключение",
                "payload": {'fight': False},
                'hide': True
            }
        ]
    }
    return


def prod(user_id, req, res, count):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = "Пожалуйста, выберите действие"
        return
    if answer:
        res['response']['text'] = "Ты победил"
    else:
        res['response']['text'] = "Ты проиграл"


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
    6: player_turn,
    7: adventure,
    8: prod
}
session_state = {}

if __name__ == '__main__':
    app.run()
