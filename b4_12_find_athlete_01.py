import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime
import time 
from math import fabs

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class athelete(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'athelete'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    age = sa.Column(sa.Integer)    
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Integer)    
    name =  sa.Column(sa.Text)
    weight =  sa.Column(sa.Integer)    
    gold_medals = sa.Column(sa.Integer)    
    silver_medals = sa.Column(sa.Integer)    
    bronze_medals = sa.Column(sa.Integer)    
    total_medals = sa.Column(sa.Integer)    
    sport = sa.Column(sa.Text)
    country= sa.Column(sa.Text)

    def __repr__(self):
        return f'Атлет №:{self.id}, name:{self.name}, height:{self.height}, birthdate:{self.birthdate}'    

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

def date_diff (v_date_01, v_date_02):
    #Дата (гггг-мм-дд)
    x1 = v_date_01.split('-');
    x2 = v_date_02.split('-');
    x3 = datetime.date(int(x1[0]),int(x1[1]),int(x1[2]));
    x4 = datetime.date(int(x2[0]),int(x2[1]),int(x2[2]));
    x5 = x3-x4;
    x6 = str(x5);
    x7 = x6.split()[0];
    if v_date_01 == v_date_02:
        x7=0
    return x7

def main():
    print("1 - введите идентификатор атлета для поиска ближайших: ");
    mode = input("Выберите режим: ");
    session = connect_db();

    if mode=="1":
        user_id = input("Укажите id атлета: ");
        query = session.query(athelete).filter(athelete.id == user_id).first();
        if query:
            dt_birth = query.birthdate;
            x_height = query.height;
            print ("Вы запросили атлета :", query);
            x=0;
            user_list_dt={};
            user_list_height={};
            query_b = session.query(athelete).all();
            for q in query_b:
                if int (q.id) != int (user_id):
                    user_list_dt[q.id] = abs (float(date_diff(q.birthdate, dt_birth)));
                    if q.height is not None and x_height is not None:
                        user_list_height[q.id] = abs (q.height - x_height);
            sorted_keys1 = sorted(user_list_dt, key=user_list_dt.get) ;
            sorted_keys2 = sorted(user_list_height, key=user_list_height.get) ;
            query_dt = session.query(athelete).filter(athelete.id == sorted_keys1[0]).first();
            query_h = session.query(athelete).filter(athelete.id == sorted_keys2[0]).first();
            print ("Ближайший атлет по ДР :", query_dt);
            print ("Ближайший атлет по росту :", query_h);

        else:
            print ("Такой атлет не найден :(");

if __name__ == "__main__":
    main()