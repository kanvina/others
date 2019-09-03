import scrapy
from scrapy.spiders import Spider
from scrapy import cmdline
import pandas as pd
import time


class spider_by_wyd(Spider):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',}
    name = 'spyder_create_by_WYD'

    def start_requests(self):

        for i in range(1,100):
            url_name= 'https://xz.58.com/xiaoqu/pn_{0}'.format(i)
            yield scrapy.Request(url_name, headers=self.headers)
            time.sleep(5)


        # url_name= 'https://xz.58.com/xiaoqu/pn_{0}'.format('60')
        # yield scrapy.Request(url_name, headers=self.headers)

    def parse(self, response):
        SpiderUrl = response.xpath('///html/body/div[4]/div[4]/div[1]/ul/li')
        list_out=[]
        for SpiderInfo in SpiderUrl:
            try:
                building_area_name = SpiderInfo.xpath('div[2]/h2/a/text()').extract()[0]
                price = SpiderInfo.xpath('div[3]/p[2]/text()').extract()[0]
                greening_rate=''
                try :
                    greening_rate=str(SpiderInfo.xpath('div[2]/p[2]/span[2]/span[2]/text()').extract()[0])
                except :
                    pass
                plot_ratio=''
                try:
                    plot_ratio = str(SpiderInfo.xpath('div[2]/p[2]/span[3]/span[2]/text()').extract()[0])
                except:
                    pass
                address=''

                try:
                    address=str(SpiderInfo.xpath('div[2]/p[1]').extract()[0]).replace(' ','').replace('<pclass="baseinfo">','').replace('<span>','').replace('</span>','').replace('</p>','').replace('\n','')

                    # address_out_list=[]
                    # for address in address_list:
                    #     address_out_list.append(address)

                except:
                    pass
                list_out.append([building_area_name,price,greening_rate,plot_ratio,address])
                # print(building_area_name,price,greening_rate,plot_ratio,adddress_text)

            except:
                print('异常：',SpiderInfo)
        pd.DataFrame(list_out).to_csv('result/price_list_all.csv',index=0,header=0,mode='a+')

if __name__=='__main__':


    cmdline.execute("scrapy crawl spyder_create_by_WYD ".split())
    # cmdline.execute(['scrapy','crawl','spyder_create_by_WYD'])
