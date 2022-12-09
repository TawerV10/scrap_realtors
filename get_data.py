from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
import time
import csv

filename = 'trial.csv'

def create_csv():
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'name', 'title', 'office', 'address', 'phone', 'link', 'instagram', 'facebook', 'twitter', 'linkedin'
        ])

def collect_data_sel(driver):
    realtors = driver.find_elements(By.XPATH, '//span[@id="realtorCard"]')
    for i in range(0, len(realtors)):
        try:
            link = driver.find_elements(By.XPATH, '//a[@class="realtorCardDetailsLink realtorDetailsLink"]')[i].get_attribute('href')
        except:
            link = ''
        try:
            name = driver.find_elements(By.XPATH, '//span[@class="realtorCardName"]')[i].text.strip()
        except:
            name = ''
        try:
            title = driver.find_elements(By.XPATH, '//div[@class="realtorCardTitle"]')[i].text.strip()
        except:
            title = ''
        try:
            office = driver.find_elements(By.XPATH, '//div[@class="realtorCardOfficeName"]')[i].text.strip()
        except:
            office = ''
        try:
            address = driver.find_elements(By.XPATH, '//div[@class="realtorCardOfficeAddress"]')[i].text.strip()
        except:
            address = ''
        try:
            phone = driver.find_elements(By.XPATH, '//span[@class="realtorCardContactNumber TelephoneNumber"]')[i].text.strip()
        except:
            phone = ''

        print(f'{name} - {title} - {office} - {address} - {phone} - {link}')

        with open('trial.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                name, title, office, address, phone, link
            ])

def collect_data(html):
    soup = BeautifulSoup(html, 'lxml')

    realtors = soup.find_all('div', class_='realtorSearchResultCardCon')
    print(len(realtors))
    for realtor in realtors:
        try:
            link = 'https://www.realtor.ca' + realtor.find('a', class_='realtorCardDetailsLink realtorDetailsLink').get('href').strip()
        except:
            link = ''
        try:
            name = realtor.find('span', class_='realtorCardName').text.strip()
        except:
            name = ''
        try:
            title = realtor.find('div', class_='realtorCardTitle').text.strip()
        except:
            title = ''
        try:
            office = realtor.find('div', class_='realtorCardOfficeName').text.strip()
        except:
            office = ''
        try:
            address = realtor.find('div', class_='realtorCardOfficeAddress').text.strip()
        except:
            address = ''
        try:
            phone = realtor.find('span', class_='realtorCardContactNumber TelephoneNumber').text.strip()
        except:
            phone = ''
        try:
            instagram = realtor.find('a', class_='InstagramSocialLink').get('href').strip()
        except:
            instagram = ''
        try:
            facebook = realtor.find('a', class_='FacebookSocialLink').get('href').strip()
        except:
            facebook = ''
        try:
            twitter = realtor.find('a', class_='TwitterSocialLink').get('href').strip()
        except:
            twitter = ''
        try:
            linkedin = realtor.find('a', class_='LinkedInSocialLink').get('href').strip()
        except:
            linkedin = ''

        print(f'{name} - {title} - {office} - {address} - {phone} - {instagram} - {facebook} - {twitter} - {linkedin} - {link}')

        with open(filename, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                name, title, office, address, phone, link, instagram, facebook, twitter, linkedin
            ])

def run_browser():
    try:
        options = webdriver.ChromeOptions()
        options.binary_location = 'C:\Program Files\Google\Chrome Beta\Application\chrome.exe'

        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()

        page_count = 30
        for i in range(1, 5 + 1):
            driver.get(f'https://www.realtor.ca/realtor-search-results#city=london&page={i}&sort=11-A')
            time.sleep(1)
            driver.get_screenshot_as_file("screenshot.png")

            collect_data(driver.page_source)
            time.sleep(1)

            print(f'{i}/{page_count}')

    except Exception as ex:
        print(ex)
    finally:
        driver.stop_client()
        driver.close()
        driver.quit()

def main():
    t0 = time.time()
    create_csv()
    run_browser()
    print(time.time() - t0)

if __name__ == '__main__':
    main()
