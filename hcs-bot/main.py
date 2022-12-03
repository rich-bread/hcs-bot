import discord
from discord.ext import commands, tasks
from module.json_module import open_json

#設定ファイルを開く
settings = open_json('appsettings.json')

#botの情報を取得
prefix = settings['prefix']
token = settings['token']

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

#botを起動
bot.run(token)