import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class Users (Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Integer)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def request_data():
    print("Привет! Я запишу твои данные!");
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ");
    last_name = input("А теперь фамилию: ");
    gender = input("А теперь пол: ");
    email = input("Мне еще понадобится адрес твоей электронной почты: ");
    birthdate = input("А теперь твой ДР в формате: (YYYY-MM-DD) :");
    height = int (input("А теперь твой рост: "));

    obj = Users (
        first_name=first_name,
        last_name=last_name,
        email=email,
        gender = gender,
        birthdate = birthdate,
        height = height
    )
    return obj;

def main():
    session = connect_db();
    obj = request_data();
    if obj is not None:
        session.add(obj);
        session.commit();
        print ("Данные успешно записаны!!!");
    else:
        print ("Некорректный формат даты!!!");

if __name__ == "__main__":
    main()