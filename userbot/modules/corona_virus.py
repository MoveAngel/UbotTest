# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port to UserBot by @MoveAngel

from covid import Covid

from userbot import CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.covid(?: |$)(.*)")
async def corona(client, message):
    await message.edit("`Processing...`")
    args = message.text.split(None, 1)
    covid = Covid()
    data = covid.get_data()
    country = args[1]
    country_data = get_country_data(country.capitalize(), data)
    if country_data:
        output_text = "`Confirmed   : {}\n`".format(country_data["confirmed"])
        output_text += "`Active      : {}`\n".format(country_data["active"])
        output_text += "`Deaths      : {}`\n".format(country_data["deaths"])
        output_text += "`Recovered   : {}`\n".format(country_data["recovered"])
        output_text += "`Last update : {}`\n". \
            format(datetime.utcfromtimestamp(country_data["last_update"] // 1000).strftime('%Y-%m-%d %H:%M:%S'))
        output_text += "`Data provided by `<a href=\"https://j.mp/2xf6oxF\">Johns Hopkins University</a>"
    else:
        output_text = "`No information yet about this country!`"
    await message.edit("**Corona Virus Info in {}**:\n\n{}".format(country.capitalize(), output_text))
    # TODO : send location of country
    # await client.send_location(message.chat.id, float(country_data["latitude"]), float(country_data["longitude"]))


def get_country_data(country, world):
    for country_data in world:
        if country_data["country"] == country:
            return country_data
    return
    
    
CMD_HELP.update({
        "covid": 
        ".covid <country>\
          \nUsage: Get an information about data covid-19 in your country.\n"
    })
