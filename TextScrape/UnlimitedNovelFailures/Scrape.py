
import logSetup
if __name__ == "__main__":
	print("Initializing logging")
	logSetup.initLogging()

import TextScrape.TextScrapeBase

import readability.readability
import bs4
import webFunctions


class Scrape(TextScrape.TextScrapeBase.TextScraper):
	tableKey = 'unf'
	loggerPath = 'Main.Unf.Scrape'
	pluginName = 'UnlimitedNovelFailuresScrape'



	wg = webFunctions.WebGetRobust(logPath=loggerPath+".Web")

	threads = 1

	baseUrl = "http://unlimitednovelfailures.mangamatters.com/"

	startUrl = baseUrl

	# Any url containing any of the words in the `badwords` list will be ignored.
	badwords = [
					'/disclaimer/',
					'/about/',
					'like_comment=',
					'replytocom=',
					'?share=',
					'/comment-page-',
					'wp-login.php',
				]

	decompose = [

		{'id'    : 'comment-wrap'},
		{'id'    : 'sidebar'},
		{'id'    : 'content-bottom'},
		{'id'    : 'content-top'},
		{'id'    : 'menu'},
		{'id'    : 'main_bg'},



		{'id'    : "fancybox-tmp"},
		{'id'    : "fancybox-loading"},
		{'id'    : "fancybox-overlay"},
		{'id'    : "fancybox-wrap"},

		{'class' : 'meta-info'},

		# {'id'    : 'header'},
		# {'id'    : 'footer'},
		# {'id'    : 'comments'},
		# {'id'    : 'nav-above'},
		# {'id'    : 'nav-below'},

		# {'id'    : 'jp-post-flair'},
		# {'id'    : 'likes-other-gravatars'},
		# {'style' : 'display:none'},

		# {'name'     : 'likes-master'},

		# {'id'     : 'primary'},
		# {'id'     : 'secondary'},
		# {'id'     : 'calendar_wrap'},
		# {'class'  : 'widget-area'},
		# {'class'  : 'xoxo'},

		# {'class'  : 'sd-title'},
		# {'class'  : 'sd-content'},


	]


	def cleanBtPage(self, inPage):

		# since readability strips tag attributes, we preparse with BS4,
		# parse with readability, and then do reformatting *again* with BS4
		# Yes, this is ridiculous.
		soup = bs4.BeautifulSoup(inPage)

		# Decompose all the parts we don't want
		for key in self.decompose:
			for instance in soup.find_all(True, attrs=key):
				instance.decompose()


		doc = readability.readability.Document(soup.prettify())
		doc.parse()
		content = doc.content()

		soup = bs4.BeautifulSoup(content)

		contents = ''


		# Relink all the links so they work in the reader.
		for aTag in soup.find_all("a"):
			try:
				aTag["href"] = self.convertToReaderUrl(aTag["href"])
			except KeyError:
				continue

		for imtag in soup.find_all("img"):
			try:
				imtag["src"] = self.convertToReaderUrl(imtag["src"])
			except KeyError:
				continue

		# Generate HTML string for /just/ the contents of the <body> tag.
		for item in soup.body.contents:
			if type(item) is bs4.Tag:
				contents += item.prettify()
			elif type(item) is bs4.NavigableString:
				contents += item
			else:
				print("Wat", item)

		title = doc.title()
		title = title.replace(" - Baka-Tsuki", "")

		return title, contents



	def processPage(self, url, content, mimeType):


		pgTitle, pgBody = self.cleanBtPage(content)
		self.extractLinks(content)
		self.updateDbEntry(url=url, title=pgTitle, contents=pgBody, mimetype=mimeType, dlstate=2)


	# Retreive remote content at `url`, call the appropriate handler for the
	# transferred content (e.g. is it an image/html page/binary file)
	def retreiveItemFromUrl(self, url):
		self.log.info("Fetching page '%s'", url)
		content, fName, mimeType = self.getItem(url)

		links = []

		if mimeType == 'text/html':
			self.log.info("Processing '%s' as HTML.", url)
			self.processPage(url, content, mimeType)
		elif mimeType in ["image/gif", "image/jpeg", "image/pjpeg", "image/png", "image/svg+xml", "image/vnd.djvu"]:
			self.log.info("Processing '%s' as an image file.", url)
			self.saveFile(url, mimeType, fName, content)
		elif mimeType in ["application/octet-stream"]:
			self.log.info("Processing '%s' as an binary file.", url)
			self.saveFile(url, mimeType, fName, content)
		else:
			self.log.warn("Unknown MIME Type? '%s', Url: '%s'", mimeType, url)


		return links

def test():
	scrp = Scrape()
	scrp.crawl()
	# scrp.retreiveItemFromUrl(scrp.baseUrl)


if __name__ == "__main__":
	test()




