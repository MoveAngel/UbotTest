# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port to UserBot by @MoveAngel

from datetime import datetime

from covid import Covid
from userbot import CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.corona(?: |$)(.*)")
async def corona(message):
    args = message.text.split(None, 1)
    covid = Covid()
    data = covid.get_data()
    input_str = args[1]
    country = input_str.capitalize()
    country_data = get_country_data(country, data)
    output_text = ""
    for name, value in country_data.items():
    output_text = "`Confirmed : {}\n`".format(country_data["confirmed"])
    output_text += "`Active : {}`\n".format(country_data["active"])
    output_text += "`Deaths : {}`\n".format(country_data["deaths"])
    output_text += "`Recovered : {}`\n".format(country_data["recovered"])
    output_text += "`Last update : {}`\n". \
        format(datetime.utcfromtimestamp(country_data["last_update"] // 1000).strftime('%Y-%m-%d %H:%M:%S'))
    await message.edit("**Corona Virus Info in {}**:\n\n{}".format(country.capitalize(), output_text))


def get_country_data(country, world):
    for country_data in world:
        if country_data["country"] == country:
            return country_data
    return {"Status": "No information yet about this country!"}
    
    
CMD_HELP.update({
        "covid": 
        ".corona <country>\
          \nUsage: Get an information about data covid-19 in your country.\n"
    })
