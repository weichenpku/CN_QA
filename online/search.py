# -*- coding:utf-8 -*-

import sys, time, urllib2
from sys import argv
from sgmllib import SGMLParser
import math
import codecs
# import requests

class getPsgs(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.psgs = []
        self.mark = 0
        self.passage = ""
        self.stack = []

    def handle_starttag(self, tag, method, attrs):
        if tag == "dd":
            self.start_dd(attrs)
        self.stack.append(tag)

    def handle_endtag(self, tag, method):
        if tag == "dd":
            self.end_dd()
        self.stack.pop()

    def start_dd(self, attrs):
        for i in range(len(attrs)):
            if attrs[i][0] == "class" and attrs[i][1] == "dd answer":
                self.mark = 1
                self.passage = ""

    def end_dd(self):
        if self.mark == 1:
            self.mark = 0
            self.psgs.append(self.passage)
            self.passage = ""

    def handle_data(self, data):
        if self.mark == 1:
            self.passage += data.decode("gbk").encode("utf-8")

    def unknown_starttag(self, tag, attrs): pass
    def unknown_endtag(self, tag): pass


def search_baidu():
    # base_url = "http://www.baidu.com/s?wd="
    base_url = "https://zhidao.baidu.com/search?lm=0&rn=10&pn=0&fr=search&word="

    with codecs.open("../questions/debug.txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]
        lines = [line.split()[0].replace('？','') for line in lines]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    index = 0
    total_size = len(lines)
    batch_size = 200
    loop_size = int(math.ceil(float(total_size) / float(batch_size)))
    print loop_size
    for loop in range(loop_size):
        f = codecs.open("../questions/psgs/" + str(loop * batch_size) + "_" + str((loop + 1) * batch_size) + ".txt", "w")
        start = loop * batch_size
        end = min(total_size, (loop + 1) * batch_size)

        for _line in lines[start:end]:
            index += 1
            print "processing ..." + str(index)
            getpsg = getPsgs()
            line = _line.replace(" ", "%20")
            if line != "":
                print (base_url+line)
                while True:
                    try:
                        req = urllib2.Request(
                            url = base_url + line,
                            headers = headers
                            )
                        response = urllib2.urlopen(req)
                        break
                    except urllib2.HTTPError as e:
                        time.sleep(10)
                html = response.read()
                getpsg.feed(html)
            f.write("<question id=%d>\n" % index)
            for i in range(10):
                f.write("<doc>\n")
                f.write(getpsg.psgs[i] if i < len(getpsg.psgs) else "")
                f.write("\n</doc>\n")
            f.write("</question>\n")
        f.close()

def main():
    search_baidu()

if __name__ == "__main__":
    main()
