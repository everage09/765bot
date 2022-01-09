import asyncio
import discord
from discord.ext import commands
import nacl  # 음성 채널 연결에 필요한 모듈
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='??',
                   status=discord.Status.online,
                   activity=discord.Game("'??help'로 명령어 확인"),
                   help_command=None,
                   intents=intents)

token = "Your Token"

for file in os.listdir("../cogs"):
    if file.endswith(".py"):
        if not file.startswith("event_manage"):
            bot.load_extension(f"cogs.{file[:-3]}")
            print(f"cogs.{file[:-3]}로드 완료.")


@bot.event
async def on_ready():
    print("================")
    print("다음으로 로그인합니다")
    print(bot.user.name)
    print(bot.user.id)
    print("================")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("명령어를 제대로 입력했는지 확인해주세요. ??help 로 명령어를 확인할 수 있습니다.")
    elif isinstance(error, (commands.CheckAnyFailure,commands.MissingPermissions,commands.MissingAnyRole)):
        await ctx.send("명령을 실행할 권한이 없습니다.")


@bot.command()
async def load(ctx, extension):
    try:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(f":white_check_mark: {extension}을 로드했습니다.")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send("이미 로드되어있습니다.")


@bot.command()
async def unload(ctx, extension):
    try:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f":white_check_mark: {extension}을 언로드했습니다.")
    except commands.ExtensionNotLoaded:
        await ctx.send("이미 언로드되어있거나 로드되어있지 않습니다.")


@bot.command()
async def reload(ctx, extension=None):
    if extension is None:
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                try:
                    bot.unload_extension(f"cogs.{file[:-3]}")
                except commands.ExtensionNotLoaded:
                    pass
                bot.load_extension(f"cogs.{file[:-3]}")
                await ctx.send(f":white_check_mark: {file[:-3]}을 리로드했습니다.")
        await ctx.send(f":white_check_mark: 모든 명령어를 리로드했습니다.")
    else:
        try:
            bot.unload_extension(f"cogs.{extension}")
        except commands.ExtensionNotLoaded:
            pass
        bot.load_extension(f"cogs.{extension}")
        await ctx.send(f":white_check_mark: {extension}을 리로드했습니다.")

bot.run(token)
