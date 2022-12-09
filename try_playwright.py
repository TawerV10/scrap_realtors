from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import asyncio
import time
from pprint import pprint
import csv

filename = 'data.csv'

def create_csv():
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'name', 'title', 'office', 'address', 'phone', 'link', 'instagram', 'facebook', 'twitter', 'linkedin'
        ])

def collect_data(html):
    soup = BeautifulSoup(html, 'lxml')

    realtors = soup.find_all('div', class_='realtorSearchResultCardCon')
    print(realtors)
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

        # print(f'{name} - {title} - {office} - {address} - {phone} - {instagram} - {facebook} - {twitter} - {linkedin} - {link}')

        with open(filename, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                name, title, office, address, phone, link, instagram, facebook, twitter, linkedin
            ])

def scraper():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()

        page.goto('https://www.realtor.ca/')
        time.sleep(30)

        page_count = 30
        for i in range(1, page_count + 1):
            page.goto(f'https://www.realtor.ca/realtor-search-results#city=london&page={i}&sort=11-A')
            time.sleep(3)

            collect_data(page.content())

            print(f'{i}/{page_count}')

        browser.close()

def main():
    t0 = time.time()
    # create_csv()
    scraper()
    print(time.time() - t0)

if __name__ == '__main__':
    main()