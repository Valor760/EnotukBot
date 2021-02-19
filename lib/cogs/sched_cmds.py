from twitchio.ext.commands import cog, command
from lib.db import db
from asyncio import sleep



class cmdSchedule():
    def __init__(self, bot):
        self.bot = bot


    @command(aliases=["addperiod", "добавитьпериод"])
    async def cmd_addperiod(self, ctx, *text):
        if self.bot.check_mod(ctx):
            cmd_text = self.bot.convert_to_str(text)
            db.execute("INSERT OR IGNORE INTO SchedCMDS (CmdText) VALUES (?)",
                       cmd_text)
            db.commit()

            await ctx.channel.send(f"@{ctx.author.name} периодическая команда успешко добавлена!")


    @command(aliases=["delperiod", "удалитьпериод"])
    async def cmd_delperiod(self, ctx, cmd_num: int):
        if self.bot.check_mod(ctx):
            if cmd_num <= len(db.column("SELECT CmdText FROM SchedCMDS")) and cmd_num > 0 :
                db.execute("DELETE FROM SchedCMDS WHERE CmdText = ?",
                           db.column("SELECT CmdText FROM SchedCMDS")[cmd_num - 1])
                db.commit()

                await ctx.channel.send(f"@{ctx.author.name} периодическая команда №{cmd_num} успешно удалена!")

            else:
                await ctx.channel.send(f"@{ctx.author.name} переодическая команда №{cmd_num} не найдена!"
                                       f" Для списка всех периодических команд воспользуйтесь !allperiod")


    @command(aliases=["allperiod", "всепериод"])
    async def cmd_allperiod(self, ctx):
        for x in db.column("SELECT CmdText FROM SchedCMDS"):
            await ctx.channel.send(f"Команда {(db.column('SELECT CmdText FROM SchedCMDS').index(x) + 1)} == {x}")
            await sleep(0.5)


    @command(aliases=["editperiod", "изменитьпериод"])
    async def cmd_editperiod(self, ctx, cmd_num: int, new_text):
        if self.bot.check_mod(ctx):
            if cmd_num <= len(db.column("SELECT CmdText FROM SchedCMDS")) and cmd_num > 0 :
                db.execute("UPDATE SchedCMDS SET CmdText = ? WHERE CmdText = ?",
                           new_text, db.column("SELECT CmdText FROM SchedCMDS")[cmd_num - 1])
                db.commit()

                await ctx.channel.send(f"@{ctx.author.name} периодическая команда №{cmd_num} успешно обновлена!")

            else:
                await ctx.channel.send(f"@{ctx.author.name} переодическая команда №{cmd_num} не найдена!"
                                       f" Для списка всех периодических команд воспользуйтесь !allperiod")


    async def event_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("sched_cmds")


def prepare(bot):
    bot.add_cog(cmdSchedule(bot))