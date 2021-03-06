from Connection import connector
from screen import screen
from random import choice
from regex import regex

class Scanner_Web_Core (object):
	logos = [(" ___                             __      __   _    \n"
              "/ __| __ __ _ _ _  _ _  ___ _ _  \ \    / /__| |__ \n"
              "\__ \/ _/ _` | ' \| ' \/ -_) '_|  \ \/\/ / -_) '_ \ \n"
              "|___/\__\__,_|_||_|_||_\___|_|     \_/\_/\___|_.__/\n"
              ),
			  ("   ____                             _      __    __ \n"
			   "  / __/______ ____  ___  ___ ____  | | /| / /__ / / \n"
			   " _\ \/ __/ _ `/ _ \/ _ \/ -_) __/  | |/ |/ / -_) _ \ \n"
			   "/___/\__/\_,_/_//_/_//_/\__/_/     |__/|__/\__/_.__/\n"),
			  (
			   "  ()                                        (_|   |   |_/ | |  \n"
			   "  /\  __   __,   _  _    _  _    _   ,_       |   |   | _ | |  \n"
			   " /  \/    /  |  / |/ |  / |/ |  |/  /  |      |   |   ||/ |/ \_\n"
			   "/(__/\___/\_/|_/  |  |_/  |  |_/|__/   |_/     \_/ \_/ |__/\_/ \n")]

	googleDot = ["com", "ac", "com.om", "ad", "ae", "com.af", "com.ag", "com.ai", "am", "it.ao", "com.ar", "cat", "as", "at", "com.au", "az", "ba",
                "com.bd", "be", "bf", "bg", "com.bh", "bi", "bj", "com.bn", "com.bo", "com.br", "bs", "co.bw", "com.by", "com.bz", "ca", "com.kh",
    	        "cc", "cd", "cf", "cn", "com.co", "co.nz", "cg", "ch", "co.ck", "cl", "cm", "cz", "de", "nu", "dj",
                "dk", "dm", "com.do", "dz", "no", "com.ec", "ee", "com.eg", "es", "com.np", "fi", "com.fj", "fm", "fr", "ga", "nl", "ge",
                "gf", "gg", "com.gh", "com.gi", "nr", "gl", "gp", "gr", "com.gt", "com.ni", "gy", "com.hk", "hn", "com.ng",
                "co.id", "iq", "ie", "co.il", "com.nf", "im", "co.in", "is", "it", "ne", "je", "com.jm", "jo", "co.jp", "co.ke", "com.na",
                "kg", "co.kr", "la", "com.lb", "li", "com.my", "co.ls", "lt", "lu", "lv", "com.ly", "com.mx",
                "co.ma", "md", "mg", "mk", "ml", "mn", "ms", "com.mt", "mu", "mv", "com.pa", "com.pe", "com.ph", "com.pk", "pn", "com.pr",
                "ps", "pt", "com.py", "com.qa", "ro", "rs", "ru", "rw", "com.sa", "com.sb", "sc", "se", "com.sg", "sh", "si", "com.sl", "sn", "sm",
                "so", "st", "com.sv", "td", "tg", "co.th", "tk", "tl", "tm", "to", "com.tn", "com.tr", "tt", "com.tw", "co.tz", "com.ua", "co.ug", "co.uk",
                "us", "com.uy", "co.uz", "co.ve", "vg", "co.vi", "vu", "co.za", "co.zm", "co.zw"]

	Forbiden = ['facebook.com', 'twitter.', '.google.','github.', 'linkedin.', 'microsoft.', 'youtube.', 'bing.',"stackoverflow.","teamfortress",
		'yahoo.', 'sogou.', 'ask.', 'yandex.', 'msn.', 'w3school.','w3.', 'windows.', 'adobe.com', 'outlook.',"laravel.","wordpress.","w3schools"
		'window.', 'JQuery.min', 'hotmail.', 'yandex.','sogou.', 'bing.','php.', 'mysql.', 'microsofttranslator.','amazon.', 'www.asp.net',
		"devdocs.","steampowered.","origin.","adsense.google.","linuxmint.","ubuntu.","debian.","arch-linux.","w3schools.com"]
	
	cmsTags = {
			"wordpress":["<a href=\"https:\/\/wordpress.org\/\">Proudly powered by WordPress", "<meta name=\"|'generator\"|' content=\"|'WordPress\"|'", "\/wp-content\/(.*).js","wordpress/plugins"],
			"joomla" : ["<meta name=\"generator\" content=\"Joomla"]
		}

	def __init__(self, connector) :
		self.version = 1.8
		self.scanTitles = {"u":"URL SCAN","d":"DORK SEARCH","md5":"MD5 ENCRYPTATION"}
		self.sc = screen()
		self.connector = connector
		self.engins = {"google":"http://www.google.{}/search?q={}&start={}",
					   "bing":"http://www.bing.com/search?q={}&first={}",
					   }
		self.urlFound = []
		self.regex = regex()

	"""
	Method prepareEngin (self, dork, engin)
		return  String ==> url of engin for Dork search
	"""
	def prepareEngin(self, dork, page, engin):
		"""
		param dork string dork to add it to url engin 
		"""
		engin = engin.lower()
		if engin == "bing":
			return self.engins.get(engin).format(dork,page)
		elif engin == "google" :
			domain = choice(self.googleDot)
			return self.engins.get(engin).format(domain,self.connector.queryEncode(dork),page)
	
	"""
	Method searchDork (self, enginUrl)
		return search dork result after passing self.connector.connection(urlEngin) to getDorkResutls method 
	"""
	def searchDork(self,enginUrl, engin):
		"""
		param enginUrl string 
		"""
		enginResponse = self.connector.connection(enginUrl)
		try :
			return self.getDorkResults( enginResponse.response.read().decode("utf-8","ignore"), engin  )
		except Exception :
			pass
	"""
	Method getDorkResults(self, html)
		return self.urlFound after filtring html code passed by searchDork and engin used
	"""
	def getDorkResults (self, html, engin):
		"""
		param html string html code  
		"""
		if engin == "bing":
			result = self.regex.findRegex(r'<h2><a href="(.*?)" h="',html)
		elif engin == "google":
			result = self.regex.findRegex(r'<div class="r"><a href="(.*?)"', html)
			
		for url in result :
			if self.isForbiden(url) == False and url not in self.urlFound :
				self.urlFound.append(url) 
		return self.urlFound
	
	"""
	Method isForbiden(self, url)
		check if the domain is forbiden 
		return False if url is not Forbiden True else
	"""
	def isForbiden(self,url):
		"""
		param url String 
		"""
		for forbiden in self.Forbiden :
			if forbiden in connector.parser(url).netloc :
				return True
		return False
	
	"""
	Method cmsDetector(self, hmtl)
		look for self.cmsTags in the html code
		return detected cms if true or not detected if is not detected
	"""
	def cmsDetector(self, html):
		"""
		param html string html code after connecting to target
		"""
		# TODO : think to use regex
		for cms in self.cmsTags.keys():
			for cmsTag in self.cmsTags.get(cms):
				if cmsTag in html:
					return cms
		return "not detected"
	
	"""
	Method pageSearcher(self, url)
		check if url is exist using method connetion.isExist in class connector after parse it 
		return url if is found and False if is not found 
	"""
	def pageSearcher(self,url, uris):
		"""
		param urls string
		"""
		parsedUrl = self.connector.parser(url)
		for path in uris:
			fullUrl = parsedUrl.scheme +"://"+ parsedUrl.netloc + path
			self.sc.prInfo("Looking for",fullUrl,rtn=True)

			if self.connector.isExist(self.connector.connection(fullUrl).status):
					return fullUrl
		return False

	"""
	Method validation (self,validation,html)
		return true if validation param found in the html code and False else
	"""
	def validation (self,validation,html):
		"""
		param validation, html String
		"""
		if validation in html :
			return True
		return False
	"""
	Method updtaeCecker(self)
		return True if a new version is available or False if not 
	"""
	def updateChecker(self):
		getVersion = self.regex.findRegex(r"<!-- Version (\d+\.\d+) -->",str(self.connector.connection("https://raw.githubusercontent.com/SuicV/Scanner-web/master/README.md").response.read()))[0]
		if float(getVersion) > self.version :
			return True
		return False
