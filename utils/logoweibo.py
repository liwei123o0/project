# -*- coding: utf-8 -*-
#! /usr/bin/env python

from selenium import webdriver
import time
driver   = webdriver.Firefox()

driver.get("http://d.weibo.com/")
driver.find_element_by_xpath("(//ul[@class='gn_login_list']//a[@class='S_txt1'])[last()]").click()
time.sleep(100)
driver.quit()