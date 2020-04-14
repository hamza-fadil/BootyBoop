import asyncio
import discord
from discord.ext import commands, tasks
import time
from selenium import webdriver
URL_TAJ = "REDACTED"
class ScapperCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.dispo = False
        self.notifStart = False
        self.found = False
        self.driver = webdriver.PhantomJS()
        self.t1 = None
    async def getSite(self):
        self.driver.get(URL_TAJ)
        await asyncio.sleep(3.0)
        prices = self.driver.find_element_by_id(id_='REDACTED')
        text = prices.text
        return text
    @commands.command(name="stop")
    async def stop(self,ctx):
        self.check.stop()
        await ctx.send('Notification stoppée')
    @tasks.loop(seconds=5.0)
    async def check(self):
        r = await self.getSite()
        try:
            start = r.find("REDACTED")
            end = r.find("REDACTED") + 40
            split = r[start:end]
            if 'complet' not in split:
                self.found = True
                elapsed = time.time() - self.t1
                hours, rem = divmod(elapsed, 3600)
                minutes, seconds = divmod(rem, 60)
                await self.start_ctx.send("Stock disponible : "+URL_TAJ)
                await self.start_ctx.send("Veuillez réactiver les notifications avec !start")
                await self.start_ctx.send("Fini, temps passé: "+"{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
        except Exception as e:
            await self.start_ctx.send("Erreur, retry en cours : ",e)
        if self.found == True: 
            self.check.stop()
    
    @commands.command(name="start")
    async def start(self,ctx):
        self.found = False
        self.t1 = time.time()
        await ctx.send("Notifications activées")
        self.start_ctx = ctx
        self.check.start()
def setup(bot):
    bot.add_cog(ScapperCog(bot))


