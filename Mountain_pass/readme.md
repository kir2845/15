# Проект виртуальной стажировки по разработке мобильного приложения

 ## Постановка задачи
 Разработка мобильного приложения для Федерации спортивного туризма России (далее - Федерация) - организации, занимающейся развитием и популяризацией спортивного туризма в России и осуществляющей надзор за проведением всероссийских соревнований по этому виду спорта.

 Пользователями мобильного приложения для Android и IOS будут являться туристы, предоставляющие информацию о посещаемых ими горных объектах (вершина, перевал, ущелье, ледник, водопад и т.д.). Добавленные в приложении данные будут отправляться в Федерацию, при появлении доступа в Интернет. 
 
 После проверки модератором информация, полученная от пользователя, вносится в базу данных. При этом пользователю в мобильном приложении доступен просмотр статуса модерации добавленных данных и база данных объектов, внесенных другими пользователями.
 

## Описание проекта

 ### Модели базы данных
 Пользователю в мобильном приложении доступны следующие действия:
 
 1 Внесение и отправка личной информации (регистрация не обязательна):
 - фамилия;
 - имя;
 - отчество;
 - электронная почта;
 - номер телефона;

 2 Внесение и отправка информации о новом объекте:
 - страна или регион;
 - категория;
 - название;
 - альтернативное название;
 - соединение с другими объектами, описание маршрута, комментарии;
 - статус данных;
 - способ прохождения маршрута;
 - координаты и высота;
 - уровень сложности прохождения маршрута в зависимости от времени года;
 - несколько фотографий;

 3 Редактирование данных, не просмотренных модератором;
 
 4 Просмотр информации об объектах, добавленных другими пользователями;
 
 5 Просмотр информации об объектах, добавленных одним пользователем по его электронной почте.
 
Для внесения данных используются разработанные модели базы данных с соответствующими полями – основная модель Peak (общая информация об объекте) и вспомогательные модели Author (информация о пользователе), Coordinate (координаты и высота объекта), Level (уровень сложности в зависимости от времени года), Image (фотографии объекта).
 
 Уровень сложности прохождения маршрута (level) заполняется в соответствии с предложенным списком (допустимые значения):

 LEVEL = [
      ('', 'не указано'),
      ('1a', '1A'),
      ('1b', '1Б'),
      ('2a', '2А'),
      ('2b', '2Б'),
      ('3a', '3А'),
      ('3b', '3Б'),
      ('4a', '4А'),
      ('4b', '4Б'),
      ('5a', '5А'),
      ('5b', '5Б'),]

 При добавлении информации о новом объекте заполняется поле status, имеющее следующие допустимые значения:
 - new – новый;
 - pending («ожидающий рассмотрения») – модератор взял в работу;
 - accepted («принято») – модерация прошла успешно;
 - rejected («отвергнутый») – модерация прошла, информация не принята.

 ## Методы API
 ### 1 Метод POST /submitData/
 Данный метод используется для добавления информации о новом объекте и принимает запрос в формате JSON. 
 
 Пример запроса JSON:
 
{
    "country": "РФ",
    "category": "перевал",
    "title": "Озерный",
    "other_titles": "",
    "connect": "соединяет две горы",
    "status": "new",
    "method_of_passage": "пешком",
    "user": {
        "surname": "Бабкин",
        "name": "Андрей",
        "patronymic": "Юрьевич",
        "email": "kir2845@mail.ru",
        "telephone": "+79518001704"
    },
    "coords": {
        "latitude": 15.3842,
        "longitude": 87.15201,
        "height": 3200
    },
    "level": {
        "winter": "1b",
        "spring": "",
        "summer": "1a",
        "autumn": "1a"
    },
    "images": [{"title": "перевал", "photo": "https://dicovage.com/image/data/journal2/blog/cikavinki/Dorohu/190.jpg"}]
}

 Результатом выполнения метода является JSON-ответ, содержащий следующие данные: 
 
 status – код HTTP, целое число:
 
    - 200 – успешно;   
    - 400 – Bad Request (при нехватке полей);  
    - 500 – ошибка при выполнении операции;
 
 message – сообщение, строка:
 
   - причина ошибки (если она была);
   - запись успешно добавлена;
 
 id – идентификатор, который был присвоен объекту при добавлении в базу данных (при успешной отправке).
 
 Примеры ответов:
 
   {"status": 200, "message": "Запись успешно добавлена", "id": 12}
   
   {"status": 500, "message": "Ошибка подключения к базе данных", "id": null}

 ### 2 Метод GET /submitData/
 Данный метод позволяет получить данные обо всех объектах базы данных, представленные в формате JSON. 

 ### 3 Метод GET /submitData/<pk:int>
 Данный метод позволяет получить данные об одном объекте по его идентификатору, представленные в формате JSON.
 
 Пример JSON ответа (GET /submitData/1/):
 
{
    "id": 1,
    "country": "РФ",
    "category": "горная вершина",
    "title": "Сугомак",
    "other_titles": "нет другого",
    "connect": "нет",
    "add_time": "2023-10-04T14:52:20.198780Z",
    "status": "new",
    "method_of_passage": "легкая пешая прогулка",
    "user": {
        "id": 1,
        "surname": "Бабкин",
        "name": "Андрей",
        "patronymic": "Юрьевич",
        "email": "kir2845@mail.ru",
        "telephone": "+79518001704"
    },
    "coords": {
        "latitude": 65.3842,
        "longitude": 17.15251,
        "height": 2200
    },
    "level": {
        "winter": "",
        "spring": "",
        "summer": "1a",
        "autumn": ""
    },
    "images": [
        {
            "title": "вершина1",
            "photo": "https://nashural.ru/assets/uploads/ekk28.jpg"
        }
    ]
}
 
 ### 4 Метод GET /submitData/ ?user_email=email
 Данный метод возвращает информацию обо всех объектах, отправленных на сервер пользователем с почтой email. 
 
 Пример запроса:
 
 GET /submitData/?user_email=kir2845@mail.ru

 ### 5 Метод PATCH /submitData/<pk:int>
 Данный метод позволяет отредактировать существующую запись (заменить), если последняя находится в статусе модерации 'new'. При этом редактировать можно все поля, кроме данных пользователя – ФИО, адреса электронной почты и номера телефона. Метод принимает запрос в формате JSON, аналогичный методу POST /submitData/.
 
 В качестве результата изменения получим ответ, содержащий следующие данные:
 
 state:
 
    - 1 – если успешно удалось отредактировать запись в базе данных;
    - 0 – отредактировать запись не удалось;
 
 message: – сообщение об успешном редактировании либо о причине неудачного обновления записи.
 
Пример JSON-ответа:

 PATCH /submitData/1/
 HTTP 200 OK
 Allow: GET, HEAD, PATCH, OPTIONS
 Content-Type: application/json
 Vary: Accept

{
    "state": 1,
    "message": "Запись успешно отредактирована",
    "id": 1
}

