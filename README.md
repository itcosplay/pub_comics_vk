# Публикация комиксов о python в vk
Скрипт скачивает случайный комикс с сайта [xkcd.com](https://xkcd.com) и публикует его на стене
вашего сообщества на сайте [vk.com](https.vk.com)


## Необходимое окружение
* Идентификатор вашего приложения [vk.com](https://vk.com/apps?act=manage)
записанный в переменную `CLIENT_ID`
* Токен, полученный на сайте [vk.com](https://vk.com/dev/implicit_flow_user)
и записанный в переменную `VK_TOKEN`. Должны быть получены права доступа к группам и стене.
* Идентификатор вашего сообщества зависанный в переменную `GROUP_ID`

Все переменные хранятся в файле .env в корневом каталоге
```
CLIENT_ID=here_must_be_your_client_id

VK_TOKEN=here_must_be_your_token

GROUP_ID=here_must_be_your_group_id
```


## Как установить
* Клонируем репозиторий
* Создаем виртуальное окружение
* В корень проекта добавляем .env c требуемыми переменными
* Устанавливаем зависимости
```
pip install -r requirements.txt
```


## Использование
Для запуска скрипта в консоли набираем команду на запуск файла:
```
python main.py
```
Случайный комикс будет опубликовн на стене вашего сообщества вместе с комментарием автора.


## Цели проекта
Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
