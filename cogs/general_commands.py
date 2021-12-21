import discord
from discord.ext import commands


# 일반 명령어 모음
class General(commands.Cog, name="명령"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['핑'])
    async def ping(self, ctx):
        await ctx.send(f"현재 딜레이: {self.bot.latency}초")

    @commands.command(aliases=['도움', '도움말', '명령', '명령어'])
    async def help(self, ctx):
        embed = discord.Embed(title="명령어 목록", description="명령어 목록입니다. ??뒤에 명령어를 붙여서 사용합니다. \n "
                                                          "예: ??안녕", color=0xff0000)
        embed.add_field(name='핑', value='딜레이 확인용 명령입니다.', inline=False)
        embed.add_field(name='안녕 / ㅎㅇ / 하이 / etc..', value='봇에게 인사를 건내요. 봇이 반갑게 인사를 받아줄 거에요!', inline=False)
        embed.add_field(name='큿', value='큿', inline=True)
        embed.add_field(name=':seven::two:', value='큿', inline=False)
        embed.add_field(name='화이팅', value='남코프로도 여러분도 모두 오늘도 화이팅!', inline=False)
        embed.add_field(name='접속유저 or 접속인원 or 온라인 or online', value='지금 온라인 상태인 유저들을 표시합니다.', inline=False)
        embed.add_field(name='내점수', value='현재 내 누적 점수를 확인합니다.', inline=False)
        embed.add_field(name='상품', value='상품목록을 확인합니다.', inline=True)
        embed.add_field(name='상품2', value='상품목록을 사진으로 받습니다. 확대해서 봐야하실 겁니다.', inline=False)
        embed.add_field(name='규칙', value='이벤트 규칙을 꼭 확인하세요!', inline=False)
        embed.add_field(name='퇴장', value='이벤트 도중 먼저 퇴장해야 할 때 입력해야 전산에 영향을 주지 않습니다.', inline=False)
        try:
            if ctx.author.roles[-1].name == '라운지장':
                embed.add_field(name='시작', value='이벤트 시작전에 꼭 실행해야하는 명령어 입니다.', inline=False)
                embed.add_field(name='초기화', value='이벤트를 종료하고 초기화하여 재시작할 수 있게 합니다.', inline=False)
                embed.add_field(name='정답 [현재 채널 상에서의 이름]', value='이번 문제를 맞춘사람을 기록합니다.', inline=False)
                embed.add_field(name='경고 [현재 채널 상에서의 이름]', value='대상에게 경고를 1회 부과합니다.', inline=False)
                embed.add_field(name='청소 / clear [지울 채팅의 개수]', value='채팅을 삭제합니다.', inline=False)
        except Exception:
            pass
        embed.set_footer(text="도움말")

        if ctx.author.dm_channel:
            await ctx.author.send(embed=embed)
        elif ctx.author.dm_channel is None:
            channel = await ctx.author.create_dm()
            await channel.send(embed=embed)

    @commands.command(aliases=['청소'], pass_context=True)
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount + 1)

    @commands.command(aliases=['접속인원', '접속유저', '온라인', 'online'])
    async def user(self, ctx):
        user_list = []
        idle = []
        dnd = []
        users = ctx.guild.members
        for user in users:
            if not user.bot and user.status == discord.Status.online:
                user_list.append((user.name, user.nick))
            elif not user.bot and user.status == discord.Status.idle:
                idle.append((user.name, user.nick))
            elif not user.bot and user.status == discord.Status.dnd:
                dnd.append((user.name, user.nick))

        user_list.sort()
        txt = "현재 접속중인 유저\n---------------"
        for member in user_list:
            if member[1] is None:
                txt += '\n' + str(member[0])
            else:
                txt += '\n' + str(member[0]) + ' a.k.a ' + str(member[1])
        await ctx.send(txt)
        txt = "\n\n현재 자리비움중인 유저\n------------"
        for member in idle:
            if member[1] is None:
                txt += '\n' + str(member[0])
            else:
                txt += '\n' + str(member[0]) + ' a.k.a ' + str(member[1])
        await ctx.send(txt)
        txt = "\n\n현재 다른용무중인 유저\n------------"
        for member in dnd:
            if member[1] is None:
                txt += '\n' + str(member[0])
            else:
                txt += '\n' + str(member[0]) + ' a.k.a ' + str(member[1])
        await ctx.send(txt)


def setup(bot):
    bot.add_cog(General(bot))
