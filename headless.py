import asyncio
import sys
import discord
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from requests_html import AsyncHTMLSession
import nest_asyncio # thanks baby
import time
URL_TAJ = "https://vente.tryandjudge.com/dofuskamas.php" #Removed URL for obvious reasons
nest_asyncio.apply()
class ScapperCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.render = None
        self.dispo = False
        self.notifStart = False
        self.asession: AsyncHTMLSession = None
    async def getSite(self):
        r = await self.asession.get(URL_TAJ)
        await r.html.arender()
        await self.asession.close()
        return r
    @commands.command(name="stop")
    async def stop(self,ctx):
        if self.notifStart == False:
            await ctx.send('Notification non activées')
        else:
            self.notifStart = False
            await ctx.send('Notifications stoppées')
    async def check(self):
        self.asession = AsyncHTMLSession()
        r = self.asession.run(self.getSite)
        try:
            bs : BeautifulSoup = BeautifulSoup(r[0].html.raw_html,"lxml")
            state: str = bs.find("td", text="Text you want to search for").find_next_sibling("td").find_next_sibling("td").text
            state.lower
            print(state)
            if 'complet' in state:
                self.dispo = False
            else:
                self.dispo = True
        except Exception as e:
            print("Erreur parsing, retry en cours ",e)
    @commands.command(name="start")
    async def start(self,ctx):
        t1 = time.time()
        await ctx.send('Notifications activées')
        self.notifStart = True
        while(self.notifStart):
            await self.check()
            print(self.notifStart)
            if (self.dispo):
                elapsed = time.time()-t1
                hours, rem = divmod(elapsed, 3600)
                minutes, seconds = divmod(rem, 60)
                await ctx.send("Stock disponible : "+URL_TAJ)
                self.notifStart = False
                await ctx.send("Veuillez réactiver les notifications avec !start")
                await ctx.send("Fini, temps passé: "+"{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))               
            await asyncio.sleep(30.0)

def setup(bot):
    bot.add_cog(ScapperCog(bot))


