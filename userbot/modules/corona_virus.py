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


@register(outgoing=True, pattern="^.covid(?: |$)(.*)")
async def corona(event):
    await event.edit("Processing...")
    country = event.pattern_match.group(1).split()
    covid = Covid()
    country_cases = covid.get_status_by_country_name(country)
    if country_cases:
        output_text = "Confirmed   : {}\n".format(country_cases["confirmed"])
        output_text += "`Active      : {}`\n".format(country_cases["active"])
        output_text += "`Deaths      : {}`\n".format(country_cases["deaths"])
        output_text += "`Recovered   : {}`\n".format(country_cases["recovered"])
        output_text += "`Last update : {}`\n". \
            format(datetime.utcfromtimestamp(country_cases["last_update"] // 1000).strftime('%Y-%m-%d %H:%M:%S'))
        output_text += f"Data provided by [Johns Hopkins University](https://j.mp/2xf6oxF)"
    else:
        output_text = "No information yet about this country!"
    await event.edit("Corona Virus Info in {}:\n\n{}".format(country.capitalize(), output_text))
    
    
CMD_HELP.update({
        "covid": 
        ".covid <country>"
        "\nUsage: Get an information about data covid-19 in your country.\n"
    })