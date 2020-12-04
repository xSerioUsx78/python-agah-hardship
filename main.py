import time
import string
import random
import pytesseract
import jdatetime
import multiprocessing as mp
from selenium import webdriver
from PIL import Image
from decouple import config
from timer import convert_to_sec, generate_time

USERNAME = config('USERNAME')
PASSWORD = config('PASSWORD')
URL = config('URL')


def create_random_name():
    return ''.join(random.choices(string.digits + string.ascii_letters, k=10))


class AgahHardship:

    def __init__(self):
        options = webdriver.chrome.options.Options()
        options.binary_location = '/opt/apps/cn.google.chrome/files/chrome'
        self.driver = webdriver.Chrome(
            executable_path='ChromeDriver/chromedriver', options=options)
        self.url = URL
        self.login(USERNAME, PASSWORD)
        self.search_take_stock('آریا')
        self.choose_your_plan('buy')

    def getting_captcha_number(self, captcha_src):

        location = captcha_src.location
        size = captcha_src.size
        image_name = f'img_{create_random_name()}.png'
        self.driver.save_screenshot(image_name)

        image = Image.open(image_name)

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        buttom = location['y'] + size['height']

        image = image.crop((left, top, right, buttom))
        image.save(image_name,  'png')
        captcha_number = pytesseract.image_to_string(image)
        return captcha_number

    def login(self, username, password):
        self.driver.get(self.url)
        time.sleep(2)

        self.driver.find_element_by_name('username').send_keys(username)
        self.driver.find_element_by_name(
            'password').send_keys(password)
        captcha_src = self.driver.find_element_by_id(
            "imgcpatcha")
        captcha_input = self.driver.find_element_by_name('captcha')
        captcha_input.send_keys(self.getting_captcha_number(captcha_src))
        time.sleep(1)

    def search_take_stock(self, name):
        self.driver.find_element_by_xpath(
            "//div[contains(@class, 'search-part')]/span"
        ).click()
        time.sleep(1)
        self.driver.find_element_by_xpath(
            "//div[contains(@select, 'getInstrument(item)')]/input[contains(@type, 'search')]"
        ).send_keys(name)
        time.sleep(1)
        self.driver.find_elements_by_xpath(
            "//tr[contains(@instrument-item, 'instrument')]"
        )[0].click()
        time.sleep(1)

    def get_price(self, price):
        price_input = self.driver.find_element_by_xpath(
            "//input[contains(@ng-model, 'order.Price')]")
        price_input.clear()
        time.sleep(1)
        price_input.send_keys(price)
        time.sleep(1)

    def get_mass(self, mass):
        mass_input = self.driver.find_element_by_xpath(
            "//input[contains(@ng-model, 'order.Quantity')]")
        mass_input.clear()
        time.sleep(1)
        mass_input.send_keys(mass)
        time.sleep(1)

    def choose_your_order(self, price_choice):
        if price_choice == 'بالاترین نقطه':
            self.driver.find_element_by_xpath(
                "//p[contains(@class, 'maxQuantity')]/span[contains(@ng-click, 'setPrice(selectInstrument.UpperPriceThreshold)')]"
            ).click()
            time.sleep(1)
            self.get_mass('100')
        elif price_choice == 'پایین ترین نقطه':
            self.driver.find_element_by_xpath(
                "//p[contains(@class, 'maxQuantity')]/span[contains(@ng-click, 'setPrice(selectInstrument.LowerPriceThreshold)')]"
            ).click()
            time.sleep(1)
            self.get_mass('200')
        elif price_choice == 'وارد کردن بصورت دستی':
            self.get_price('180,505')
            self.get_mass('100')
        time.sleep(1)

    def buy(self):
        for i in range(self.get_time_request(2)):
            self.driver.find_element_by_class_name('btn-buy').click()
            if i > 0:
                time.sleep(5)
            elif i < 1:
                time.sleep(1)
            self.choose_your_order('پایین ترین نقطه')
            self.driver.find_element_by_xpath(
                "//button[contains(@class, 'Buy')]").click()
            time.sleep(1)
            if i > 0:
                pass
            elif i < 1:
                # self.get_time(generate_time('20:20:00'))
                self.get_time('02:12:00')
            self.driver.find_element_by_xpath(
                "//button[contains(@class, 'btnAccept')]").click()
            time.sleep(1)

    def sell(self):
        for i in range(self.get_time_request(2)):
            self.driver.find_element_by_class_name('btn-Sell').click()
            if i > 0:
                time.sleep(5)
            elif i < 1:
                time.sleep(1)
            self.choose_your_order('پایین ترین نقطه')
            self.driver.find_element_by_xpath(
                "//button[contains(@ng-click, 'order.sell(true, $event)')]").click()
            time.sleep(1)
            if i > 0:
                pass
            elif i < 1:
                # self.get_time(generate_time('20:20:00'))
                self.get_time('23:18:50')
            self.driver.find_element_by_xpath(
                "//button[contains(@class, 'btnAccept')]").click()
            time.sleep(1)

    def choose_your_plan(self, choice):
        if choice == 'buy':
            self.buy()
        elif choice == 'sell':
            self.sell()
        else:
            raise TypeError('you are dumbass')

    def get_time(self, time_):
        sep_time = time_.replace(':', '')
        # sep_time = time_
        now = jdatetime.datetime.now()
        timer = convert_to_sec(now, sep_time)
        if timer < 0:
            raise ValueError('choose right time baby')
        else:
            time.sleep(timer)

    def get_time_request(self, time):
        return time


if __name__ == "__main__":
    AgahHardship()
