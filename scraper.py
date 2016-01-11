# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from splinter import Browser
import scraperwiki
from bs4 import BeautifulSoup as bs
import re


with Browser("phantomjs") as browser:
    # -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import scraperwiki
from bs4 import BeautifulSoup as bs
import csv
import re
from splinter import Browser
import requests


def salesweb():
    with Browser() as browser:
        url = 'http://salesweb.civilview.com/Default.aspx?id=01230'
        browser.visit(url)
        page_soup = bs(browser.html, 'lxml')
        rows = page_soup.find('table', 'mGrid').find_all('tr')[1:]
        for i, row in enumerate(rows):
            details_row = i+2
            print details_row-1
            num_sheriff = row.find('td').find_next('td').text.strip()
            details = browser.find_by_xpath('/html/body/form/div[3]/table/tbody/tr[6]/td/div/table/tbody/tr[{}]/td[1]/a'.format(details_row))
            details.click()
            page_detail_soup = bs(browser.html, 'lxml')
            approx_judgment = page_detail_soup.find('td', text=re.compile('Judgment')).find_next('td').text.strip()
            redemption = page_detail_soup.find('td', text=re.compile('Redemption')).find_next('td').text.strip()
            sales_date = page_detail_soup.find('td', text=re.compile('Sales Date')).find_next('td').text.strip()
            brs = page_detail_soup.find('td', text=re.compile('Address')).find_next('td').find_all('br')
            if len(brs) == 1:
                search_address = address = ''
                try:
                    search_address = page_detail_soup.find('td', text=re.compile('Address')).find_next('td').find('br').previousSibling.strip()
                    address = search_address+' '+page_detail_soup.find('td', text=re.compile('Address')).find_next('td').find('br').nextSibling.strip()
                except:
                    pass

            elif len(brs) == 2:
                unit = page_detail_soup.find('td', text=re.compile('Address')).find_next('td').find('br').find_next('br').previousSibling.strip().replace('DUPLEX', '')
                if '-' in unit:
                    unit = ''
                elif 'UNIT 10 D' in unit:
                    unit = 'UNIT 10D'
                street_address = page_detail_soup.find('td', text=re.compile('Address')).find_next('td').find('br').previousSibling.strip()
                search_address = street_address+' '+unit
                address = street_address+' '+unit+' '+page_detail_soup.find('td', text=re.compile('Address')).find_next('td').find('br').find_next('br').nextSibling.strip()
            with Browser() as assess_browser:
                assess_url = 'http://web.assess.co.polk.ia.us/cgi-bin/web/tt/form.cgi?tt=query/basic/homepage&submit_form=1&'
                assess_browser.visit(assess_url)
                print search_address
                if not search_address:
                    mailing_address = geoparcel = total = ''
                else:
                    search = assess_browser.fill('straddr__address', search_address.strip())
                    perform = assess_browser.find_by_name('submit_form').click()
                    check_soup = bs(assess_browser.html, 'lxml')
                    records = ''
                    try:
                        records = check_soup.find('span', 'normal').previousSibling.previousSibling.split(' Records')[0][-1:].strip()
                    except:
                        pass
                    print records
                    if records and int(records) == 0:
                        try:
                            assess_browser.visit(assess_url)
                            search = assess_browser.fill('straddr__address', search_address.strip().split('UNIT')[0].strip())
                            perform = assess_browser.find_by_name('submit_form').click()
                            district_soup = bs(assess_browser.html, 'lxml')
                            mailing_address = ''
                            try:
                                mailing_address = district_soup.find('caption', text=re.compile('Mailing Address')).find_next('tr').find('td').find_next('td').text.strip()
                            except:
                                pass
                            if not mailing_address:
                                street_page_row = district_soup.find('table', 'allborder stripe ').find('tbody').find('a')
                                if not street_page_row:
                                    total = mailing_address = geoparcel = ''

                                else:
                                    link = 'http://web.assess.co.polk.ia.us'+street_page_row['href']
                                    total = street_page_row.find_next('td').find_next('td').text.strip()
                                    district_page = requests.get(link)
                                    district_list_soup = bs(district_page.text, 'lxml')
                                    mailing_address = district_list_soup.find('caption', text=re.compile('Mailing Address')).find_next('tr').find('td').find_next('td').text.strip()
                                    geoparcel = district_list_soup.find('th', text=re.compile('Geoparcel')).find_next('td').text.strip()
                            else:
                                geoparcel = district_soup.find('th', text=re.compile('Geoparcel')).find_next('td').text.strip()
                                total = district_soup.find('th', text=re.compile('Total')).find_next('tr').find_all('td')[-1].text.strip()
                            print mailing_address, geoparcel, total
                        except:
                            mailing_address = geoparcel = total = ''
                    if assess_browser.is_text_present('Geoparcel', wait_time=10):
                        district_soup = bs(assess_browser.html, 'lxml')
                        mailing_address = district_soup.find('caption', text=re.compile('Mailing Address')).find_next('tr').find('td').find_next('td').text.strip()
                        geoparcel = district_soup.find('th', text=re.compile('Geoparcel')).find_next('td').text.strip()
                        total = district_soup.find('th', text=re.compile('Total')).find_next('tr').find_all('td')[-1].text.strip()
                    else:
                        district_soup = bs(assess_browser.html, 'lxml')
                        street_page_row = district_soup.find('table', 'allborder stripe ').find('tbody').find('a')
                        if not street_page_row:
                            total = mailing_address = geoparcel = ''
                        else:
                            link = 'http://web.assess.co.polk.ia.us'+street_page_row['href']
                            total = street_page_row.find_next('td').find_next('td').text.strip()
                            district_page = requests.get(link)
                            district_list_soup = bs(district_page.text, 'lxml')
                            mailing_address = district_list_soup.find('caption', text=re.compile('Mailing Address')).find_next('tr').find('td').find_next('td').text.strip()
                            geoparcel = district_list_soup.find('th', text=re.compile('Geoparcel')).find_next('td').text.strip()
                print num_sheriff
                scraperwiki.sqlite.save(unique_keys=['num_sheriff'], data={'num_sheriff': num_sheriff, 'sales_date': sales_date, 'address': address, 'approx_judgment': approx_judgment, 'redemption': redemption,  'mailing_address': mailing_address, 'geoparcel': geoparcel, 'total': total})

            back = browser.find_by_value('Back').click()




if __name__ == '__main__':
        s= salesweb()
