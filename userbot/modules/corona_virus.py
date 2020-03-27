# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port to UserBot by @MoveAngel

from covid import Covid

from userbot import CMD_HELP
from userbot.events import register

covid_str = (
    "**{country}:**  ✅ `{confirmed}` 🦠 `{active}` ⚠️ `{critical}` 💀 `{deaths}` 💚 `{recovered}`"
)


@register(outgoing=True, pattern="^.covid(?: |$)(.*)")
async def covid19(event):
    """Get the current covid stats for a specific country or overall."""
    covid = Covid(source="worldometers")
    match = event.matches[0].group(1)
    if match:
        strings = []
        args, _ = await client.parse_arguments(match)
        if match.lower() == "countries":
            strings = sorted(covid.list_countries())
        else:
            for c in args:
                try:
                    country = covid.get_status_by_country_name(c)
                    strings.append(covid_str.format(**country))
                except ValueError:
                    continue
        if strings:
            await event.answer(',\n'.join(strings))
    else:
        country = "Worldwide"
        active = covid.get_total_active_cases()
        confirmed = covid.get_total_confirmed_cases()
        recovered = covid.get_total_recovered()
        deaths = covid.get_total_deaths()
        string = covid_str.format(country=country,
                                  active=active,
                                  confirmed=confirmed,
                                  recovered=recovered,
                                  deaths=deaths,
                                  critical='?')
        await event.answer(string)
    
    
CMD_HELP.update({
        "covid": 
        ".covid <country>\
          \nUsage: Get an information about data covid-19 in your country.\n"
    })
