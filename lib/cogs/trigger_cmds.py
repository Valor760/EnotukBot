from twitchio.ext.commands import cog, command
from ..db import db


@cog(name='triggerCmds')
class triggerCmds():
    def __init__(self, bot):
        self.bot = bot


    @command(aliases=['addtrigger', 'добавитьтриггер'])
    async def cmd_addtrigger(self, ctx, trigger_word, *trigger_text):
        if self.bot.check_mod(ctx):

            self.bot.trigger_words.append(trigger_word)
            trigger_text = self.bot.convert_to_str(trigger_text)

            db.execute("INSERT OR IGNORE INTO Triggers (TriggerWord) VALUES (?)",
                       trigger_word)
            db.execute("UPDATE Triggers SET TriggerText = ? WHERE TriggerWord = ?",
                       trigger_text, trigger_word)
            db.commit()

            await ctx.channel.send(f'@{ctx.author.name} триггер на слово " {trigger_word} " успешно добавлен!')


    @command(aliases=['deltrigger', 'удалитьтриггер'])
    async def cmd_deltrigger(self, ctx, trigger_word):
        if self.bot.check_mod(ctx):

            if trigger_word in db.column("SELECT TriggerWord FROM Triggers"):

                db.execute("DELETE FROM Triggers WHERE TriggerWord = ?",
                           trigger_word)
                db.commit()

                self.bot.trigger_words.remove(trigger_word)

                await ctx.channel.send(f'@{ctx.author.name} триггер на слово " {trigger_word} " успешно удален!')

            else:
                ctx.channel.send(f'@{ctx.author.name} триггера на слово " {trigger_word} " не существует!'
                                 f' Для списка всех триггеров - !alltrigger')


    @command(aliases=['edittrigger', 'обновитьтриггер'])
    async def cmd_edittrigger(self, ctx, trigger_word, *new_text):
        if self.bot.check_mod(ctx):

            if trigger_word in db.column("SELECT TriggerWord FROM Triggers"):

                new_text = self.bot.convert_to_str(new_text)
                db.execute("UPDATE Triggers SET TriggerText = ? WHERE TriggerWord = ?",
                           new_text, trigger_word)
                db.commit()

            else:
                ctx.channel.send(f'@{ctx.author.name} триггера на слово " {trigger_word} " не существует!'
                                 f' Для списка всех триггеров - !alltrigger')


    @command(aliases=['alltrigger', 'всетриггеры'])
    async def cmd_alltrigger(self, ctx):
        await ctx.channel.send(f"Бот триггерится на слова: {self.bot.convert_to_str(self.bot.trigger_words)}")


    async def event_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("trigger_cmds")


def setup(bot):
    bot.add_cog(triggerCmds(bot))