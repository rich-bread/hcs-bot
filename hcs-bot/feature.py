import asyncio
import discord
from discord.ext import commands
import module.discord_module as dismod
import database

class icon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #アイコン提出コマンド
    @commands.command(name='upload')
    async def upload_command(self, ctx):
        try:
            author = ctx.author #コマンド実行者

            role = get_role(ctx, "bot使用権") #対象ロール
            frontdesk = await icon.create_frontdesk(self, ctx, role, author) #受付チャンネルを作成

            await frontdesk.send(f"<@{author.id}>") #コマンド実行者にメンション
            await icon.upload_checker(self, ctx, frontdesk, author) #アイコン提出関数

        except Exception as e:
            print(e)

        finally:
            await frontdesk.send(embed=dismod.default("終了", "10秒後にこのチャンネルは削除されます"))
            await asyncio.sleep(10)
            await author.remove_roles(role) #コマンド実行者からロールを外す
            await frontdesk.delete() #作成した受付チャンネルを削除

    @commands.command(name='uploadtest')
    async def upload_test(self, ctx):
        role = get_role(ctx, "bot使用権")
        channel = await icon.create_frontdesk(self, ctx, role, ctx.author)

    #受付チャンネルの作成
    async def create_frontdesk(self, ctx, role, author):
        channelName = "受付" #チャンネル名
        categoryName = "🥫はじめにご覧ください" #カテゴリ名

        channel = await ctx.guild.create_text_channel(channelName) #チャンネルを作成
        category = discord.utils.get(ctx.guild.channels, name=categoryName) #カテゴリを取得
        await channel.edit(category=category) #作成したチャンネルを指定カテゴリに移動

        await channel.set_permissions(ctx.guild.default_role, read_messages=True, send_messages=False) #デフォルトユーザーの権限設定
        await channel.set_permissions(role, read_messages=True, send_messages=True) #ロール付与者の権限設定
    
        await author.add_roles(role) #authorにロール付与

        return channel

    #アイコン提出機能
    async def upload_checker(self, ctx, channel, author):
        try:
            #ユーザから送信されたメッセージに画像が添付されているかの確認
            message = ctx.message #メッセージ
            attachments = message.attachments #添付ファイルリスト
            #添付ファイルリストが0の場合、コマンドをはじく
            if len(attachments) == 0:
                await channel.send(embed=dismod.error("画像が添付されていません。画像を添付したうえで再度コマンドの実行をお願いします"))
                return

            #コマンド実行者のTwitterIDの入力
            title1 = "実行者のTwitterID"
            content1 = "このコマンドを実行しているユーザのTwitterIDを入力してください"
            authorid = await icon.await_message(self, channel, author, title1, content1)
            if authorid == None: return

            #待機メッセージ
            await channel.send(embed=dismod.waiting("有効なTwitterIDであるか確認中"))

            #コマンド実行者のTwitterID登録確認
            author_result = (await database.post_db('user_check', [authorid])).json()
            if author_result[0] != True:
                await channel.send(embed=dismod.error("正しいTwitterIDを入力してください"))
                return

            #コマンド実行者が所属するチームのリーダーのTwitterID入力
            title2 = "チームリーダーのTwitterID"
            content2 = "このコマンドを実行しているユーザが所属するチームのリーダーのTwitterIDを入力してください"
            leaderid = await icon.await_message(self, channel, author, title2, content2)
            if leaderid == None: return

            #待機メッセージ
            await channel.send(embed=dismod.waiting("有効なTwitterIDであるか確認中"))

            #チームリーダーのTwitterID登録確認
            leader_result = (await database.post_db('user_check', [authorid])).json()
            if leader_result[0] != True:
                await channel.send(embed=dismod.error("正しいTwitterIDを入力してください"))
                return

            #待機メッセージ
            await channel.send(embed=dismod.waiting("コマンド実行者が指定リーダーのチームに所属しているか確認中"))

            #コマンド実行者が指定リーダーのチームに所属しているか確認
            idList = [authorid, leaderid]
            team_result = (await database.post_db('team_check', idList)).json()
            if team_result[0] != True:
                await channel.send(embed=dismod.error("指定したリーダーのチームに所属していません"))
                return

            #アイコン提出ログ記入
            iconUrl = attachments[0].url
            iconData = [authorid, iconUrl]
            await database.post_db('icon_upload', iconData)
            icon_channel = get_channel(ctx, "アイコン")
            await icon_channel.send(f"<@{author.id}>のアイコン↓")
            await icon_channel.send(attachments[0].url)

            #ロール付与
            roleInfo = (await database.get_db('hcsGiveRole', authorid, leaderid)).json()
            roleNameList = []
            roleNameList.append(roleInfo["大会ロール"])
            if roleInfo["リーダーロール"] == "あり":
                roleNameList.append("チームリーダー")
            if roleInfo["ナンバリングロール"] != "":
                roleNameList.append("Team"+str(roleInfo["ナンバリングロール"]))
            else:
                admin_channel = get_channel(ctx, "運営ログ")
                await admin_channel.send(embed=dismod.error(f"<@{author.id}>さんにチームナンバリングロールが付与できませんでした。手動での追加をお願いします"))

            for roleName in roleNameList:
                role = get_role(ctx, roleName)
                await author.add_roles(role)

            log_channel = get_channel(ctx, "完了通知")
            await log_channel.send(embed=dismod.success(f"<@{author.id}>さんにロールを付与しました"))

        except Exception as e:
            print(e)
            await channel.send(embed=dismod.error("予期せぬエラーが発生しました。このメッセージが送信された場合は運営までご連絡ください"))

        else:
            return

    #ユーザからのメッセージを確認する関数
    async def check_message(self, channel, author):
        def check(m: discord.Message):
            return m.channel == channel and m.author.id == author.id
        try:
            message = await self.bot.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeouError:
            error = await channel.send(embed=dismod.error("待機時間内にメッセージが確認できませんでした"))
            return None
        else:
            return message.content

    #ユーザからのメッセージを待機する関数
    async def await_message(self, channel, author, title, content):
        bot_msg = await channel.send(embed=dismod.default(title, content))
        user_msg = await icon.check_message(self, channel, author)
        return user_msg

#特定ロールの取得
def get_role(ctx, name):
    role = discord.utils.get(ctx.guild.roles, name=name)
    return role

#特定チャンネルの取得
def get_channel(ctx, name):
    channel = discord.utils.get(ctx.guild.channels, name=name)
    return channel

def setup(bot):
    return bot.add_cog(icon(bot))
