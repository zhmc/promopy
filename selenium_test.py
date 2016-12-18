 # -*- coding:utf-8-*-
import browser
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys,os
type=sys.getfilesystemencoding()

print "程序开始 ".decode('utf-8').encode(type) + browser.strftime('%Y-%m-%d %H:%M:%S')
driver = webdriver.PhantomJS(service_args=['--load-images=no'])

#firefoxBin = os.path.abspath("C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe")
#os.environ["webdriver.firefox.bin"] = firefoxBin
#driver2 = webdriver.Firefox()

#driver2 = webdriver.Firefox(executable_path="C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe")

print "加载浏览器完成 ".decode('utf-8').encode(type) + browser.strftime('%Y-%m-%d %H:%M:%S')
url="http://promomart.espwebsite.com/ProductResults/?SearchTerms=HAT"

#wait = ui.WebDriverWait(driver,15)


driver.get(url)

print "加载页面1完成 ".decode('utf-8').encode(type) + browser.strftime('%Y-%m-%d %H:%M:%S')

"""
locator = (By.XPATH, '//input[@class="ProdID"]')
try:
  WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))
  print driver.find_element_by_xpath('//input[@class="ProdID"]').get_attribute('value')
finally:
  driver.close()
"""

for i in range(20):
	locator2 = (By.XPATH, '//a[@class="edcPageNext"]')
	WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator2))
	link = driver.find_element_by_xpath('//a[@class="edcPageNext"]')
	link.click()
	print "加载页面".decode('utf-8').encode(type)+str(i+2)+"完成: ".decode('utf-8').encode(type) + browser.strftime('%Y-%m-%d %H:%M:%S')



#wait.until(lambda driver: driver.find_element_by_xpath('//div[@class="col4 prodPannel"]')
#driver_item.find_element_by_xpath("//div[@class='fliter-wp']/div/form/div/div/label[5]").click()

ProdIDs = driver.find_elements_by_xpath('//input[@class="ProdID"]')
for item in ProdIDs:
	one = item.get_attribute('value')
	print "id " ,one

print "程序结束 ".decode('utf-8').encode(type) + browser.strftime('%Y-%m-%d %H:%M:%S')
driver.close()