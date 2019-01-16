from player import player
import asyncio
import aiohttp
from bs4 import BeautifulSoup
class scraping:
	async def getPlayer(self,name):
		hdr = {'User-Agent':'Mozilla/5.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
		async with aiohttp.get("http://www.blissscape.net/highscores/index.php",params={"player":name}, headers=hdr) as r:
			if r.status==200:
				print(name.strip()+": "+str(r.status))
				soup = BeautifulSoup(await r.text(), "lxml")
				table = soup.findAll('table')
				if table:
					rows = table[0].findAll('tr')
					del rows[0]
					total = []
					for i in rows:
						cells = i.findAll('td')
						total.append([int(cells[3].getText().replace(',','')),int(cells[2].getText().replace(',',''))])
					return player(name,total)
				else:
					return None

			