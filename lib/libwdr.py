# -*- coding: utf-8 -*-
import libwdrparser as libWdrParser
#import libwdrjsonparser as libWdrJsonParser
import libwdrrssparser as libWdrRssParser
import libwdrrssandroidparser as libWdrRssAndroidParser
from libmediathek4 import lm4

ignoreLetters=['#','q','x']

class libwdr(lm4):
	def __init__(self):
		lm4.__init__(self)
		self.defaultMode = 'libWdrListMain'
	
		self.modes.update({
		'libWdrListMain': self.libWdrListMain,
		'libWdrListLetter': self.libWdrListLetter,
		'libWdrListVideos': self.libWdrListVideos,
		'libWdrListId': self.libWdrListId,
		'libWdrListFeed': self.libWdrListFeed,
		'libWdrListDateVideos': self.libWdrListDateVideos,
		'libWdrSearch': self.libWdrSearch,
		'libWdrListSearch': self.libWdrListSearch,
		})

		self.playbackModes = {
			'libWdrPlay':self.libWdrPlay,
			'libWdrPlayAudio':self.libWdrPlayAudio,
			'libWdrPlayJs':self.libWdrPlayJs,
		}

	def libWdrListMain(self):
		l = []
		l.append({'metadata':{'name':self.translation(32030)}, 'params':{'mode':'libWdrListId', 'id':'sendung-verpasst-100'}, 'type':'dir'})
		l.append({'metadata':{'name':self.translation(32132)}, 'params':{'mode':'libMediathekListLetters','ignore':'#', 'subParams':'{"mode":"libWdrListLetter"}'}, 'type':'dir'})
		l.append({'metadata':{'name':self.translation(32133)}, 'params':{'mode':'libMediathekListDate', 'subParams':'{"mode":"libWdrListDateVideos"}'}, 'type':'dir'})
		"""
		l.append({'_name':self.translation(31032), 'mode':'libWdrListLetters', '_type':'dir'})
		l.append({'_name':self.translation(31033), 'mode':'libWdrListDate', '_type':'dir'})
		#l.append({'name':'Videos in Gebärdensprache', 'mode':'libWdrListFeed', 'url':'http://www1.wdr.de/mediathek/video/sendungen/videos-dgs-100~_format-mp111_type-rss.feed', '_type':'dir'})
		#l.append({'name':'Videos mit Untertiteln', 'mode':'libWdrListFeed', 'url':'http://www1.wdr.de/mediathek/video/sendungen/videos-untertitel-100~_format-mp111_type-rss.feed', '_type':'dir'})
		l.append({'_name':self.translation(31039), 'mode':'libWdrSearch', '_type':'dir'})
		"""
		return {'items':l,'name':'root'}
		
	def libWdrListLetter(self):
		return libWdrRssAndroidParser.parseShows(f'sendungen-{self.params["letter"]}-102')
		
	def libWdrListVideos(self):
		return libWdrRssAndroidParser.parseVideos(self.params['url'])
		
	def libWdrListId(self):
		return libWdrRssParser.parseFeed(f'https://www1.wdr.de/{self.params["id"]}~_format-mp111_type-rss.feed')

	def libWdrListFeed(self):
		return libWdrRssParser.parseFeed(self.params['url'])

	def libWdrListDateVideos(self):
		self.params['id'] = f'sendung-verpasst-100~_tag-{self.params["ddmmyyyy"]}'
		return self.libWdrListId()
		
	def libWdrSearch(self):
		import libwdrhtmlparser as libWdrHtmlParser
		#search_string = libMediathek.getSearchString()
		return libWdrHtmlParser.parse("http://www1.wdr.de/mediathek/video/suche/avsuche100~suche_parentId-videosuche100.html?pageNumber=1&sort=date&q="+search_string)
		
	def libWdrListSearch(self):
		import libwdrhtmlparser as libWdrHtmlParser
		return libWdrHtmlParser.parse(self.params['url'])
		
	def libWdrPlay(self):
		if 'm3u8' in self.params:
			return {'media':[{'url':self.params['m3u8'], 'type':'video', 'stream':'HLS'}]}
		else:
			return libWdrParser.parseVideo(self.params['url'])
		
	def libWdrPlayAudio(self):
		import libwdrnimex
		return libwdrnimex.getAudio(self.params['id'])
		
	def libWdrPlayJs(self):
		return libWdrParser.parseVideoJs(self.params['url'])
		
		