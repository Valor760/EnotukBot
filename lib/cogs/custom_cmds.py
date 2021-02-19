from twitchio.ext.commands import cog
from twitchio.ext.commands import command
from ..db import db


class customCmds():
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=["addcom", "add", "добавить", "добавитькоманду"])
    async def cmd_add(self, ctx, cmd_name, *text):
        """
        bla bla bla
        """
        if self.bot.check_mod(ctx):

            if cmd_name.startswith('!'):
                cmd_name = cmd_name[1:]

            values = db.column("SELECT CmdName FROM CustomCMD")

            if cmd_name in values:
                await ctx.channel.send(f"@{ctx.author.name} такая команда уже существует. Переименуйте новую команду или удалите старую")

            else:
                db.execute("INSERT OR IGNORE INTO CustomCMD (CmdName) VALUES (?)",
                           cmd_name)

                cmd_text = self.bot.convert_to_str(text)
                db.execute("UPDATE CustomCMD SET CmdText = ? WHERE CmdName = ?",
                           cmd_text, cmd_name)

                db.commit()
                self.bot.add_command(command(name=cmd_name)(self.__cmd_send_text__))
                await ctx.channel.send(f"@{ctx.author.name} команда успешно добавлена")


    @command(aliases=["edit", "editcom", "ред", "редактировать", "обновить"])
    async def cmd_edit(self, ctx, cmd_name, *text):
        if self.bot.check_mod(ctx):

            if cmd_name.startswith('!'):
                cmd_name = cmd_name[1:]

            if cmd_name not in db.column("SELECT CmdName FROM CustomCMD"):
                await ctx.channel.send(f"@{ctx.author.name} такой команды не существует. Список команд - !команды")

            else:
                cmd_text = self.bot.convert_to_str(text)

                db.execute("UPDATE CustomCMD SET CmdText = ? WHERE CmdName = ?",
                           cmd_text, cmd_name)

                db.commit()
                await ctx.channel.send(f"@{ctx.author.name} команда успешно обновлена")


    @command(aliases=["delete", "del", "delcom", "удалить", "удалитькомманду"])
    async def cmd_delete(self, ctx, cmd_name):
        '''
        !del <название команды>  ---  удаляет указанную команду
        '''
        if self.bot.check_mod(ctx):

            if cmd_name.startswith('!'):
                cmd_name = cmd_name[1:]

            if cmd_name not in db.column("SELECT CmdName FROM CustomCMD"):
                await ctx.channel.send(f"@{ctx.author.name} такой команды не существует. Список команд - !команды")

            else:
                db.execute("DELETE FROM CustomCMD WHERE CmdName = ?",
                           cmd_name)
                db.commit()
                await ctx.channel.send(f"@{ctx.author.name} команда успешно удалена")

    @command(aliases=db.column("SELECT cmdName FROM CustomCMD"))
    async def cmd_send_text(self, ctx, mention=None):
        await self.__cmd_send_text__(ctx, mention)


    async def __cmd_send_text__(self, ctx, mention=None):
        cmd_name = ctx.content.split(' ')[0]
        if cmd_name.startswith('!'):
            cmd_name = cmd_name[1:]

        cmd_text = db.column("SELECT CmdText FROM CustomCMD WHERE CmdName = ?",
                             cmd_name)

        if mention == None:
            await ctx.channel.send(cmd_text[0])
        else:
            await ctx.channel.send(f"@{mention.replace('@','')} {cmd_text[0]}")


    @command(aliases=['добавитькд', 'addcd', 'addcooldown'])
    async def cmd_addcd(self, ctx, cmd_name, time: int):
        if self.bot.check_mod(ctx):
            if cmd_name.replace('!', '') in db.column("SELECT cmdName FROM customCMD"):
                db.execute("UPDATE CustomCMD SET CoolDown = ? WHERE CmdName = ?",
                           time, cmd_name.replace('!', ''))
                db.commit()

                await ctx.channel.send(f"@{ctx.author.name} кд на команду '{cmd_name}' успешно установлено!")
            else:
                await ctx.channel.send(f"@{ctx.author.name} такой команды не существует! Для списка всех команд попробуйте !help")


    async def event_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("custom_cmds")


def prepare(bot):
    bot.add_cog(customCmds(bot))