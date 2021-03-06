

from ScrapePlugins.JzLoader.jzFeedLoader import JzFeedLoader
from ScrapePlugins.JzLoader.jzContentLoader import JzContentLoader

import ScrapePlugins.RunBase

import time

import runStatus


class Runner(ScrapePlugins.RunBase.ScraperBase):
	loggerPath = "Main.Jz.Run"

	pluginName = "JzLoader"


	def _go(self):

		self.log.info("Checking Jz feeds for updates")
		fl = JzFeedLoader()
		fl.go()
		fl.closeDB()

		time.sleep(3)
		#print "wat", cl

		if not runStatus.run:
			return

		cl = JzContentLoader()

		if not runStatus.run:
			return

		todo = cl.retreiveTodoLinksFromDB()

		if not runStatus.run:
			return

		cl.processTodoLinks(todo)
		cl.closeDB()
