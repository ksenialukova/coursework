import telebot
import config
import dbworker

bot = telebot.TeleBot(config.token)


# /start            +
# main_view         +
# /addexpense       +
# type_expense      +
# price             +
# /addincome
# /reset
# setting(удаление пользователя)

# /plancost
# /boardcosts
# /statistic
# /help
# /setting(настройка граничных цен)


@bot.message_handler(commands=["start"])
def start(message):
    dbworker.add_user(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username)
    main_view(message)


@bot.message_handler(commands=["addexpense"])
def addexpense(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('coffee', 'food')
    keyboard.row('/help', '/reset')
    keyboard.row('/mainmenu')
    bot.send_message(message.chat.id, "Choose type of expense: ", reply_markup=keyboard)
    dbworker.set_state(message.chat.id, config.State.S_ENTER_TYPE_EXPENSE, message.chat.username)


@bot.message_handler(commands=["addincome"])
def addincome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('salary', 'pozhertvovanie gosudarstva')
    keyboard.row('/help', '/reset')
    keyboard.row('/mainmenu')
    bot.send_message(message.chat.id, "Choose type of income: ", reply_markup=keyboard)
    dbworker.set_state(message.chat.id, config.State.S_ENTER_TYPE_INCOME, message.chat.username)


@bot.message_handler(commands=["mainmenu"])
def mainmenu(message):
    main_view(message)


@bot.message_handler(commands=["help"])
def helper(message):
    bot.send_message(message.chat.id, "allfunction")


@bot.message_handler(commands=["reset"])
def reset(message):
    dbworker.set_state(message.chat.id, config.State.S_START, message.chat.username)
    dbworker.drop_table(message.chat.id)
    main_view(message)


@bot.message_handler(commands=["setting"])
def setting(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('/deleteuser')
    keyboard.row('/setboardcosts')
    keyboard.row('/help')
    keyboard.row('/reset')
    bot.send_message(message.chat.id, 'enter please', reply_markup=keyboard)


@bot.message_handler(commands=["setboardcosts"])
def board(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('coffee')
    keyboard.row('food')
    keyboard.row('/help')
    keyboard.row('/reset')
    bot.send_message(message.chat.id, 'enter please', reply_markup=keyboard)
    dbworker.set_state(message.chat.id, config.State.S_ENTER_BOARDCOST, message.chat.username)


@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) ==
                                                                  config.State.S_ENTER_BOARDCOST)
def type_board(message):
    btype = message.text
    dbworker.drop_table(message.chat.id)
    dbworker.temp_table_expense(message.chat.id, btype)
    dbworker.set_state(message.chat.id, config.State.S_ENTER_BOARDPRICE, message.chat.username)
    bot.send_message(message.chat.id, 'Enter sum, please')


@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) ==
                                                                  config.State.S_ENTER_BOARDPRICE)
def price(message):
    try:
        price = float(message.text)
        dbworker.add_board(message.chat.id, price)
        bot.send_message(message.chat.id, 'Your boarderprice was saved')
        dbworker.set_state(message.chat.id, config.State.S_ENTER_TYPE_EXPENSE, message.chat.username)
    except ValueError:
        bot.send_message(message.chat.id, 'Try something else, my love')
        print("Error type")


@bot.message_handler(commands=['boarderprice'])
def see_board(message):
    res = dbworker.print_board(message.chat.id)
    if res:
        for i in res:
            name, price = i
            bot.send_message(message.chat.id, '{0}: {1}'.format(name, price))
    else:
        bot.send_message(message.chat.id, 'You havent any boarder price')


@bot.message_handler(commands=["deleteuser"])
def deleting(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('/yes', '/no')
    keyboard.row('/reset')
    bot.send_message(message.chat.id, 'Are you sure? If you press \'yes\' all data will be deleted', reply_markup=keyboard)


@bot.message_handler(commands=["yes"])
def delet(message):
    dbworker.drop_table(message.chat.id)
    dbworker.del_info(message.chat.id)
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('/start')
    bot.send_message(message.chat.id, 'Ok, goodbye.\nI thought we were friends', reply_markup=keyboard)


@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) ==
                                                                  config.State.S_ENTER_TYPE_EXPENSE)
def type_expense(message):
    ex_type = message.text
    dbworker.drop_table(message.chat.id)
    dbworker.temp_table_expense(message.chat.id, ex_type)
    dbworker.set_state(message.chat.id, config.State.S_ENTER_PRICE, message.chat.username)
    bot.send_message(message.chat.id, 'Enter sum, please')


@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) ==
                                                                  config.State.S_ENTER_PRICE)
def price(message):
    try:
        price = float(message.text)
        dbworker.add_expense(message.chat.id, price)
        bot.send_message(message.chat.id, 'Your expense was saved')
        dbworker.set_state(message.chat.id, config.State.S_ENTER_TYPE_EXPENSE, message.chat.username)
    except ValueError:
        bot.send_message(message.chat.id, 'Try something else, my love')
        print("Error type")


@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) ==
                                                                  config.State.S_ENTER_TYPE_INCOME)
def type_income(message):
    in_type = message.text
    dbworker.drop_table(message.chat.id)
    dbworker.temp_table_income(message.chat.id, in_type)
    dbworker.set_state(message.chat.id, config.State.S_ENTER_INCOME, message.chat.username)
    bot.send_message(message.chat.id, 'Enter sum, please')
    bot.send_message(message.chat.id, 'PS If you want enter float number you will use dot, not comma(56.6)')


@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) ==
                                                                  config.State.S_ENTER_INCOME)
def price(message):
    try:
        price = float(message.text)
        dbworker.add_income(message.chat.id, price)
        bot.send_message(message.chat.id, 'Your income was saved')
        dbworker.set_state(message.chat.id, config.State.S_ENTER_TYPE_INCOME, message.chat.username)
    except ValueError:
        bot.send_message(message.chat.id, 'Try something else, my love')
        print("Error type")


@bot.message_handler(commands=["statistic"])
def stat(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('/bymessage')
    keyboard.row('/sendPDF')
    keyboard.row('/reset')
    bot.send_message(message.chat.id, "Choose:", reply_markup=keyboard)


@bot.message_handler(commands=["bymessage"])
def stat1(message):
    line = ''
    res = dbworker.income_stat(message.chat.id)
    if res:
        line += 'INCOME:\n'
        for i in res:
            name, price = i
            line += '{0}: {1}\n'.format(name, price)

    res = dbworker.outcome_stat(message.chat.id)
    if res:
        line += '\nOUTCOME:\n'
        for i in res:
            name, price = i
            line += '{0}: {1}\n'.format(name, price)
    bot.send_message(message.chat.id, line)


@bot.message_handler(commands=["sendPDF"])
def sendPDF(message):
    dbworker.createPDF(message.chat.id)
    bot.send_document(message.chat.id, open('report228568230.pdf', 'rb'))

def main_view(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('/addexpense', '/addincome')
    keyboard.row('/boarderprice', '/statistic')
    keyboard.row('/help', '/setting')
    keyboard.row('/reset')
    bot.send_message(message.chat.id, "Lets start", reply_markup=keyboard)


if __name__ == "__main__":
    bot.polling()
