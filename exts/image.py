"""
Image extension for qrm
---
Copyright (C) 2019-2021 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import aiohttp
from datetime import datetime

import discord.ext.commands as commands

import common as cmn

import data.options as opt


class ImageCog(commands.Cog):
    gl_baseurl = "https://www.fourmilab.ch/cgi-bin/uncgi/Earth?img=ETOPO1_day-m.evif&dynimg=y&opt=-p"

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bandcharts = cmn.ImagesGroup(cmn.paths.resources / "bandcharts.1.json")
        self.maps = cmn.ImagesGroup(cmn.paths.resources / "maps.1.json")
        self.session = aiohttp.ClientSession(connector=bot.qrm.connector)

    @commands.command(name="bandplan", aliases=["plan", "bands"], category=cmn.cat.ref)
    async def _bandplan(self, ctx: commands.Context, region: str = ""):
        """Gets the frequency allocations chart for a given country."""
        async with ctx.typing():
            arg = region.lower()
            embed = cmn.embed_factory(ctx)
            if arg not in self.bandcharts:
                desc = "Possible arguments are:\n"
                for key, img in self.bandcharts.items():
                    desc += f"`{key}`: {img.name}{('  ' + img.emoji if img.emoji else '')}\n"
                embed.title = "Bandplan Not Found!"
                embed.description = desc
                embed.colour = cmn.colours.bad
                await ctx.send(embed=embed)
                return
            metadata: cmn.ImageMetadata = self.bandcharts[arg]
            if metadata.description:
                embed.description = metadata.description
            if metadata.source:
                embed.add_field(name="Source", value=metadata.source)
            embed.title = metadata.long_name + ("  " + metadata.emoji if metadata.emoji else "")
            embed.colour = cmn.colours.good
            embed.set_image(url=opt.resources_url + metadata.filename)
            await ctx.send(embed=embed)

    @commands.command(name="map", category=cmn.cat.maps)
    async def _map(self, ctx: commands.Context, map_id: str = ""):
        """Posts a ham-relevant map."""
        async with ctx.typing():
            arg = map_id.lower()
            embed = cmn.embed_factory(ctx)
            if arg not in self.maps:
                desc = "Possible arguments are:\n"
                for key, img in self.maps.items():
                    desc += f"`{key}`: {img.name}{('  ' + img.emoji if img.emoji else '')}\n"
                embed.title = "Map Not Found!"
                embed.description = desc
                embed.colour = cmn.colours.bad
                await ctx.send(embed=embed)
                return
            metadata: cmn.ImageMetadata = self.maps[arg]
            if metadata.description:
                embed.description = metadata.description
            if metadata.source:
                embed.add_field(name="Source", value=metadata.source)
            embed.title = metadata.long_name + ("  " + metadata.emoji if metadata.emoji else "")
            embed.colour = cmn.colours.good
            embed.set_image(url=opt.resources_url + metadata.filename)
            await ctx.send(embed=embed)

    @commands.command(name="grayline", aliases=["greyline", "grey", "gray", "gl"], category=cmn.cat.maps)
    async def _grayline(self, ctx: commands.Context):
        """Gets a map of the current greyline, where HF propagation is the best."""
        embed = cmn.embed_factory(ctx)
        embed.title = "Current Greyline Conditions"
        embed.colour = cmn.colours.good
        date_params = f"&date=1&utc={datetime.utcnow():%Y-%m-%d+%H:%M:%S}"
        embed.set_image(url=self.gl_baseurl + date_params)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(ImageCog(bot))
