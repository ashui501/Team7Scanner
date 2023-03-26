""" Team7 || RiZoeL """

import re
from Team7 import Team7Users
from Team7.functions import scanpass, revertpass, get_urp, getuser, user_in_res, check_reason, rcodes
from pyrogram import filters, Client
from pyrogram.types import Message 

@Client.on_message(filters.user(Team7Users) & filters.command(["ping"], ["!", "?", "/", "."]))
async def scan_user(Team7: Client, message: Message):
    user, re, pr = await get_urp(Team7, message)
    if not user:
        return 
    if await user_in_res(message, user.id):
       return

    reason_code, _ = await check_reason(re)
    if reason_code == "Null":
       await message.reply(f"Eh! `{re}` is wrong bancode! Type /bancodes to get all bancodes!")
       return
    if pr.startswith("https://telegra.ph/file") or pr.startswith("https://telegra.ph") or pr.startswith("https://graph.org") or pr.startswith("https://graph.org/file"):
        proof = str(pr)
    else:
        await message.reply("need telegraph link as a proof!")
        return
    await scanpass(Team7, message, user, re, proof)

@Client.on_message(filters.user(Team7Users) & filters.command(["ping"], ["!", "?", "/", "."]))
async def scan_user(Team7: Client, message: Message):
    user = getuser(Team7, message)
    if not user:
        return 
    if await user_in_res(message, user.id):
       return
    await revertpass(Team7, message, user)
