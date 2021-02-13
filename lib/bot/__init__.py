from twitchio.ext.commands import Bot as TwitchBotBase
from glob import glob
from data.db.codes import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncio import sleep
from lib.db import db
from datetime import datetime
import platform
from random import randint
from copy import deepcopy


if platform.system() == 'Windows':
    COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

elif platform.system() == 'Linux':
    COGS = [path.split("/")[-1][:-3] for path in glob("./lib/cogs/*.py")]

IGNORE_EXCEPTIONS = []


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)


    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"> {cog} cog ready")


    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(TwitchBotBase):
    def __init__(self):
        self.Prefix = BOT_PREFIX
        self.cogs_ready = Ready()
        self.scheduler = AsyncIOScheduler()
        self.ready = False

        self.msg_count = 0
        self.msg_position = randint(0, len(db.column("SELECT CmdText FROM SchedCMDS")) - 1)
        self.can_process = True

        self.trigger_words = db.column("SELECT TriggerWord FROM Triggers")
        self.words_on_cooldown = []

        db.autosave(self.scheduler)

        super().__init__(
            irc_token = TMI_TOKEN,
            client_id = CLIENT_ID,
            nick = BOT_NICK,
            prefix = BOT_PREFIX,
            initial_channels = CHANNEL
        )


    def update_db(self):
        db.commit()


    def setup(self):
        for cog in COGS:
            self.load_module(f"lib.cogs.{cog}")
            print(f"--- {cog} cog is loaded")


    def run(self):
        print("RUNNING SETUP.....")
        self.setup()

        print("RUNNING BOT.....")
        super().run()


    # async def event_command_error(self, ctx, error):
    #     if any([isinstance(error, exc) for exc in IGNORE_EXCEPTIONS]):
    #         pass
    #     else:
    #         # await ctx.channel.send("Произошла ошибка!")
    #         pass


    async def event_ready(self):
        if not self.ready:

            self.update_db()

            self.scheduler.start()

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print(">>Bot Ready<<")


    async def event_message(self, message):
        if message.author.name.lower() == BOT_NICK.lower():
            return
        print(f"({message.channel})[{message.author.name}]:   {message.content}")


        if 'custom-reward-id' in message.tags:

            if message.tags['custom-reward-id'] == '94d550f4-aa87-4684-9b0d-09a65857eca9':
                await self.points_timeout(message)

            elif message.tags['custom-reward-id'] == 'd6dd0097-ab41-4fbf-bc19-16591dd72682':
                await self.points_timeout_self(message)

        if not message.content.startswith('!'):
            await self.trigger_message(message)

        await bot.handle_commands(message)

        self.msg_count += 1
        await self.send_periodic_msg(message)


    def check_mod(self, ctx):
        if ctx.author.is_mod or ctx.author.name.lower() == 'valor760':
            return True
        else:
            return False


    # Превращаем список слов в строку
    def convert_to_str(self, list, separator=' '):
        return separator.join(list)


    # Отправляем нужное упоминание в чат, в зависимости было оно или нет
    def mention(self, user_mention):
        if user_mention == '':
            return ''
        elif user_mention.startswith('@'):
            return f"{user_mention} "
        else:
            return '@' + user_mention + ' '


    # Отправка переодических сообщений из базы данных
    # TODO: сделать так, чтобы функция работала из файла sched_cmds.py
    async def send_periodic_msg(self, ctx):
        if self.msg_count > 10 and self.can_process:
            if self.msg_position >= len(db.column("SELECT CmdText FROM SchedCMDS")):
                self.msg_position = 0

            await ctx.channel.send(db.column("SELECT CmdText FROM SchedCMDS")[self.msg_position])

            self.msg_position += 1
            self.msg_count = 0

            self.can_process = False
            await self.sleep_check()


    async def sleep_check(self):
        await sleep(300)
        self.can_process = True


    # Таймаут на 10 минут за поинты выбранного человека
    async def points_timeout(self, ctx):
        user_on_timeout = ctx.content.split(' ')[0].lower()
        user_on_timeout = user_on_timeout.replace(',', '')

        if user_on_timeout.startswith('@'):
            user_on_timeout = user_on_timeout[1:]

        user_role = await self.check_on_user_role(user_on_timeout)

        if user_role == 'mods':
            await ctx.channel.send(f"@{ctx.author.name} вы не можете замутить модератора!")

        elif user_role == 'vips':
            await ctx.channel.send(f"@{ctx.author.name} вы не можете замутить ВИПа!")

        elif user_role == 'streamer':
            await ctx.channel.send(f"@{ctx.author.name} вы не можете замутить стримера!")

        else:
            cur_day = int(datetime.utcnow().strftime("%d"))
            cur_month = int(datetime.utcnow().strftime("%m"))
            cur_year = int(datetime.utcnow().strftime("%Y"))

            if user_on_timeout not in db.column("SELECT Nickname FROM Timeouts"):
                db.execute("INSERT INTO Timeouts (Nickname) VALUES (?)",
                           user_on_timeout)
                db.execute("UPDATE Timeouts SET Day = ?, Month = ?, Year = ? WHERE Nickname = ?",
                           cur_day, cur_month, cur_year, user_on_timeout)
                db.commit()

                await ctx.channel.timeout(user_on_timeout)
                await sleep(0.5)
                await ctx.channel.send(f"{user_on_timeout} получил мут на 10 минут! Кто следующий?")


            else:
                db_day = int(db.column("SELECT Day FROM Timeouts WHERE Nickname = ?",
                                    user_on_timeout)[0])
                db_month = int(db.column("SELECT Month FROM Timeouts WHERE Nickname = ?",
                                    user_on_timeout)[0])
                db_year = int(db.column("SELECT Year FROM Timeouts WHERE Nickname = ?",
                                    user_on_timeout)[0])

                if cur_day > db_day or cur_month > db_month or cur_year > db_year:
                    db.execute("UPDATE Timeouts SET Day = ?, Month = ?, Year = ? WHERE Nickname = ?",
                               cur_day, cur_month, cur_year, user_on_timeout)
                    db.commit()

                    await ctx.channel.timeout(user_on_timeout)
                    await sleep(0.5)
                    await ctx.channel.send(f"{user_on_timeout} получил мут на 10 минут! Кто следующий?")

                else:
                    await ctx.channel.send(f"@{ctx.author.name} пользователь {user_on_timeout} не может быть замьючен, "
                                           f"потому что получал уже получал мут за последние 24 часа")


    async def check_on_user_role(self, user_on_timeout):
        chatters = await bot.get_chatters('enoootuuuk')
        mods = chatters[4]
        vips = chatters[3]

        if user_on_timeout.startswith('@'):
            user_on_timeout = user_on_timeout[1:]

        if user_on_timeout.lower() in mods:
            return 'mods'

        elif user_on_timeout.lower() in vips:
            return 'vips'

        elif user_on_timeout.lower() == 'enoootuuuk':
            return "streamer"


    async def points_timeout_self(self, ctx):
        await ctx.channel.timeout(ctx.author.name)


    async def trigger_message(self, ctx):
        for word in self.trigger_words:
            if word in ctx.content and word not in self.words_on_cooldown:
                text = db.column("SELECT TriggerText FROM Triggers WHERE TriggerWord = ?",
                                 word)
                await ctx.channel.send(self.convert_to_str(text))
                await self.word_cooldown(word)
                return


    async def word_cooldown(self, word):
        self.words_on_cooldown.append(word)
        await sleep(30)
        self.words_on_cooldown.remove(word)



bot = Bot()