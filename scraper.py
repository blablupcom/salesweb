from splinter import Browser
import scraperwiki

with Browser("phantomjs") as browser:
    url = 'http://salesweb.civilview.com/Default.aspx?id=01230'
    browser.visit(url)
    page_soup = bs(browser.html, 'lxml')
    rows = page_soup.find('table', 'mGrid').find_all('tr')[1:]
    for i, row in enumerate(rows):
        details_row = i+2
        details = browser.find_by_xpath('/html/body/form/div[3]/table/tbody/tr[6]/td/div/table/tbody/tr[{}]/td[1]/a'.format(details_row))
        details.click()
        page_detail_soup = bs(browser.html, 'lxml')
        approx_judgment = page_detail_soup.find('td', text=re.compile('Judgment')).find_next('td').text.strip()
        redemption = page_detail_soup.find('td', text=re.compile('Redemption')).find_next('td').text.strip()
        sales_date = page_detail_soup.find('td', text=re.compile('Sales Date')).find_next('td').text.strip()
        address = page_detail_soup.find('td', text=re.compile('Address')).find_next('td').text.strip()
        back = browser.find_by_value('Back').click()
        num_sheriff = row.find('td').find_next('td').text.strip()
        print(num_sheriff)
        scraperwiki.sqlite.save(unique_keys=['num_sheriff'], data={'num_sheriff': num_sheriff, 'sales_date': sales_date, 'address': address, 'approx_judgment': approx_judgment, 'redemption': redemption})
