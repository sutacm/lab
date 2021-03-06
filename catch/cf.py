import urllib
import urllib2
import re
from config import cf_timeout 
from threading import Timer
from time import time
#import socket
#socket.setdefaulttimeout(5)


class cf:

    def __init__(self):
        self.url_head = 'http://codeforces.com/profile'
        self.open_timeout = 5.0
        self.read_timeout = cf_timeout


    def __match(self, text):
        s = (r'span style=\"font-weight:bold;\" class=\".*?\">(?P<rating>\d*?)</span>')
        pattern = re.compile(s)
        match = pattern.search(text)
        if match != None:
            return match.group('rating')
        else:
            #print 'miss match when find cf_name = %s' % (self.name)
            return '0'


    def __handler(self, response):
        response.close()


    def __catch(self, name):
        url = '%s/%s' %(self.url_head, name)
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=self.open_timeout)
            t = Timer(self.read_timeout, self.__handler, [response])
            t.start()
            html = response.read()
            t.cancel()
            text = ''
            for line in html:
                text += line 
            return text
        except:
            #print 'timeout when find cf_name = %s' % (name)
            return ''


    def __find(self, name):
        start_time = time()
        if name == '' or name == None:
            return
        text = self.__catch(name=name)
        end_time = time()
        if text != '':
            solved = self.__match(text)
            if solved != '0':
                self.results[name] = solved
            print name, solved, end_time - start_time
    
    
    def find_one(self, name):
        self.results = {}
        self.__find(name=name)
        return self.results


    def find_multi(self, names=[]):
        self.results = {}
        for name in names:
            self.__find(name=name)
        return self.results


