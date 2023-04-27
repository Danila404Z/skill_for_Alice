from flask import Flask
from data.users import User
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/cities.db")
    # app.run()

    # user = User()
    db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.commit()
    user = db_sess.query(User).all()
    for q in user:
        print(q.city)


if __name__ == '__main__':
    main()