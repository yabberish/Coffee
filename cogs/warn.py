import json
import random
import ast
from datetime import datetime
import os

import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions

with open("data/embed_colors.txt") as f:
    data = f.read()
    colors = ast.literal_eval(data)
    color_list = [c for c in colors.values()]

class Warn(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='warn',
        description='Warn server members for breaking rules.',
        usage=';;warn <@user> for being rude!'
    )
    @has_permissions(manage_messages=True)
    async def warn_command(self, ctx, user:discord.Member, *, reason:str):
        if user.id == self.bot.user.id:
            await ctx.send("Are you seriously trying to warn me?")
            return
        if user.bot == 1:
            await ctx.send("Bots aren't able to be warned sorry.")
            return
        if user == ctx.author:
            await ctx.send("Do you really wanna play yourself?")
            return
        if user.guild_permissions.manage_messages == True:
            await ctx.send("The specified user has the \"Manage Messages\" permission (or higher) inside the guild/server.")
            return
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if not os.path.exists("data/warns/" + str(ctx.guild.id) + "/"):
            os.makedirs("data/warns/" + str(ctx.guild.id) + "/")
        try:
            with open(f"data/warns/{str(ctx.guild.id)}/{str(user.id)}.json") as f:
                data = json.load(f)
        except FileNotFoundError:
            with open(f"data/warns/{str(ctx.guild.id)}/{str(user.id)}.json", "w") as f:
                data = ({
                    'offender_name':user.name,
                    'warns':1,
                    1:({
                        'warner':ctx.author.id,
                        'warner_name':ctx.author.name,
                        'reason':reason,
                        'channel':str(ctx.channel.id),
                        'datetime':dt_string
                    })
                })
                json.dump(data, f)
            embed = discord.Embed(
                title=f"{user.name}'s new warn",
                color=random.choice(color_list)
            )
            embed.set_author(
                name=ctx.message.author.name,
                icon_url=ctx.message.author.avatar_url,
                url=f"https://discord.com/users/{ctx.message.author.id}/"
            )
            embed.add_field(
                name="Warn 1",
                value=f"Warner: {ctx.author.name} (<@{ctx.author.id}>)\nReason: {reason}\nChannel: <#{str(ctx.channel.id)}>\nDate and Time: {dt_string}",
                inline=True
            )
            guild = ctx.guild
            channel = guild.text_channels, name='coffee-logs'
            if channel is None:
             channel = await guild.create_text_channel('coffee-logs')
            await channel.send(
                content="Successfully added new warn.",
                embed=embed
            )
            
            return
        warn_amount = data.get("warns")
        new_warn_amount = warn_amount + 1
        data["warns"]=new_warn_amount
        data["offender_name"]=user.name
        new_warn = ({
            'warner':ctx.author.id,
            'warner_name':ctx.author.name,
            'reason':reason,
            'channel':str(ctx.channel.id),
            'datetime':dt_string
        })
        data[new_warn_amount]=new_warn
        json.dump(data, open(f"data/warns/{str(ctx.guild.id)}/{str(user.id)}.json", "a"))

        embed = discord.Embed(
            title=f"{user.name}'s new warn",
            color=random.choice(color_list)
        )
        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url,
            url=f"https://discord.com/users/{ctx.message.author.id}/"
        )
        embed.add_field(
            name=f"Warn {new_warn_amount}",
            value=f"Warner: {ctx.author.name} (<@{ctx.author.id}>)\nReason: {reason}\nChannel: <#{str(ctx.channel.id)}>\nDate and Time: {dt_string}",
            inline=True
        )
        await ctx.send(
            content="Successfully added new warn.",
            embed=embed
        )
       
    @warn_command.error
    async def warn_handler(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('{0.author.name}, you do not have the correct permissions to do so. *(commands.MissingPermissions error, action cancelled)*'.format(ctx))
            return
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                await ctx.send("{0.author.name}, you forgot to specify a user to warn. *(commands.MissingRequiredArgument error, action cancelled)*".format(ctx))
                return
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'reason':
                await ctx.send("{0.author.name}, you forgot to specify a reason. *(commands.MissingRequiredArgument error, action cancelled)*".format(ctx))
                return
        print(error)
        await ctx.send(error)

    @commands.command(
        name='warns',
        description='See all the warns a user has',
        usage='<@offender>',
        aliases=['warnings']
    )
    async def warns_command(self, ctx, user:discord.Member):
        try:
            with open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            await ctx.send(f"{ctx.author.name}, user [{user.name} ({user.id})] does not have any warns.")
            return
        warn_amount = data.get("warns")
        last_noted_name = data.get("offender_name")
        if warn_amount == 1:
            warns_word = "warn"
        else:
            warns_word = "warns"
    

        try:
            username = user.name
        except:
          
            username = last_noted_name


        embed = discord.Embed(
            title=f"{username}'s warns",
            description=f"They have {warn_amount} {warns_word}.",
            color=random.choice(color_list)
        )
        embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url,
            url=f"https://discord.com/users/{ctx.message.author.id}/"
        )
        for x in range (1,warn_amount+1):
            with open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "r") as f:
                data = json.load(f)

            warn_dict = data.get(str(x))
            warner_id = warn_dict.get('warner')
            try:
                warner_name = self.bot.get_user(id=warner_id)
            except:
                
                warner_name = warn_dict.get('warner_name')

            warn_reason = warn_dict.get('reason')
            warn_channel = warn_dict.get('channel')
            warn_datetime = warn_dict.get('datetime')

            embed.add_field(
                name=f"Warn {x}",
                value=f"Warner: {warner_name} (<@{warner_id}>)\nReason: {warn_reason}\nChannel: <#{warn_channel}>\nDate and Time: {warn_datetime}",
                inline=True
            )
        await ctx.send(
            content=None,
            embed=embed
        )
    @warns_command.error
    async def warns_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                await ctx.send("Please mention someone to verify their warns.")
                return
        await ctx.send(error)

    @commands.command(
        name='remove_warn',
        description='Removes a specific warn from a specific user.',
        usage='@user 2',
        aliases=['removewarn','clearwarn']
    )
    @has_permissions(manage_messages=True)
    async def remove_warn_command(self, ctx, user:discord.Member, *, warn:str):
        try:
            with open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "r") as f:
                data = json.load(f)
            
        except FileNotFoundError:
            
            await ctx.send(f"[{ctx.author.name}], user [{user.name} ({user.id})] does not have any warns.")
            return
        warn_amount = data.get('warns')
        specified_warn = data.get(warn)
        warn_warner = specified_warn.get('warner')
        warn_reason = specified_warn.get('reason')
        warn_channel = specified_warn.get('channel')
        warn_datetime = specified_warn.get('datetime')
        try:
            warn_warner_name = self.bot.get_user(id=warn_warner)
        except:
            
            warn_warner_name = specified_warn.get('warner_name')

        confirmation_embed = discord.Embed(
            title=f'{user.name}\'s warn number {warn}',
            description=f'Warner: {warn_warner_name}\nReason: {warn_reason}\nChannel: <#{warn_channel}>\nDate and Time: {warn_datetime}',
            color=random.choice(color_list),
        )
        confirmation_embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url,
            url=f"https://discord.com/users/{ctx.message.author.id}/"
        )
        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        await ctx.send(content='Are you sure you want to remove this warn? (Reply with y or n)', embed=confirmation_embed)
        msg = await self.bot.wait_for('message', check=check)
        reply = msg.content.lower()
        if reply in ('y', 'yes', 'confirm'):

            if warn_amount == 1: 
                os.remove("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json")
                await ctx.send(f"[{ctx.author.name}], user [{user.name} ({user.id})] has gotten their warn removed.")
                return
            if warn != warn_amount:
                for x in range(int(warn),int(warn_amount)):
                    data[str(x)] = data[str(x+1)]
                    del data[str(x+1)]
            else:
                del data[warn]
            data['warns']=warn_amount - 1
            json.dump(data,open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "w"))
            await ctx.send(f"[{ctx.author.name}], user [{user.name} ({user.id})] has gotten their warn removed.")
            return
        elif reply in ('n', 'no', 'cancel'):
            await ctx.send("Alright, action cancelled.")
            return
        else:
            await ctx.send("I have no idea what you want me to do. Action cancelled.")
    @remove_warn_command.error
    async def remove_warn_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                await ctx.send("Please mention someone to remove their warns.")
                return
            if error.param.name == 'warn':
                await ctx.send("You did not specify a warn ID to remove.")
                return
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("You specified an invalid ID.")
            return
        await ctx.send(error)

    @commands.command(
        name='edit_warn',
        description='Edits a specific warn from a specific user.',
        usage='@user 2',
        aliases=['editwarn','changewarn']
    )
    @has_permissions(manage_messages=True)
    async def edit_warn_command(self, ctx, user:discord.Member, *, warn:str):
        try:
            with open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            await ctx.send(f"[{ctx.author.name}], user [{user.name} ({user.id})] does not have any warns.")
            return


        def check(ms):
            return ms.channel == ctx.message.channel and ms.author == ctx.message.author

        await ctx.send(content='What would you like to change the warn\'s reason to?')
        msg = await self.bot.wait_for('message', check=check)
        warn_new_reason = msg.content.lower()

        specified_warn = data.get(warn)
        warn_warner = specified_warn.get('warner')
        warn_channel = specified_warn.get('channel')
        warn_datetime = specified_warn.get('datetime')
        try:
            warn_warner_name = self.bot.get_user(id=warn_warner)
        except:
            warn_warner_name = specified_warn.get('warner_name')

        confirmation_embed = discord.Embed(
            title=f'{user.name}\'s warn number {warn}',
            description=f'Warner: {warn_warner_name}\nReason: {warn_new_reason}\nChannel: <#{warn_channel}>\nDate and Time: {warn_datetime}',
            color=random.choice(color_list),
        )
        confirmation_embed.set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url,
            url=f"https://discord.com/users/{ctx.message.author.id}/"
        )

        await ctx.send(content='Are you sure you want to edit this warn like this? (Reply with y/yes or n/no)', embed=confirmation_embed)

        msg = await self.bot.wait_for('message', check=check)
        reply = msg.content.lower() 
        if reply in ('y', 'yes', 'confirm'):
            specified_warn['reason']=warn_new_reason
            json.dump(data,open("data/warns/" + str(ctx.guild.id) + "/" + str(user.id) + ".json", "w"))
            await ctx.send(f"[{ctx.author.name}], user [{user.name} ({user.id})] has gotten their warn edited.")
            return
        elif reply in ('n', 'no', 'cancel'):
            await ctx.send("Alright, action cancelled.")
            return
        else:
            await ctx.send("I have no idea what you want me to do. Action cancelled.")
    @edit_warn_command.error
    async def edit_warn_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'user':
                await ctx.send("Please mention someone to remove their warns.")
                return
            if error.param.name == 'warn':
                await ctx.send("You did not specify a warn ID to remove.")
                return
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("You specified an invalid ID.")
            return
        await ctx.send(error)



def setup(bot):
    bot.add_cog(Warn(bot))
