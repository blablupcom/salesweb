from splinter import Browser
import scraperwiki

with Browser("phantomjs") as browser:
	url = 'http://salesweb.civilview.com/Default.aspx?id=01230'
	browser.visit(url)
	button = browser.find_by_xpath('/html/body/form/div[3]/table/tbody/tr[6]/td/div/table/tbody/tr[2]/td[1]/a')
	button.click()
	browser.is_text_present('Approx.')
	a = browser.find_by_xpath('/html/body/form/div[3]/table/tbody/tr[3]/td/div/table/tbody/tr[2]/td[2]').text
	scraperwiki.sqlite.save(unique_keys=['a'], data={"a": a})
