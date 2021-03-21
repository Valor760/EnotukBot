from twitchio.ext.commands import command
from glob import glob
from ..db import db
from asyncio import sleep
from datetime import datetime
from requests import get
import json
from calendar import monthrange


class cmdHelp:
    def __init__(self, bot):
        self.bot = bot
        self.params = {'Accept' : 'application/vnd.twitchtv.v5+json',
                       'client-id': '1gkf7h1glsxebahdji24zy53r423vm'}

    COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

    # TODO: СДЕЛАТЬ!!!
    @command(name='help', aliases=['cmdhelp', "команды", "помощь", 'commands'])
    async def cmd_help(self, ctx, cmd_name = '', mention = ''):
        '''!help [название команды]'''
        # Отправляем весь список команд
        if (cmd_name == '' or cmd_name.startswith('@')) and not self.bot.check_mod(ctx):
            cmds = ["!" + key.replace('cmd_', '') for key in self.bot.commands.keys() if '_adm' not in key] + ["!" + key2 for key2 in db.column("SELECT CmdName FROM CustomCMD")]
            cmds.remove("!send_text")

            await ctx.channel.send(f"{self.bot.mention(cmd_name)}"
                                   f"Список всех комманд: {self.bot.convert_to_str(cmds)}")
            await sleep(0.5)
            await ctx.channel.send(f"Для большей информации: !help [название_команды]")

        elif ctx.author.name.lower() == 'valor760' or self.bot.check_mod(ctx):
            cmds = ["!" + key.replace('cmd_', '').replace('_adm', '') for key in self.bot.commands.keys()] + ["!" + key2 for key2 in db.column("SELECT CmdName FROM CustomCMD")]
            cmds.remove("!send_text")

            await ctx.channel.send(f"Список всех комманд: {self.bot.convert_to_str(cmds)}")
            await sleep(0.5)
            await ctx.channel.send(f"Для большей информации: !help [название_команды]")

        # Отправляем сведения о команде !help
        # Потому что не могу получить __doc__ от функции cmd_help
        elif 'help' in cmd_name.lower() or "помощь" in cmd_name.lower() or "команды" in cmd_name.lower():
            await ctx.channel.send(f"{self.bot.mention(mention)}"
                                   f"!{cmd_name.replace('!', '')} [название_команды]"
                                   f" ---- узнать больше информации о конкретной команде")

        else:
            all_cmds = [cmd for cmd in self.bot.commands.keys()] + [cmd1 for cmd1 in db.column("SELECT CmdName FROM CustomCMD")]
            if not cmd_name in all_cmds:
                await ctx.channel.send(f"{self.bot.mention(mention)}"
                                       f"\"{cmd_name if not cmd_name.startswith('!') else cmd_name[1:]}\""
                                       f" команда не найдена")

            else:
                # await ctx.channel.send(f"{('@' + mention + ' ') if not mention.startswith('@') else '' if mention == '@' else mention + ' '}"
                #                        f"{self.bot.}")
                print(self.bot.commands[cmd_name].__class__)


    @command(aliases=["live", "up", "uptime", "стрим"])
    async def cmd_live(self, ctx, mention = ''):
        if json.loads(get("https://api.twitch.tv/kraken/streams/108997445", headers=self.params).text)['stream'] != None:
            stream_start = json.loads(get("https://api.twitch.tv/kraken/streams/108997445", headers=self.params).text)['stream']['created_at']
            stream_start = str(stream_start.split('T')[1])[:-1].split(":")
            cur_time = str(datetime.utcnow()).split(' ')[-1].split('.')[0].split(':')

            mins = int(cur_time[1]) - int(stream_start[1])
            hours = int(cur_time[0]) - int(stream_start[0])

            if mins < 0:
                mins = 60 + mins
                hours -= 1

            if hours < 0:
                hours = 24 + hours

            await ctx.channel.send(f"{self.bot.mention(mention)}"
                                   f"Стрим длится {self.get_hour(hours)}"
                                   f"{self.get_min(mins)}")

        else:
            await ctx.channel.send(f"{('@' + mention + ' ') if not mention.startswith('@') and mention != '' else '' if mention == '' else mention + ' '}"
                                   f"Стрим оффлайн!")


    @command(aliases=['timeouts', 'муты'])
    async def cmd_timeouts(self, ctx):
        cur_day = int(datetime.utcnow().strftime("%d"))
        cur_month = int(datetime.utcnow().strftime("%m"))
        cur_year = int(datetime.utcnow().strftime("%Y"))

        users = db.column("SELECT Nickname FROM Timeouts WHERE Day = ? AND Month = ? AND Year = ?",
                          cur_day, cur_month, cur_year)

        if len(users) == 0:
            await ctx.channel.send(f'Сегодня еще никто не получал мут! Кто же станет первым? monkaHmm')

        else:
            await ctx.channel.send(f'Сегодня мут получали: {self.bot.convert_to_str(users)}')


    @command(aliases=['follow', 'followtime', 'фоллоу', 'followage'])
    async def cmd_followtime(self, ctx, mention = ''):
        '''Some shit'''

        if mention == '':
            mention = ctx.author.name

        else:
            mention = mention.replace('@', '')
            mention = mention.replace(',', '')

        user_id = json.loads(get(f'https://api.twitch.tv/kraken/users?login={mention}', headers = self.params).text)['users'][0]['_id']

        user_follow_time = json.loads(get(f'https://api.twitch.tv/kraken/users/{user_id}'
                                          f'/follows/channels/108997445', headers=self.params).text)

        if 'created_at' in user_follow_time:
            user_follow_time = user_follow_time['created_at']

            cur_day = int(datetime.utcnow().strftime("%d"))
            cur_month = int(datetime.utcnow().strftime("%m"))
            cur_year = int(datetime.utcnow().strftime("%Y"))
            cur_hour = int(datetime.utcnow().strftime("%H"))
            cur_min = int(datetime.utcnow().strftime("%M"))

            user_day = cur_day - int(user_follow_time.split('T')[0].split('-')[-1])
            user_month = cur_month - int(user_follow_time.split('T')[0].split('-')[1])
            user_year = cur_year - int(user_follow_time.split('T')[0].split('-')[0])
            user_hour = cur_hour - int(user_follow_time.split('T')[1].split(':')[0])
            user_min = cur_min - int(user_follow_time.split('T')[1].split(':')[1])

            if user_min < 0:
                user_min = 60 + user_min
                user_hour -= 1

            if user_hour < 0:
                user_hour = 24 + user_hour
                user_day -= 1

            if user_day < 0:
                user_day = monthrange(user_year, int(user_follow_time.split('T')[0].split('-')[1]))[-1] + user_day
                user_month -= 1

            if user_month < 0:
                user_month = 12 + user_month
                user_year -= 1


            text = f'@{mention} подписан на канал уже '
            count = 0
            for x in (self.get_year(user_year), self.get_month(user_month), self.get_day(user_day), self.get_hour(user_hour), self.get_min(user_min)):
                if count == 3:
                    break

                if x != '':
                    count += 1
                    text += x

            await ctx.channel.send(text)

        else:
            await ctx.channel.send(f'Пользователь {mention} не подписан на канал!')


    def get_year(self, year):
        if year <= 0:
            return ''

        elif year == 1:
            return f'{year} год '

        elif year == 2 or year == 3 or year == 4:
            return f'{year} года '

        else:
            return f'{year} лет '


    def get_month(self, month):
        if month <= 0:
            return ''

        elif month == 1:
            return f'{month} месяц '

        elif month == 2 or month == 3 or month == 4:
            return f'{month} месяца '

        else:
            return f'{month} месяцев '


    def get_day(self, day):
        if day <= 0:
            return ''

        elif day % 10 == 1 and day // 10 != 1:
            return f'{day} день '

        elif (day % 10 == 2 or day % 10 == 3 or day % 10 == 4) and day // 10 != 1:
            return f'{day} дня '

        else:
            return f'{day} дней '


    def get_hour(self, hour):
        if hour <= 0:
            return ''

        elif hour % 10 == 1 and hour // 10 != 1:
            return f'{hour} час '

        elif (hour % 10 == 2 or hour % 10 == 3 or hour % 10 == 4) and hour // 10 != 1:
            return f'{hour} часа '

        else:
            return f'{hour} часов '


    def get_min(self, min):
        if min <= 0:
            return ''

        elif min % 10 == 1 and min // 10 != 1:
            return f'{min} минуту '

        elif (min % 10 == 2 or min % 10 == 3 or min % 10 == 4) and min // 10 != 1:
            return f'{min} минуты '

        else:
            return f'{min} минут '

    @command(aliases=['test'])
    async def cmd_test(self, ctx, cmd_name = ''):
        qwe = await self.bot.get_chatters("enoootuuuk")
        print(qwe[3])


    async def event_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("cmdHelp")


def prepare(bot):
    bot.add_cog(cmdHelp(bot))