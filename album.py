import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums


def array_valid(dict):
    """
    Проверяет наличие значений в словаре 
    """
    if dict['artist'] and dict['genre'] and dict['album']:
        return True
    else:
        return False


def year_valid(str):
    """
    Проверяет корректно ли указан год
    """
    if len(str) == 4 and str.isdigit():
        if int(str) > 1900 and int(str) < 2020:
            return True
        else:
            return False
    else:
        return False


def add_album(album_data):
    """
    Трансформирует словарь в экземпляр класса
    """
    album = Album(
        year=album_data["year"],
        artist=album_data["artist"],
        genre=album_data["genre"],
        album=album_data["album"],
    )
    return album


def save_album(obj):
    """
    Cохраняет альбом в базе данных 
    """
    session = connect_db()
    # запрашиваем данные пользоватлея
    session.add(obj)
    # сохраняем все изменения, накопленные в сессии
    session.commit()