from DatabaseConnection import Database
from telegram import *
from telegram.ext import *
from Buy import buy
class wallet (Database):
    
    def showBlance(self,update,context):
        username = self.Mysql.Search("Users","Active_ID",update.message.chat_id)[0][0]
        results = self.Mysql.Search("wallet","Username",username)[0]
        update.message.reply_text("ð°Your Balance : {}".format(results[2]),reply_markup=
        InlineKeyboardMarkup([[InlineKeyboardButton("ðµ Add Balance",callback_data="addBalance")],
        [InlineKeyboardButton("ð Exit",callback_data="Exit")]]))

    def setValue(self,Username,update):
        self.attr = "(ID,Username,Balance)"
        self.Mysql.Insert("wallet",self.attr,"('{}','{}','0')".format(update.message.chat.id,Username))


    def add_Balance(self,update,context:CallbackContext):
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id

        context.bot.edit_message_text(text="choose your add balance option ð",chat_id = chat_id,message_id = message_id,
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("ðµ 20000",callback_data="add/20000"),InlineKeyboardButton("ðµ 50000",callback_data="add/50000")],
        [InlineKeyboardButton("ðµ 70000",callback_data="add/70000"),InlineKeyboardButton("ðµ 100000",callback_data="add/100000")],[InlineKeyboardButton("ð¤ Optional",callback_data="add/Optional")],
        [InlineKeyboardButton("â Close",callback_data="Exit")]]))



    def add(self,update,context):
        balance = update.callback_query.data.split("/")[1]
        username = self.Mysql.Search("Users","Active_ID",update.callback_query.message.chat_id)[0][0]
        myBalace = self.Mysql.Search("wallet","Username",username)[0][2]

        if(balance != "Optional"):
            credit = int(balance)+int(myBalace)
            self.Mysql.Update("wallet","Balance",credit,"Username",username)
            context.bot.send_message(text = f"ð° {balance} credit added to your wallet",chat_id = update.callback_query.message.chat_id )
        else:
            context.bot.send_message(text = "enter the credit amount that you want to add:",chat_id = update.callback_query.message.chat_id ,reply_markup = ForceReply())

    def add_Optional(self,update):
        balance = update.message.text
        username = self.Mysql.Search("Users","Active_ID",update.message.chat_id)[0][0]
        myBalace = self.Mysql.Search("wallet","Username",username)[0][2]
        credit = int(balance)+int(myBalace)
        self.Mysql.Update("wallet","Balance",credit,"Username",username)
        update.message.reply_text(f"ðµ {balance} credit added to your wallet",
        reply_markup = ReplyKeyboardMarkup([[KeyboardButton("ðBack")]],resize_keyboard=True))


    def PayByCredit(self,update,context):
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
        answer = update.callback_query.data

        context.bot.edit_message_text(message_id = message_id,text = "Please wait",chat_id = update.callback_query.message.chat_id)
        if("YES" in answer):
            username = self.Mysql.Search("Users","Active_ID",update.callback_query.message.chat_id)[0][0]
            myBalace = int(self.Mysql.Search("wallet","Username",username)[0][2])
            price = int(self.Mysql.Search("Foods","Food_ID",answer.split(" ")[1])[0][3])
            ACCOUNT_DATA = self.Mysql.Search("Sellers","Food_ID",answer.split(" ")[1])[0]
            if(price <= myBalace):
                self.Mysql.Update("wallet","Balance",myBalace-price,"Username",username)
                context.bot.edit_message_text(message_id= message_id,text = "Your purchase was successfull ð",chat_id = update.callback_query.message.chat_id)
                context.bot.send_message(text = "ð´ Account Details :\n{}\nð§¾ Username â¡ï¸{}\n\nð Password â¡ï¸{}".format(20*'=',ACCOUNT_DATA[2],ACCOUNT_DATA[3]),chat_id = update.callback_query.message.chat_id ,
                reply_markup = ReplyKeyboardMarkup([[KeyboardButton("ðBack")]],resize_keyboard=True))
                # buy.removeOrder(update,context,None)
            else:
                context.bot.edit_message_text(message_id=message_id,text = "Your balance is not enough ð¥",chat_id = update.callback_query.message.chat_id)
        else:
            context.bot.edit_message_text(message_id = message_id,text = "You've canceled your purchase ð",chat_id = update.callback_query.message.chat_id)
