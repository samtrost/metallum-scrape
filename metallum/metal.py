from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import csv
import string


csv_file = open('bands.csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(['name', 'ID'])

for letter in list(string.ascii_uppercase):
	driver = webdriver.Chrome('./chromedriver.exe')
	driver.get("https://www.metal-archives.com/lists/" + str(letter))

	index = 1
	while True:
		try:
			print("Scraping page:" + str(index))
			index += 1

			wait_bands = WebDriverWait(driver, 10)
			time.sleep(5)
			bands = wait_bands.until(EC.presence_of_all_elements_located((By.XPATH,
									 '//table[@id="bandListAlpha"]/tbody/tr')))

			bands = driver.find_elements_by_xpath('//table[@id="bandListAlpha"]/tbody/tr')

			for band in bands:
				try:
					band_dict = {}
					name = band.find_element_by_xpath('.//td/a').text
					ID = band.find_element_by_xpath('.//td/a').get_attribute('href').rsplit('/', 1)[-1]
					band_dict['name'] = name
					band_dict['ID'] = ID
					writer.writerow(band_dict.values())

				except UnicodeEncodeError:
					pass	

			wait_button = WebDriverWait(driver, 10)
			time.sleep(5)
			button = wait_button.until(EC.element_to_be_clickable((By.XPATH,
									   '//a[@class="next paginate_button"]')))

			button = driver.find_element_by_xpath('//a[@class="next paginate_button"]')
			button.click()

		except WebDriverException as e:
			print(e)
			driver.close()
			break