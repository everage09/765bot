import gs
import re
import discord
import gspread.exceptions
from discord.ext import commands


# 이벤트 진행 전용 명령어 모음
class Event(commands.Cog, name="명령"):
    def __init__(self, bot):
        self.bot = bot
        self.sh = gs.GS()
        self.event_start = False
        self.qno = 1

    def is_guild_owner():
        def predicate(ctx):
            return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id

        return commands.check(predicate)

    @commands.command(aliases=['join'])
    async def 출근(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("먼저 음성채널에 들어가셔야 합니다.")

    @commands.command(aliases=['leave', 'quit'])
    async def 퇴근(self, ctx):
        try:
            await self.bot.voice_clients[0].disconnect()
        except Exception as e:
            await ctx.send("명령 처리 도중 뭔가 잘못됬습니다. 다시 시도해주세요.")

    @commands.command()
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), is_guild_owner(), commands.has_role(843864275792560198))
    async def 시작(self, ctx):
        try:
            self.event_start = True
            await ctx.send("지금부터 이벤트를 시작합니다. \n 1번 문제부터 시작합니다.")
            await ctx.send("잠깐 주목해주세요.")
        except commands.NoPrivateMessage:
            await ctx.send("DM으로는 실행할 수 없는 메세지입니다.")

    @commands.command()
    @commands.guild_only()
    @commands.check_any(commands.is_owner(), is_guild_owner(), commands.has_role(843864275792560198))
    async def 초기화(self, ctx):
        try:
            self.event_start = False
            self.qno = 1
            worksheet = self.sh.worksheet("참가자_포인트")
            values = worksheet.get('B3:B36')
            for value in values:
                if value[0].find('불참') == -1:
                    value[0] = '0'
            worksheet.update("B3:B36", values)
            await ctx.send("이벤트를 종료하고 초기상태로 돌립니다.")
        except commands.NoPrivateMessage:
            await ctx.send("DM으로는 실행할 수 없는 메세지입니다.")

    @commands.command(pass_context=True,aliases=['wjdekq'])
    @commands.check_any(commands.is_owner(), is_guild_owner(), commands.has_role(843864275792560198))
    async def 정답(self, ctx, name):
        try:
            if self.event_start:
                worksheet = self.sh.worksheet("문제로그")
                worksheet.update_cell(self.qno+1, 5, name)

                if name == "모두":
                    await ctx.send(f"{name}가 {self.qno}번 문제를 맞추는 데 성공하고 포인트를 획득합니다.")
                else:
                    await ctx.send(f"{name}님이 {self.qno}번문제를 맞추고 포인트를 획득합니다.")
                self.qno += 1

                worksheet2 = self.sh.worksheet("참가자_포인트")
                values = worksheet2.get('B3:B36')
                check = re.compile('[0-9]*,*[가-힣]+')
                for value in values:
                    if check.match(value[0]) is None:
                        value[0] = str(int(value[0]) + 1)
                worksheet2.update("B3:B36", values)

            else:
                await ctx.send("먼저 ??시작 명령어로 이벤트 시작을 선언해주세요.")
        except :
            pass

    @commands.command()
    async def 퇴장(self,ctx):
        worksheet = self.sh.worksheet("참가자_포인트")
        name = ctx.author.name
        nick = ctx.author.nick
        try:
            cell = worksheet.find(name)
        except gspread.exceptions.CellNotFound:
            cell = worksheet.find(nick)

        try:
            val = str(worksheet.cell(cell.row,2).value)
            if val.find('중도퇴장') == -1:
                val += ',중도퇴장'
                worksheet.update_cell(cell.row, 2, val)
                await ctx.send("퇴장 처리 되었습니다.")
            else:
                await ctx.send("이미 퇴장 처리 된 상태입니다.")
        except gspread.exceptions.GSpreadException:
            print('not found')

    @commands.command(aliases=['score','sowjatn'])
    async def 내점수(self, ctx):
        try:
            name = ctx.author.name
            nick = ctx.author.nick
            worksheet = self.sh.worksheet("참가자_포인트")
            try:
                cell = worksheet.find(name)
            except gspread.exceptions.CellNotFound:
                cell = worksheet.find(nick)

            score = worksheet.cell(cell.row,12).value
            if ctx.author.dm_channel:
                await ctx.author.send(f"현재 {name}님의 점수는 {score}점 입니다.")
            elif ctx.author.dm_channel is None:
                channel = await ctx.author.create_dm()
                await channel.send(f"현재 {name}님의 점수는 {score}점 입니다.")
        except:
            pass

    @commands.command(aliases=['rule','RULE','Rule','rbclr'])
    async def 규칙(self, ctx):
        await ctx.send("규칙은 규칙 채널에 공지된 글을 확인해주세요!")

    @commands.command()
    async def 상품2(self, ctx):
        try:
            file1 = discord.File("/Users/X5967T/PycharmProjects/765bot/prize1.png")
            file2 = discord.File("/Users/X5967T/PycharmProjects/765bot/prize2.png")
            file3 = discord.File("/Users/X5967T/PycharmProjects/765bot/prize3.png")
            if ctx.author.dm_channel:
                await ctx.author.send(file=file1)
                await ctx.author.send(file=file2)
                await ctx.author.send(file=file3)
            elif ctx.author.dm_channel is None:
                channel = await ctx.author.create_dm()
                await channel.send(file=file1)
                await channel.send(file=file2)
                await channel.send(file=file3)
        except Exception as e:
            print(e)
            print("something went wrong")

    @commands.command(aliases=['prize','tkdvna'])
    async def 상품(self, ctx):
        try:
            worksheet = self.sh.worksheet("상품")
            prize_list = worksheet.get('A2:C136')
            n = 0
            l = 1
            embed = discord.Embed(title=f":gift:상품목록{l}", description="상품목록입니다.", color=0xff0000)
            for i in range(len(prize_list)):
                embed.add_field(name=prize_list[i][0], value='{}, 개수: {}'.format(prize_list[i][1], prize_list[i][2]),
                                inline=True)
                n += 1
                if n % 25 == 0:
                    if ctx.author.dm_channel:
                        await ctx.author.send(embed=embed)
                        l += 1
                        embed = discord.Embed(title=f":gift:상품목록{l}", description="상품목록입니다.", color=0xff0000)
                    elif ctx.author.dm_channel is None:
                        channel = await ctx.author.create_dm()
                        await channel.send(embed=embed)
                        l += 1
                        embed = discord.Embed(title=f":gift:상품목록{l}", description="상품목록입니다.", color=0xff0000)
            await ctx.author.send(embed=embed)
        except Exception as e:
            print(e)
            print("something went wrong")

    @commands.command(pass_context=True,aliases=['warn','rudrh'])
    @commands.check_any(commands.is_owner(), is_guild_owner(), commands.has_role(843864275792560198))
    async def 경고(self, ctx, member: discord.Member = None):
        def check_name(mem):
            if mem in ctx.guild.members:
                return True
            else:
                return False
        try:
            if check_name(member):
                worksheet = self.sh.worksheet("참가자_포인트")
                try:
                    cell = worksheet.find(member.name)
                except gspread.exceptions.CellNotFound:
                    cell = worksheet.find(member.nick)
                warn = int(worksheet.cell(cell.row,8).value)
                warn += 1
                worksheet.update_cell(cell.row,8,warn)

                if warn == 1:
                    worksheet.update_cell(cell.row,9,10)
                    await ctx.send(f"{member.name}님의 점수를 10점 감점했습니다.\n"
                                                      "추가 경고시 누적 점수의 10%가 차감됩니다.")
                elif warn == 2:
                    minus_score = float(worksheet.cell(cell.row,9).value)
                    minus_score += float(worksheet.cell(cell.row,11).value) * 0.1
                    worksheet.update_cell(cell.row, 9, minus_score)
                    await ctx.send(f"{member.name}님의 점수를 10% 차감했습니다.\n"
                                                      "추가 경고시 점수가 몰수되고 이벤트채널에서 일시적으로 퇴장됩니다.")
                if warn >= 3:
                    minus_score = float(worksheet.cell(cell.row, 9).value)
                    minus_score += float(worksheet.cell(cell.row, 11).value)
                    worksheet.update_cell(cell.row, 9, minus_score)
                    print("out")
                    await member.edit(voice_channel=None)
                    await member.remove_roles(discord.utils.get(ctx.guild.roles, name="킹반인"))
                    await member.add_roles(discord.utils.get(ctx.guild.roles, name="일시적강퇴"))

                    await ctx.send(f"{member.name}님을 이벤트페이지에서 일시적 추방했습니다.")
            else:
                await ctx.send("이름을 정확히 입력해주세요.")
        except gspread.exceptions.GSpreadException:
            await ctx.send("적합한 데이터를 찾지 못하였습니다.")
        except Exception as e:
            print(e)
            await ctx.send("실행 도중 오류가 발생했습니다. 명령어를 제대로 입력했는지 확인해주세요.")

    @commands.command()
    @commands.check_any(commands.is_owner(), is_guild_owner(),commands.has_role(843864275792560198))
    async def yee(self,ctx):
        await ctx.send('Hello mister owner!')


def setup(bot):
    bot.add_cog(Event(bot))


