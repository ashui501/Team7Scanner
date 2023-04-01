""" © Team7 || RiZoeL """

from Team7.database import users_db, scan_db
from Team7.core import Team7Scanner, assistant, SCAN_LOGS as seven_logs
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from .revertfunc import revertcallpass
from .check_reason import check_reason
from .redfunc import passcmd_to_red 

scan_cmd = """
/gban {} 
Reason: {}
Proof: {}

Note: user {} is official scanned by Team7 || Red7
"""

async def scanpass(T7, message, user, reason_code, proof):
   reason, red7code = await check_reason(reason_code)
   if user.username:
      bancmd = scan_cmd.format(user.username, reason, proof, user.first_name)
   else:
      bancmd = scan_cmd.format(user.id, reason, proof, user.first_name)

   huh = await message.reply("Passing cmd..")
   done = 0
   fail = 0
   for bot in users_db.get_all_bots():
      try:
         await assistant.send_message(bot.username, bancmd)
         done += 1
      except:
         try:
            await assistant.send_message(bot.user_id, bancmd)
            done += 1
         except:
            fail += 1

   final_text = f"User {user.mention} in scan list! \n\n cmd passed to `{done}` bots and failed in `{fail}` bots!"
   await huh.delete()
   await message.reply(final_text, reply_markup=InlineKeyboardMarkup([
                                 [
                                 InlineKeyboardButton("• Revert •", callback_data=f"revert:{user.id}")
                                 ],
                                 ]
                                 )
                                 )
   scan_db.scan_user(user.id, reason)
   try:
      await passcmd_to_red(user, red7code, proof)
   except Exception as eor:
      print(f"[Team7 Error]: {str(eor)}")
      pass
   log_msg = "**#SCAN** \n\n"
   log_msg += f"Admin: {message.from_user.mention}\n"
   log_msg += f"User: {user.mention} (`{user.id}`) \n"
   log_msg += f"Reason: `{reason}` \n"
   log_msg += f"Proof: `{proof}` \n"
   await T7.send_message(seven_logs, log_msg)
   try:
      to_user_text = f"Hey {user.mention}! \n\n You're Scanned By [Team7](https://t.me/Team7_Support_chats) \n\n Reason: {reason} \n Proof: {proof}"
      if user.username:
         await assistant.send_message(user.username, to_user_text, disable_web_page_preview=True)
      else:
         await assistant.send_message(user.id, to_user_text, disable_web_page_preview=True)
   except:
      print(f"{user.first_name} is Noob!")
      pass

async def scancallpass(T7, callback, user, reason_code, proof):
   reason, red7code = await check_reason(reason_code)
   if user.username:
      bancmd = scan_cmd.format(user.username, reason, proof)
   else:
      bancmd = scan_cmd.format(user.id, reason, proof)

   await callback.answer("passing cmd....")
   done = 0
   fail = 0
   for bot in users_db.get_all_bots():
      try:
         await assistant.send_message(bot.username, bancmd)
         done += 1
      except:
         try:
            await assistant.send_message(bot.user_id, bancmd)
            done += 1
         except:
            fail += 1
   try:
       await callback.edit_message_text(f"User {user.mention} is now in Scanlist! \n\n cmd passed to `{done}` bots and failed in `{fail}` bots!")
   except Exception:
       await callback.delete()
   scan_db.scan_user(user.id, reason_code)
   try:
      await passcmd_to_red(user, red7code, proof)
   except Exception as eor:
      print(f"[Team7 Error]: {str(eor)}")
      pass
   log_msg = "**#SCAN** \n\n"
   log_msg += f"Admin: {callback.from_user.mention}\n"
   log_msg += f"User: {user.mention} (`{user.id}`) \n"
   log_msg += f"Reason: `{reason}` \n"
   log_msg += f"Proof: `{proof}` \n"
   await T7.send_message(seven_logs, log_msg)

@Team7Scanner.on_callback_query(filters.regex(r'revert'))
async def scan_callback(T7: Team7Scanner, callback: CallbackQuery):
    query = callback.data.split(":")
    admin = callback.from_user
    message = callback.message
    if users_db.check_owner(admin.id) or users_db.check_dev(admin.id):
       user = await T7.get_users(query[1])
       await revertcallpass(T7, callback, user)
    else:
       await callback.answer("Only Team7Scanne's Owner and Devs can!") 
