# Copyright (C) 2020 MoveAngel and MinaProject
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

from io import BytesIO
from PIL import Image
import asyncio
import time
from datetime import datetime
from telethon import events
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pySmartDL import SmartDL
import datetime
from collections import defaultdict
import math
import os
import requests
import zipfile
import logging
import requests
import base64
import json
import telethon
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.types import DocumentAttributeVideo
from telethon.errors.rpcerrorlist import StickersetInvalidError
from telethon.errors import MessageNotModifiedError
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import (DocumentAttributeFilename, DocumentAttributeSticker,
                               InputMediaUploadedDocument, InputPeerNotifySettings,
                               InputStickerSetID, InputStickerSetShortName,
                               MessageMediaPhoto)
from userbot.modules.upload_download import progress, humanbytes, time_formatter
from userbot import bot, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, QUOTES_API_TOKEN
from userbot.events import register


if 1 == 1:
    strings = {
        "name": "Quotes",
        "api_token_cfg_doc": "API Key/Token for Quotes.",
        "api_url_cfg_doc": "API URL for Quotes.",
        "colors_cfg_doc": "Username colors",
        "default_username_color_cfg_doc": "Default color for the username.",
        "no_reply": "You didn't reply to a message.",
        "no_template": "You didn't specify the template.",
        "delimiter": "</code>, <code>",
        "server_error": "Server error. Please report to developer.",
        "invalid_token": "You've set an invalid token, get it from `http://antiddos.systems`.",
        "unauthorized": "You're unauthorized to do this.",
        "not_enough_permissions": "Wrong template. You can use only the default one.",
        "templates": "Available Templates: <code>{}</code>",
        "cannot_send_stickers": "You cannot send stickers in this chat.",
        "admin": "admin",
        "creator": "creator",
        "hidden": "hidden",
        "channel": "Channel"
    }

    config = dict({"api_url": "http://api.antiddos.systems",
                                          "username_colors": ["#fb6169", "#faa357", "#b48bf2", "#85de85",
                                                              "#62d4e3", "#65bdf3", "#ff5694"],
                                          "default_username_color": "#b48bf2"})


THUMB_IMAGE_PATH = "./thumb_image.jpg"


@register(outgoing=True, pattern="^.mmf(?: |$)(.*)")
async def mim(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("`Syntax: reply to an image with .mmf` 'text on top' ; 'text on bottom' ")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("```reply to a image/sticker/gif```")
       return
    chat = "@MemeAutobot"
    sender = reply_message.sender
    file_ext_ns_ion = "@memetime.png"
    file = await bot.download_file(reply_message.media)
    uploaded_gif = None
    if reply_message.sender.bot:
       await event.edit("```Reply to actual users message.```")
       return
    else:
     await event.edit("```Transfiguration Time! Mwahaha Memifying this image! (」ﾟﾛﾟ)｣ ```")
     await asyncio.sleep(5)
    
    async with bot.conversation("@MemeAutobot") as bot_conv:
          try:
            memeVar = event.pattern_match.group(1)
            await silently_send_message(bot_conv, "/start")
            await asyncio.sleep(1)
            await silently_send_message(bot_conv, memeVar)
            await bot.send_file(chat, reply_message.media)
            response = await bot_conv.get_response()
          except YouBlockedUserError: 
              await event.reply("```Please unblock @MemeAutobot and try again```")
              return
          if response.text.startswith("Forward"):
              await event.edit("```can you kindly disable your forward privacy settings for good, Nibba?```")
          if "Okay..." in response.text:
            await event.edit("```🛑 🤨 NANI?! This is not an image! This will take sum tym to convert to image... UwU 🧐 🛑```")
            thumb = None
            if os.path.exists(THUMB_IMAGE_PATH):
                thumb = THUMB_IMAGE_PATH
            input_str = event.pattern_match.group(1)
            if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
                os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
            if event.reply_to_msg_id:
                file_name = "meme.png"
                reply_message = await event.get_reply_message()
                to_download_directory = TEMP_DOWNLOAD_DIRECTORY
                downloaded_file_name = os.path.join(to_download_directory, file_name)
                downloaded_file_name = await bot.download_media(
                    reply_message,
                    downloaded_file_name,
                    )
                if os.path.exists(downloaded_file_name):
                    await bot.send_file(
                        chat,
                        downloaded_file_name,
                        force_document=False,
                        supports_streaming=False,
                        allow_cache=False,
                        thumb=thumb,
                        )
                    os.remove(downloaded_file_name)
                else:
                    await event.edit("File Not Found {}".format(input_str))
            response = await bot_conv.get_response()
            the_download_directory = TEMP_DOWNLOAD_DIRECTORY
            files_name = "memes.webp"
            download_file_name = os.path.join(the_download_directory, files_name)
            await bot.download_media(
                response.media,
                download_file_name,
                )
            requires_file_name = TEMP_DOWNLOAD_DIRECTORY + "memes.webp"
            await bot.send_file(  # pylint:disable=E0602
                event.chat_id,
                requires_file_name,
                supports_streaming=False,
                caption="Memifyed",
            )
            await event.delete()
            #await bot.send_message(event.chat_id, "`☠️☠️Ah Shit... Here we go Again!🔥🔥`")
          elif not is_message_image(reply_message):
            await event.edit("Invalid message type. Plz choose right message type u NIBBA.")
            return
          else: 
               await bot.send_file(event.chat_id, response.media)

def is_message_image(message):
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            return True
        if message.media.document:
            if message.media.document.mime_type.split("/")[0] == "image":
                return True
        return False
    return False
    
async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


@register(outgoing=True, pattern="^.q(?: |$)(.*)")
async def quotes(qotlti):
    if qotlti.fwd_from:
        return 
    if not qotlti.reply_to_msg_id:
       await qotlti.edit("```Reply to any user message.```")
       return
    reply_message = await qotlti.get_reply_message() 
    if not reply_message.text:
       await qotlti.edit("```Reply to text message```")
       return
    chat = "@QuotLyBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await qotlti.edit("```Reply to actual users message.```")
       return
    await qotlti.edit("```Making a Quote```")
    async with bot.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=1031952739))
              await bot.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await qotlti.reply("```Please unblock @QuotLyBot and try again```")
              return
          if response.text.startswith("Hi!"):
             await qotlti.edit("```Can you kindly disable your forward privacy settings for good?```")
          else: 
             await qotlti.delete()   
             await bot.forward_messages(qotlti.chat_id, response.message)


@register(outgoing=True, pattern="^.hz(?: |$)(.*)")
async def hazmat(hazzz):
    if hazzz.fwd_from:
        return
    if not hazzz.reply_to_msg_id:
       await hazzz.edit("`WoWoWo Capt!, we are not going suit a ghost!...`")
       return
    reply_message = await hazzz.get_reply_message()
    if not reply_message.media:
       await hazzz.edit("`Word can destroy anything Capt!...`")
       return
    chat = "@hazmat_suit_bot"
    await hazzz.edit("```Suit Up Capt!, We are going to purge some virus...```")
    async with bot.conversation("@hazmat_suit_bot") as conv:
          try:
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=905164246))
              await bot.forward_messages(chat, reply_message)
              response = await response
          except YouBlockedUserError:
              await hazzz.reply("```Unblock @hazmat_suit_bot plox```")
              return
          else:
             file = response
             await hazzz.delete()
             await hazzz.client.send_message(hazzz.chat_id, response.message, reply_to=hazzz.message.reply_to_msg_id)


@register(outgoing=True, pattern="^.pch(?: |$)(.*)")
async def quotecmd(message):  # noqa: C901
    """Quote a message.
    Usage: .pch [template]
    If template is missing, possible templates are fetched."""
        if QUOTES_API_TOKEN is None:
            await message.edit("Provide QUOTES_API_TOKEN from http://antiddos.systems/login in config.py or heroku vars first!!")
            return
        await message.edit("`Processing...`")
        args = message.raw_text.split(" ")[1:]
        if args == []:
            args = ["default"]
        reply = await message.get_reply_message()

        if not reply:
            return await message.edit(strings["no_reply"])

        if not args:
            return await message.edit(strings["no_template"])

        username_color = username = admintitle = user_id = None
        profile_photo_url = reply.from_id

        admintitle = ""
        if isinstance(message.to_id, telethon.tl.types.PeerChannel):
            try:
                user = await bot(telethon.tl.functions.channels.GetParticipantRequest(message.chat_id,
                                                                                              reply.from_id))
                if isinstance(user.participant, telethon.tl.types.ChannelParticipantCreator):
                    admintitle = user.participant.rank or strings["creator"]
                elif isinstance(user.participant, telethon.tl.types.ChannelParticipantAdmin):
                    admintitle = user.participant.rank or strings["admin"]
                user = user.users[0]
            except telethon.errors.rpcerrorlist.UserNotParticipantError:
                user = await reply.get_sender()
        elif isinstance(message.to_id, telethon.tl.types.PeerChat):
            chat = await bot(telethon.tl.functions.messages.GetFullChatRequest(reply.to_id))
            participants = chat.full_chat.participants.participants
            participant = next(filter(lambda x: x.user_id == reply.from_id, participants), None)
            if isinstance(participant, telethon.tl.types.ChatParticipantCreator):
                admintitle = strings["creator"]
            elif isinstance(participant, telethon.tl.types.ChatParticipantAdmin):
                admintitle = strings["admin"]
            user = await reply.get_sender()
        else:
            user = await reply.get_sender()

        username = telethon.utils.get_display_name(user)
        user_id = reply.from_id

        if reply.fwd_from:
            if reply.fwd_from.saved_from_peer:
                username = telethon.utils.get_display_name(reply.forward.chat)
                profile_photo_url = reply.forward.chat
                admintitle = strings["channel"]
            elif reply.fwd_from.from_name:
                username = reply.fwd_from.from_name
            elif reply.forward.sender:
                username = telethon.utils.get_display_name(reply.forward.sender)
            elif reply.forward.chat:
                username = telethon.utils.get_display_name(reply.forward.chat)

        pfp = await bot.download_profile_photo(profile_photo_url, bytes)
        if pfp is not None:
            profile_photo_url = "data:image/png;base64, " + base64.b64encode(pfp).decode()

        if user_id is not None:
            username_color = config["username_colors"][user_id % 7]
        else:
            username_color = config["default_username_color"]

        request = json.dumps({
            "ProfilePhotoURL": profile_photo_url,
            "usernameColor": username_color,
            "username": username,
            "adminTitle": admintitle,
            "Text": reply.message,
            "Markdown": get_markdown(reply),
            "Template": args[0],
            "APIKey": QUOTES_API_TOKEN
        })

        resp = requests.post(config["api_url"] + "/api/v2/quote", data=request)
        resp.raise_for_status()
        resp = resp.json()

        if resp["status"] == 500:
            return await message.edit(strings["server_error"])
        elif resp["status"] == 401:
            if resp["message"] == "ERROR_TOKEN_INVALID":
                return await message.edit(strings["invalid_token"])
            else:
                raise ValueError("Invalid response from server", resp)
        elif resp["status"] == 403:
            if resp["message"] == "ERROR_UNAUTHORIZED":
                return await message.edit(strings["unauthorized"])
            else:
                raise ValueError("Invalid response from server", resp)
        elif resp["status"] == 404:
            if resp["message"] == "ERROR_TEMPLATE_NOT_FOUND":
                newreq = requests.post(config["api_url"] + "/api/v1/getalltemplates", data={
                    "token": QUOTES_API_TOKEN
                })
                newreq = newreq.json()

                if newreq["status"] == "NOT_ENOUGH_PERMISSIONS":
                    return await message.edit(strings["not_enough_permissions"])
                elif newreq["status"] == "SUCCESS":
                    templates = strings["delimiter"].join(newreq["message"])
                    return await message.edit(strings["templates"].format(templates))
                elif newreq["status"] == "INVALID_TOKEN":
                    return await message.edit(strings["invalid_token"])
                else:
                    raise ValueError("Invalid response from server", newreq)
            else:
                raise ValueError("Invalid response from server", resp)
        elif resp["status"] != 200:
            raise ValueError("Invalid response from server", resp)

        req = requests.get(config["api_url"] + "/cdn/" + resp["message"])
        req.raise_for_status()
        file = BytesIO(req.content)
        file.seek(0)

        img = Image.open(file)
        with BytesIO() as sticker:
            img.save(sticker, "webp")
            sticker.name = "sticker.webp"
            sticker.seek(0)
            try:
                await message.delete()
                await reply.reply(file=sticker)
            except telethon.errors.rpcerrorlist.ChatSendStickersForbiddenError:
                await message.edit(strings["cannot_send_stickers"])
            file.close()


def get_markdown(reply):
    if not reply.entities:
        return []

    markdown = []
    for entity in reply.entities:
        md_item = {
            "Type": None,
            "Start": entity.offset,
            "End": entity.offset + entity.length - 1
        }
        if isinstance(entity, telethon.tl.types.MessageEntityBold):
            md_item["Type"] = "bold"
        elif isinstance(entity, telethon.tl.types.MessageEntityItalic):
            md_item["Type"] = "italic"
        elif isinstance(entity, (telethon.tl.types.MessageEntityMention, telethon.tl.types.MessageEntityTextUrl,
                                 telethon.tl.types.MessageEntityMentionName, telethon.tl.types.MessageEntityHashtag,
                                 telethon.tl.types.MessageEntityCashtag, telethon.tl.types.MessageEntityBotCommand,
                                 telethon.tl.types.MessageEntityUrl)):
            md_item["Type"] = "link"
        elif isinstance(entity, telethon.tl.types.MessageEntityCode):
            md_item["Type"] = "code"
        elif isinstance(entity, telethon.tl.types.MessageEntityStrike):
            md_item["Type"] = "stroke"
        elif isinstance(entity, telethon.tl.types.MessageEntityUnderline):
            md_item["Type"] = "underline"
        else:
            logger.warning("Unknown entity: " + str(entity))

        markdown.append(md_item)
    return markdown


CMD_HELP.update({
        "memify": 
        ".mmf texttop ; textbottom\
            \nUsage: Reply a sticker/image/gif and send with cmd."
    })

CMD_HELP.update({
        "quotly": 
        ".q \
          \nUsage: Enhance ur text to sticker."
    })

CMD_HELP.update({
        "hazmat":
        ".hz \
          \nUsage: Reply to a image / sticker to suit up!"
    })

CMD_HELP.update({
        "stickerchat": 
        ".pch \
          \nUsage: Same as quotly, enhance ur text to sticker."
    })
