import os
import discord
from discord.ext import commands, tasks
from module.json_module import open_json
from server import keep_alive

#設定ファイルを開く
settings = open_json('appsettings.json')

#botの情報を取得
prefix = settings['prefix']
token = os.getenv('DISCORDBOT_TOKEN')

#インテント有効化
intents = discord.Intents.all()

#botを作成
bot = commands.Bot(intents=intents, command_prefix=prefix)

#起動時処理
@bot.event
async def on_ready():
    print("Ready.")

#Extensionを付与
bot.load_extension("feature")

#ウェブサーバーを起動
keep_alive()

#botを起動
bot.run(token)