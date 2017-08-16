# -*- coding: utf-8 -*-
import requests
from lxml import html
from lxml import etree
import sys 
reload(sys) 
sys.setdefaultencoding( "utf-8" )

def cmpBook(book1, book2):
	if float(book1.rating) > float(book2.rating):
		return -1
	elif float(book1.rating) == float(book2.rating):
		return 0
	else:
		return 1

class Book:
	def __init__(self, title, rating, link):
		self.title = title
		self.rating = rating
		self.link = link
	def tohtml(self):
		return u'<h2><a href="%s">%s</a></h2><h3>%s</h3>' % (self.link, self.title, self.rating)

bookList = []
start = 0
s = requests.session()
for i in range(100):
	# 投资
	# url = 'https://book.douban.com/tag/%E6%8A%95%E8%B5%84?start={}&type=S'.format(start)
	# 金融史
	#url = 'https://book.douban.com/tag/%E9%87%91%E8%9E%8D%E5%8F%B2?start={}&type=S'.format(start)
	# 金融
	#url = 'https://book.douban.com/tag/%E9%87%91%E8%9E%8D?start={}'.format(start)
	url = sys.argv[2] + '?start={}'.format(start)

	page = s.get(url)
	doc = html.fromstring(page.content)
	books = doc.xpath('//li[@class="subject-item"]/div[@class="info"]')
	if (len(books) == 0):
		break
	else:
		start += len(books)
	for book in books:
		titleElement = book.xpath('.//h2/a')[0]
		title = titleElement.text.strip(" \n")
		link = titleElement.attrib['href']
		rating = book.xpath('.//span[@class="rating_nums"]')
		rating_nums = '0.0'
		if len(rating) > 0:
			rating_nums = rating[0].text
		bookList.append(Book(title, rating_nums, link))

bookList = sorted(bookList, cmp = cmpBook)


s = u'<!DOCTYPE html><head></head><body>'
for book in bookList:
	if float(book.rating) > float('7.5'):
		s += book.tohtml()

s += u'</body></html>'
name = "douban.html"
if len(sys.argv) > 1:
	name = sys.argv[1]
f = open(name, "w")
f.write(s)
f.close()