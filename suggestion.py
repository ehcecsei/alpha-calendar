from datetime import datetime
from agenda import Agenda
from jdcommodity import JDCommodity
import random

class Suggestion(object):
	def __init__(self, jdID, db):
		self.jdID = jdID
		self.db = db

		self.events = None
		self.today = datetime.now()
		self.pastEvents = []
		self.futureEvents = []

		self.eventdetail = ""
		self.search = ""
		self.keyword = ""
		self.suggest = ""

		self.adsIntro = []
		self.adsEnding = []
		self.complainEnding = []
		self.lazyEnding = []

		self.eventdict = {}
		self.keywordict = {}

		self.__query_all_events()
		#self.__classify_events()
		self.__populate_phrases()
		

	def __query_all_events(self):
		self.events = self.db.session.query(Agenda.startTime, Agenda.endTime, 
			Agenda.agendaType, Agenda.agendaDetail).filter(Agenda.jdID==self.jdID).all()

	def __classify_events(self):
		for e in self.events:
			event = QueriedEvent(e)
			if event.is_future() is False:
				self.pastEvents.append(event)
			else:
				self.futureEvents.append(event)

	def __get_pastEvents(self):
		return self.pastEvents

	def __get_futureEvents(self):
		return self.futureEvents

	def __suggestion_gen(self):
		type_no = random.randrange(0, 5, 1)
		if len(self.events) == 0:
			suggest = self.__nonesense_gen()
		elif type_no == 4:
			suggest = self.__nonesense_gen()
		else:
			suggest = self.__ads_gen()
		return suggest


	def __nonesense_gen(self):
		num = len(self.events)
		if num < 5:
			randnum = random.randrange(0, len(self.complainEnding), 1)
			rst = "这段时间...您没记录几条计划呀。" + self.complainEnding[randnum]
		else:
			randnum = random.randrange(0, len(self.lazyEnding), 1)
			rst = "很荣幸呀，这段时间您一共记录了" + str(num) + "条计划。" + self.lazyEnding[randnum]

		return rst

	def __ads_gen(self):
		self.__get_keyword()
		commodity = JDCommodity(self.keyword)
		inum = random.randrange(0, len(self.adsIntro), 1)
		enum = random.randrange(0, len(self.adsEnding), 1)
		suggest = "根据您的" + self.eventdetail + "计划，" + self.adsIntro[inum] + commodity.get_info() + self.adsEnding[enum]
		return suggest

	def __get_keyword(self):
		self.__populate_dict()
		num = random.randrange(0, len(self.events), 1)
		self.eventdetail = self.events[num][3]
		self.keyword = self.eventdict[self.eventdetail]
		self.search = self.keywordict[self.keyword]

	def __populate_dict(self):
		f = open('eventkey', 'r')
		lines = f.readlines()
		for l in lines:
			a = l.rstrip().split(' ')
			self.eventdict[a[0]] = a[1]
		f.close()

		f = open('jdkey', 'r')
		lines = f.readlines()
		for l in lines:
			a = l.rstrip().split(' ')
			self.keywordict[a[0]] = [i for i in a[1:]]
		f.close()


	def __populate_phrases(self):
		self.complainEnding = ["真担心我会下岗...", "看来最近不忙呀，挺好挺好。", 
		"别抛弃我呀，我还在不断进步呢", "好难过的说，一难过就给不了什么建议了", 
		"想抱怨几句...算了，还是不说了", "我该提些什么建议呢..."]

		self.lazyEnding = ["看在我工作这么努力的份上...今儿就让我打个酱油怎样。", "看来您最近安排挺多的，我就不打扰啦。",
		"不过我今天有些懒...就不具体帮您分析了。", "感谢您的使用！我也会更努力的。", "遇到这么努力的您，我真的好感动呀。"]

		self.adsIntro = ["我向您推荐京东上的: ","我来打个京东软广告: ","我在京东上找到您可能会喜欢的: ", 
		"我在京东上找到有关的"]

		self.adsEnding = ["打了很多的软广告，希望您不要介意。", "如果您感兴趣的话，可以到京东上购买噢。感谢您的宝贵时间。", 
		"感谢您听完我的软广告。", "感谢您的时间，希望您喜欢这则广告。"]


	def get_suggestion(self):
		suggest = self.__suggestion_gen()
		return suggest




		
