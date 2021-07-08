from twitchio.ext.commands import command
# from bs4 import BeautifulSoup
import requests
from data.db.codes import lastfm_api_key


class music():
    def __init__(self, bot):
        self.bot = bot
        self.request_url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={'enoootuuuk'}&api_key={lastfm_api_key}&format=json&limit=2"

    @command(aliases=['song', 'music', 'песня', 'currentsong'])
    async def cmd_song(self, ctx, mention = ''):
        with requests.get(self.request_url, headers = {}) as response:
            songs = response.json()
            if '@attr' in songs['recenttracks']['track'][0]:
                print(songs["recenttracks"]["track"])
                await ctx.channel.send(f'{self.bot.mention(mention)}Сейчас играет: {songs["recenttracks"]["track"][0]["artist"]["#text"]}'
                                       f' - {songs["recenttracks"]["track"][0]["name"]}')
            else:
                await ctx.channel.send(f'{self.bot.mention(mention)}Сейчас не играет музыка из плейлиста Енотика!')



    @command(aliases=['last', 'lastsong', 'ls', 'последняяпесня', 'предыдущаяпесня'])
    async def cmd_lastsong(self, ctx, mention = ''):
        with requests.get(self.request_url, headers = {}) as response:
            songs = response.json()
            if '@attr' in songs['recenttracks']['track'][0]:
                await ctx.channel.send(f'{self.bot.mention(mention)}Прошлая песня: {songs["recenttracks"]["track"][1]["artist"]["#text"]}'
                                       f' - {songs["recenttracks"]["track"][1]["name"]}')
            else:
                await ctx.channel.send(f'{self.bot.mention(mention)}Прошлая песня: {songs["recenttracks"]["track"][0]["artist"]["#text"]}'
                                       f' - {songs["recenttracks"]["track"][0]["name"]}')


    # @command(aliases=['song', 'music', 'песня'])
    # async def cmd_song(self, ctx, mention = ''):
    #     playlist_url = "https://www.last.fm/ru/user/enoootuuuk"
    #     song = self.get_song(self.get_html(playlist_url), playlist_url)
    #     full_song = f'{song["artist"]} - {song["song_name"]}'
    #     await ctx.channel.send(f'{self.bot.mention(mention)}Сейчас играет: {full_song}')
    #
    #
    # def get_html(self, url):
    #     r = requests.get(url)
    #     return r.text
    #
    #
    # def get_song(self, html, url):
    #     soup = BeautifulSoup(html, 'html.parser')
    #
    #     try:
    #         artist  = soup.find('tr', class_ = 'chartlist-row--now-scrobbling').find(class_ = 'chartlist-artist').find('a').text.strip()
    #
    #     except:
    #         artist = None
    #     try:
    #         song_name = soup.find('tr', class_ = 'chartlist-row--now-scrobbling').find(class_ = 'chartlist-name').find('a').text.strip()
    #
    #     except:
    #         song_name = None
    #
    #     song = {'artist' : artist,
    #             'song_name' : song_name}
    #
    #     return song



    async def event_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("music")


def prepare(bot):
    bot.add_cog(music(bot))