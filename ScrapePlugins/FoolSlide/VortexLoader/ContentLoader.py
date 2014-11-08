
import webFunctions
import settings

import ScrapePlugins.RetreivalBase

import ScrapePlugins.FoolSlide.FoolSlideDownloadBase

class ContentLoader(ScrapePlugins.FoolSlide.FoolSlideDownloadBase.FoolContentLoader):




	loggerPath = "Main.Vs.Cl"
	pluginName = "Vortex Scans Content Retreiver"
	tableKey = "vx"
	dbName = settings.dbName
	tableName = "MangaItems"
	groupName = "VortexScans"

	wg = webFunctions.WebGetRobust(logPath=loggerPath+".Web")

	retreivalThreads = 1

	contentSelector = ('article', 'content')

if __name__ == '__main__':
	import utilities.testBase as tb

	with tb.testSetup():
		fl = ContentLoader()

		fl.go()
