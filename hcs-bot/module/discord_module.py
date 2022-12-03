import discord

#通常
def default(title, content, color=0x0067C0):
    embed=discord.Embed(title=title,description=content, color=color)
    return embed

#完了
def success(content):
    embed=discord.Embed(description=content,color=0x2CA02C)
    embed.set_author(name='完了', icon_url='http://assets.stickpng.com/images/5aa78e207603fc558cffbf19.png')
    return embed

#エラー
def error(content):
    embed=discord.Embed(description=content,color=0xEC1A2E)
    embed.set_author(name='エラー', icon_url='https://www.freeiconspng.com/thumbs/error-icon/error-icon-4.png')
    return embed

#待機中
def waiting(content):
    embed=discord.Embed(description=content,color=0x73A1FB)
    embed.set_author(name='待機中', icon_url='https://cdn-icons-png.flaticon.com/512/248/248958.png')
    return embed

#注意
def caution(content):
    embed=discord.Embed(description=content,color=0xFF983F)
    embed.set_author(name='注意', icon_url='https://www.freeiconspng.com/thumbs/warning-icon-png/orange-warning-icon-3.png')
    return embed