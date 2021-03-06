

from ScrapePlugins.PururinLoader.pururinDbLoader import PururinDbLoader
from ScrapePlugins.PururinLoader.pururinContentLoader import PururinContentLoader

import settings

import runStatus

import ScrapePlugins.RunBase

class Runner(ScrapePlugins.RunBase.ScraperBase):


	loggerPath = "Main.Pururin.Run"
	pluginName = "Pururin"


	sourceName = "Pururin"
	feedLoader = PururinDbLoader
	contentLoader = PururinContentLoader





if __name__ == "__main__":
	import utilities.testBase as tb

	with tb.testSetup(startObservers=False):
		mon = Runner()
		mon.go()

