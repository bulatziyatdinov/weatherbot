from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 1🔎💡📲📢
btn_vote = InlineKeyboardButton(text='✅За Севу✅', callback_data='vote_for_seva')
btn_remove_vote = InlineKeyboardButton(text='❌Убрать голос❌', callback_data='devote_for_seva')
btn_share = InlineKeyboardButton(text='📢Поделиться📢', switch_inline_query='\nГОЛОСУЙТЕ ЗА СЕВУ!')
btn_prog = InlineKeyboardButton(text='🔎Программа Севы🔎', callback_data='prog_seva')
prog_prez_seva = InlineKeyboardButton(text='🔎Презентация Севы🔎', callback_data='prog_prez_seva')

btn_credits = InlineKeyboardButton(text='🔎Создатели🔎', callback_data='prog_credits')
btn_seva_group = InlineKeyboardButton(text='📎Канал Севы📎', url='https://t.me/+MLBG-JSAaAxlMjZi')

# btn_commands_admin = InlineKeyboardButton(text='/admin', callback_data='btn_admin')
# btn_commands_send = InlineKeyboardButton(text='/send', callback_data='btn_send')
# btn_commands_sended = InlineKeyboardButton(text='/sended', callback_data='btn_sended')
# btn_commands_sendown = InlineKeyboardButton(text='/sendown', callback_data='btn_sendown')
# btn_commands = InlineKeyboardButton(text='/sendown', switch_inline_query_current_chat='prog_commands')


share = InlineKeyboardMarkup(row_width=1)
vote = InlineKeyboardMarkup(row_width=2)
devote = InlineKeyboardMarkup(row_width=2)
program = InlineKeyboardMarkup(row_width=1)
admin = InlineKeyboardMarkup(row_width=2)
vote_1 = InlineKeyboardMarkup()
debates = InlineKeyboardMarkup()

seva_group = InlineKeyboardMarkup(row_width=1)
seva_group.insert(btn_seva_group)
seva_group.insert(btn_share)

share.insert(btn_share)
program.insert(btn_prog)
program.insert(btn_share)

vote.insert(btn_vote)
vote_1.add(btn_vote)
vote_1.row(btn_share)

debates.add(prog_prez_seva)
debates.row(btn_vote, btn_share)

devote.insert(btn_remove_vote)
devote.insert(btn_share)



# admin.insert(btn_commands_admin)
# admin.insert(btn_commands_send)
# admin.insert(btn_commands_sended)
# admin.insert(btn_commands_sendown)
