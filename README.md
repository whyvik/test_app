## test_app (FastAPI / PostgreSQL)

Реализовать RESTful API для системы учета транзакций (Фрэймворк на выбор / БД на выбор). 

Эндпоинты:
1) Авторизация. Параметры: email и пароль
2) Записать транзакцию: Параметры: Сумма (Число), Дата(Дата без времени), Категория (Строка) /  Доступно авторизованным пользователям
3) Получить все записанные пользователем тарнзакции (включая прошлые сессии) / Ответ в формате JSON / Доступно авторизованным пользователям

Варианты использования:
1) Пользователь авторизуется исползуя эндпоинт (1) (если такого пользователя нет то он создается) получает сессионный токен.
2) Пользователь записывает транзакции используя эндпоинт (2)
3) Пользователь может прочитать все свои транзакции используя эндпоинт (3)

Доп. требования (не обязательные но будут плюсом):
- В связи с необходимостью защиты персональных данных, в БД нужно обеспечить безопасное хранение email, пароля так чтобы в случае кражи БД злоумышленники не смогли использовать данные и при этом обеспечить быструю работу запросов (2) и (3).
- Если возможно, реализовать так чтобы не хранить значения пароля в отдельных полях таблицы БД или где либо на бэкенд.