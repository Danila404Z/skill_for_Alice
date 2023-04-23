import json
import random
from flask import Flask
from data.users import User
from data import db_session
from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

randoms_city = []

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

map = {
    'name': 'Карта', 'img': '1540737/9a736424f0bdd7a7b363'}



enemy_list = [
    {'name': 'ДИСПЕЧЕР', 'img': '937455/ca2af00e06e35553463f'},
    {'name': 'ВРАЧ', 'img': '1540737/d05372b3940e40006578'},
    {'name': 'ИНЖЕНЕР', 'img': '997614/d82a9562cabf518d2f34'},
    {'name': 'СПЕЦИАЛИСТ ПО КАРАНТИНУ', 'img': '1656841/b74e609ca15422b99a9e'},
    {'name': 'УЧЕНЫЙ', 'img': '1521359/0b9e7ad83c45b1177a6a'}
]


def offer_class(user_id, req, res):
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


def offer_adventure(user_id, req, res):
    count = 0
    couth = 0
    for i in req['request']['nlu']['entities']:
        if i['type'] == 'YANDEX.NUMBER':
            if couth := i['value']:
                session_state[user_id]['integer'] = couth
                print(couth)
                count = couth - 1
    nicknames(user_id, req, res, couth, count)


def difficulty_level(user_id, req, res):
    print("HELLO")

def dialog(user_id, req, res, couth, count):
    print("FFFFFFF")
    print(count)
    for entity in req['request']['nlu']['entities']:
        if entity['type'] != 'YANDEX.FIO':
            res['response']['text'] = f'Назовите имена игроков поочередно'
            count = count - 1
            return

        else:
            nicknames(user_id, req, res, couth, count)


def over(user_id, req, res):
    res['response'] = {
        "text": "Приятно познакомиться! Выберите уровень сложности",
        "buttons": [
            {
                "title": "Начальный",
                "payload": {'text': "Начальный"},
                'hide': True
            },
            {
                "title": "Средний",
                "payload": {'text': "Средний"},
                'hide': True
            },
            {
                "title": "Продвинутый",
                "payload": {'text': "Продвинутый"},
                'hide': True
            }
        ]
    }
    session_state[user_id] = {
        'state': 9
    }
    return


def nicknames(user_id, req, res, couth, count):
    if count == 0:
        res['response']['text'] = f'Назовите имя игрока'
        hehe = "ghb"
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            if nickname := entity['value'].get('first_name'):
                nickname = nickname.capitalize()
                session_state[user_id]['first_name'] = nickname
                if hehe == "ghb":
                    res['response']['text'] = f"Приятно познакомиться {nickname}"
                    names.append(nickname)
                    session_state[user_id] = {
                        'state': 11
                    }
                    return
                else:
                    res['response']['text'] = f"Приятно познакомиться {nickname}"
                    names.append(nickname)
    else:
        dialog(user_id, req, res, couth, count)


def level(user_id, req, res):
    if req['request']['payload']['text'] == "Начальный":
        pass
    elif req['request']['payload']['text'] == "Средний":
        pass
    elif req['request']['payload']['text'] == "Продвинутый":
        pass
    res['response']['text'] = 'поздравляю, вы выбрали уровень сложности, получить способность?'
    session_state[user_id] = {
        'state': 12
    }
    return


def dop_player_turn_starts(user_id, req, res):
    enemy = random.choice(enemy_list)
    res['response'] = {
        "text": f"{enemy['name']} - ваша способность, подробнее о ней вы можете прочитать в правилах",
        "card": {
            'type': "BigImage",
            "image_id": enemy['img'],
            'title': f"{enemy['name']} - способность 1 игрока. Получить способность?"
        }
    }
    session_state[user_id] = {
        'state': 15
    }


def dop_player_turn_starts1(user_id, req, res):
    enemy = random.choice(enemy_list)
    res['response'] = {
        "text": f"{enemy['name']} - ваша способность, подробнее о ней вы можете прочитать в правилах",
        "card": {
            'type': "BigImage",
            "image_id": enemy['img'],
            'title': f"{enemy['name']} - способность игрока. Игрок под номером 1, продолжить?"
        }
    }
    session_state[user_id] = {
        'state': 13
    }


def player_turn_starts(user_id, req, res):
    res['response'] = {
        "text": "Сначала нужно осуществить 4 передвижения",
        "buttons": [
            {
                "title": "Передвижение",
                "payload": {'text': "Передвижение"},
                'hide': True
            },
            {
                "title": "Колода",
                "payload": {'text': "Колода"},
                'hide': True
            },
            {
                "title": "Посмотреть карту",
                "payload": {'text': "Посмотреть карту"},
                'hide': True
            }
        ]
    }
    session_state[user_id] = {
        'state': 14
    }
    return


def level1(user_id, req, res):
    if req['request']['payload']['text'] == "Передвижение":
        pass
    elif req['request']['payload']['text'] == "Колода":
        db_sess = db_session.create_session()
        user = db_sess.query(User).all()
        player1 = []
        player2 = []
        for q in user:
            randoms_city.append(q.city)
        print(len(randoms_city))
        player1.append(random.SystemRandom().sample(randoms_city, 6))
        player2.append(random.SystemRandom().sample(randoms_city, 6))
        print(player1)
        res['response']['text'] = f'Ваша колода: \n {", ".join(*player1)}'
    elif req['request']['payload']['text'] == "Посмотреть карту":
        res['response'] = {
            "text": f"{map['name']}",
            "card": {
                'type': "BigImage",
                "image_id": map['img'],
                'title': f"{map['name']}"}
        }
    session_state[user_id] = {
        'state': 13
    }


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


def dil(user_id, req, res):
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
        res['response'] = {
            "text": "Игроки побеждают, как только изобретут все 4 лекарства \n Есть 3 варианта проигрыша игроков: \n *если маркер вспышек достиг последнего деления на треке \n *если болезнь победила \n *если карты закончились",
            "buttons": [
                {
                    "title": "Назад",
                    "payload": {'fight': True},
                    'hide': True
                }
            ]
        }
        session_state[user_id] = {
            'state': 8
        }
        return


def adventure(user_id, req, res):
    try:
        selected_class = req['request']['payload']['class']
    except KeyError:
        res['response']['text'] = 'Пожалуйста, выберете класс'
        return
    session_state[user_id].update({
        'class': selected_class,
        'state': 8
    })
    if selected_class == "ДИСПЕЧЕР":
        res['response'] = {
            'text': f"{selected_class.capitalize()} - прекраccный выбор",
            'card': {
                'type': 'BigImage',
                'image_id': player_class[selected_class]['img'],
                'title': f"{selected_class.capitalize()} может потратить действие, чтобы: *передвинуть любого игрока в город, где уже есть игрок."
            },
            'buttons': [
                {
                    "title": "Меню игроков",
                    "payload": {'fight': True},
                    'hide': True
                }
            ]
        }
        return
    elif selected_class == "ВРАЧ":
        res['response'] = {
            'text': f"{selected_class.capitalize()} - прекраccный выбор",
            'card': {
                'type': 'BigImage',
                'image_id': player_class[selected_class]['img'],
                'title': f"{selected_class.capitalize()} при лечении болезни убирает все кубики одного цвета, с лекарством убирает кубики, когда наступает на поле"
            },
            'buttons': [
                {
                    "title": "Меню игроков",
                    "payload": {'fight': True},
                    'hide': True
                }
            ]
        }
        return
    elif selected_class == "ИНЖЕНЕР":
        res['response'] = {
            'text': f"{selected_class.capitalize()} - прекраccный выбор",
            'card': {
                'type': 'BigImage',
                'image_id': player_class[selected_class]['img'],
                'title': f"{selected_class.capitalize()} тратит действие: строит исследовательскую станцию, либо может переместиться от станции к станции без карты города"
            },
            'buttons': [
                {
                    "title": "Меню игроков",
                    "payload": {'fight': True},
                    'hide': True
                }
            ]
        }
        return
    elif selected_class == "СПЕЦИАЛИСТ ПО КАРАНТИНУ":
        res['response'] = {
            'text': f"{selected_class.capitalize()} - прекраccный выбор",
            'card': {
                'type': 'BigImage',
                'image_id': player_class[selected_class]['img'],
                'title': f"{selected_class.capitalize()} предотвращает вспышки и обнаружение болезни в том городе, где находится"
            },
            'buttons': [
                {
                    "title": "Меню игроков",
                    "payload": {'fight': True},
                    'hide': True
                }
            ]
        }
        return
    elif selected_class == "УЧЕНЫЙ":
        res['response'] = {
            'text': f"{selected_class.capitalize()} - прекраccный выбор",
            'card': {
                'type': 'BigImage',
                'image_id': player_class[selected_class]['img'],
                'title': f"{selected_class.capitalize()} необходимо карты, чтобы изобрести лекарство от болезни"
            },
            'buttons': [
                {
                    "title": "Меню игроков",
                    "payload": {'fight': True},
                    'hide': True
                }
            ]
        }
        return


def prod(user_id, req, res):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = "Пожалуйста, выберите действие"
        return
    if answer:
        rules(user_id, req, res)
    else:
        res['response']['text'] = "Ты проиграл"


def player_turn(user_id, req, res):
    if req['request']['payload']['text'] == "добор карт":
        res['response']['text'] = "В игральную руку добавляются 2 карты городов, но их должно быть не больше 6"
    elif req['request']['payload']['text'] == "4 действия":
        pass
    elif req['request']['payload']['text'] == "Обнаружение болезни":
        res['response']['text'] = "Вы обнаруживаете болезни в некоторых городах, осторожно, могут возникнуть вспышки"
    session_state[user_id] = {
        'state': 10
    }


def back(user_id, req, res):
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
    states[session_state[user_id]['state']](user_id, req, res)


def main():
    db_session.global_init("db/cities.db")
    app.run()


states = {
    1: offer_class,
    2: offer_adventure,
    3: difficulty_level,
    4: end_game,
    5: dil,
    6: player_turn,
    7: adventure,
    8: prod,
    9: level,
    10: back,
    11: over,
    12: dop_player_turn_starts,
    13: player_turn_starts,
    14: level1,
    15: dop_player_turn_starts1
}
session_state = {}

if __name__ == '__main__':
    main()
