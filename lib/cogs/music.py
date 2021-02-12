from twitchio.ext.commands import cog,command
from bs4 import BeautifulSoup
import requests


@cog(name='music')
class music():
    def __init__(self, bot):
        self.bot = bot


    @command(aliases=['song', 'music', 'песня'])
    async def cmd_song(self, ctx, mention = ''):
        playlist_url = "https://www.last.fm/ru/user/enoootuuuk"
        song = self.get_song(self.get_html(playlist_url), playlist_url)
        full_song = f'{song["artist"]} - {song["song_name"]}'
        await ctx.channel.send(f'{self.bot.mention(mention)}Сейчас играет: {full_song}')


    def get_html(self, url):
        r = requests.get(url)
        return r.text


    def get_song(self, html, url):
        soup = BeautifulSoup(html, 'html.parser')

        try:
            artist  = soup.find('tr', class_ = 'chartlist-row--now-scrobbling').find(class_ = 'chartlist-artist').find('a').text.strip()

        except:
            artist = None

        try:
            song_name = soup.find('tr', class_ = 'chartlist-row--now-scrobbling').find(class_ = 'chartlist-name').find('a').text.strip()

        except:
            song_name = None

        song = {'artist' : artist,
                'song_name' : song_name}

        return song


    async def event_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("music")


def setup(bot):
    bot.add_cog(music(bot))