#wallhaven热门图片采集下载
#author 微信：huguo00289
#https://cloud.tencent.com/developer/article/1799246
# —*—coding: utf-8 -*-
import requests
from lxml import etree
from fake_useragent import UserAgent
import time
from requests.adapters import HTTPAdapter
import threading


class Top(object):
    def __init__(self):
        self.ua=UserAgent().random
        self.url="https://wallhaven.cc/user/dhark4511/uploads?page="

    def get_response(self,url):
        response=requests.get(url=url, headers={'user-agent': self.ua}, timeout=6)
        return response

    def get_third(self,url,num):
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=num))
        s.mount('https://', HTTPAdapter(max_retries=num))

        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        try:
            r = s.get(url=url, headers={'user-agent': self.ua},timeout=5)
            return r
        except requests.exceptions.RequestException as e:
            print(e)
        print(time.strftime('%Y-%m-%d %H:%M:%S'))


    def get_html(self,response):
        html = response.content.decode('utf-8')
        tree = etree.HTML(html)
        return tree

    def parse(self,tree):
        imgsrcs = tree.xpath('//ul/li/figure/img/@data-src')
        print(len(imgsrcs))
        return imgsrcs

    def get_imgurl(self,imgsrc):
        img = imgsrc.replace("th", "w").replace("small", "full")
        imgs = img.split('/')
        imgurl = f"{'/'.join(imgs[:-1])}/wallhaven-{imgs[-1]}"
        print(imgurl)
        return imgurl

    def down(self,imgurl,imgname):
        #r=self.get_response(imgurl)
        r = self.get_third(imgurl,3)
        with open(f'{imgname}', 'wb') as f:
            f.write(r.content)
            print(f"保存 {imgname} 图片成功！")
        time.sleep(2)

    def downimg(self,imgsrc,pagenum,i):
        imgurl = self.get_imgurl(imgsrc)
        imgname = f'{pagenum}-{i}{imgurl[-4:]}'
        try:
            self.down(imgurl, imgname)
        except Exception as e:
            print(f"下载图片出错，错误代码：{e}")
            if "jpg" in imgname:
                ximgname = f'{pagenum}-{i}.png'
            if "png" in imgname:
                ximgname = f'{pagenum}-{i}.jpg'
            self.down(imgurl, ximgname)



    def get_topimg(self,pagenum):
        url=f'{self.url}{pagenum}'
        print(url)
        response=self.get_response(url)
        tree=self.get_html(response)
        imgsrcs=self.parse(tree)
        i=1
        for imgsrc in imgsrcs:
            self.downimg(imgsrc,pagenum,i)
            i=i+1

    def get_topimgs(self,pagenum):
        url=f'{self.url}{pagenum}'
        print(url)
        response=self.get_response(url)
        tree=self.get_html(response)
        imgsrcs=self.parse(tree)
        i=1
        threadings = []
        for imgsrc in imgsrcs:
            t = threading.Thread(target=self.downimg, args=(imgsrc,pagenum,i))
            i = i + 1
            threadings.append(t)
            t.start()

        for x in threadings:
            x.join()

        print("多线程下载图片完成")


    def main(self):
        num=3
        for pagenum in range(1,num+1):
            print(f">>正在采集第{pagenum}页图片数据..")
            self.get_topimgs(pagenum)


if __name__=='__main__':
    spider=Top()
    spider.main()