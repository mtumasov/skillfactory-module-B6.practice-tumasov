from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

# get блок


@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "У {} {} альбомов.".format(artist, (len(album_names)))
        result += " Список альбомов {}: ".format(artist)
        result += ",".join(album_names)
    return result


# Post блок


@route("/albums", method="POST")
def new_album():
    album_data = {
        "year": request.forms.get("year"),
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    # Запросим список альбомов этого артиста
    album_list = album.find(album_data["artist"])
    # Получим список названий этих альбомов
    album_names = [album.album for album in album_list]
    # если такой альбом уже есть вернем ошибку
    if album_data["album"] in album_names:
        message = "такой альбом уже существует"
        response = HTTPError(409, message)
    else:  # проверяем данные  на валидность
        if not album.array_valid(album_data):
            message = "Данные введены не корректно"
            response = HTTPError(409, message)
        else:  # проверяем дату на валидность
            if not album.year_valid(album_data['year']):
                message = "Несуществующая дата"
                response = HTTPError(409, message)
            else:  # сохраняем новый альбом и уведомляем пользователя
                new_album = album.add_album(album_data)
                album.save_album(new_album)
                response = "Альбом сохранен в базе данных"
    return response


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
