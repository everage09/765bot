from discord.ext import commands


class trivia(commands.Cog, name="명령"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['hello', 'hi', 'ㅎㅇ', '안녕하세요', '하위'])
    async def 안녕(self, ctx):
        await ctx.send(ctx.author.mention + "P 안녕하세요!")

    @commands.command()
    async def 화이팅(self, ctx):
        await ctx.send("765프로 화이팅!")

    @commands.command(aliases=['멍청이', 'babo'])
    async def 바보(self, ctx):
        await ctx.send("방금 뭐라고 했냐")

    @commands.command(aliases=['큿'], name='72')
    async def name(self, ctx):
        await ctx.send("큿-")

    @commands.command(name='?')
    async def what1(self, ctx):
        await ctx.send("?")

    @commands.command(name='??')
    async def what2(self, ctx):
        await ctx.send("??")

    @commands.command(name='!')
    async def what3(self, ctx):
        await ctx.send("?!")

    @commands.command(aliases=['tf36'])
    async def 테프(self,ctx):
        await ctx.send("항상 고생하시는 우리의 라운지 장님. 터틀 포에버-")

    @commands.command(aliases=['evrage','Everage','Evan','evan'])
    async def 에반(self,ctx):
        await ctx.send("에반 (17세(17진법), 솔로, (들을)교양 없는 남자, 착한 사람, 리겜 응애뉴비)")

    @commands.command(aliases=['엥'],name='엥?')
    async def 엥(self, ctx):
        await ctx.send("엥?\nㄴ엥?\n  ㄴ엥?\n   ㄴ엥?")

    @commands.command(aliases=['961','315','876'])
    async def 그회사(self, ctx):
        await ctx.send("어허 전 765봇이에요!")

    @commands.command()
    async def 야(self, ctx):
        await ctx.send("왜")

    @commands.command(aliases=['newbie'])
    async def 뉴비(self, ctx):
        await ctx.send("에반")

    @commands.command(aliases=['gosu'])
    async def 고수(self, ctx):
        await ctx.send("호시쿠즈, 카호, 진영공주님. ㅇㄱㄹㅇㅂㅂㅂㄱ 반박시 대머리")

    @commands.command(aliases=[])
    async def 갓겜(self, ctx):
        await ctx.send("그것은 밀리시타를 말하는 것이로군요.")

    @commands.command(aliases=['호!','ho','Ho'])
    async def 호(self, ctx):
        await ctx.send("하이호-")

    @commands.command(aliases=['후우카','fuka','Fuka'])
    async def 후카(self, ctx):
        await ctx.send("지상최고의 정통파 아이돌")

    @commands.command(aliases=['19'])
    async def 이쿠(self, ctx):
        await ctx.send("호라네!")


def setup(bot):
    bot.add_cog(trivia(bot))