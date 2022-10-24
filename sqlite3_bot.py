# import all the libraries for the vk_api
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

# libraries with vk token and vk group_id
import _token

# library for databases
import sqlite3

# necessary global variables for the chatbot
group_id = _token.group_id
token = _token.token

# database creation
db = sqlite3.connect('action.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    userId BIGINT,
    act TEXT,
    fio TEXT,
    gender TEXT,
    age TEXT
)""")
db.commit()
userAct = '0'


def sendMsg(id, some_text):
    """
    function to send a message
    """

    vk_session.method("messages.send",
                      {"user_id": id, "message": some_text, "random_id": 0})


def fixMsg(msg):
    """
    function for string
    """

    msg = "'" + msg + "'"
    return msg


def main():
    """
    function with db
    """

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            msg = event.text.lower()
            id = event.user_id
            sql.execute(f"SELECT userId FROM users WHERE userId = '{id}'")
            if sql.fetchone() is None:
                sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                            (id, "newUser", "0", "0", "0"))
                db.commit()
                sendMsg(id,
                        "Привет, напиши 'магазин', что бы просмотреть доступные товары.")
            else:
                userAct = sql.execute(
                    f"SELECT act FROM users WHERE userId = '{id}'").fetchone()[
                    0]
                if userAct == "newUser" and msg == "магазин":
                    sendMsg(id,
                            "Товары доступные без регистрации: Хлеб, вода, овощи, фрукты. Отправь 'рег' для регистрации.")
                elif userAct == "newUser" and msg == "рег":
                    sql.execute(
                        f"UPDATE users SET act = 'getFio' WHERE userId = {id}")
                    db.commit()
                    sendMsg(id, "Напиши свое ФИО")
                elif userAct == "getFio":
                    sql.execute(
                        f"UPDATE users SET fio = {fixMsg(msg)} WHERE userId = {id}")
                    sql.execute(
                        f"UPDATE users SET act = 'getGender' WHERE userId = {id}")
                    db.commit()
                    sendMsg(id, "Твой пол?")
                elif userAct == "getGender":
                    sql.execute(
                        f"UPDATE users SET gender = {fixMsg(msg)} WHERE userId = {id}")
                    sql.execute(
                        f"UPDATE users SET act = 'getAge' WHERE userId = {id}")
                    db.commit()
                    sendMsg(id, "Сколько тебе лет?")
                elif userAct == "getAge":
                    sql.execute(
                        f"UPDATE users SET age = {fixMsg(msg)} WHERE userId = {id}")
                    sql.execute(
                        f"UPDATE users SET act = 'full' WHERE userId = {id}")
                    db.commit()
                    sendMsg(id, "Регистрация прошла успешно!")
                elif userAct == "full" and msg == "магазин":
                    sendMsg(id,
                            "Ты зарегистрированный пользователь.")


if __name__ == '__main__':
    # linking to vk
    vk_session = vk_api.VkApi(token = token)
    longpoll = VkLongPoll(vk_session)
    vk = vk_session.get_api()

    main()
