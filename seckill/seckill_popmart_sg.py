#!/usr/bin/env python3
# encoding=utf-8


import os
import platform
from time import sleep
from random import choice
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

import seckill.settings as utils_settings
from utils.utils import get_useragent_data

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from config import global_config


# 不变量
MAX_RETRY_COUNT = 30
CHECKOUT_EMAIL = "james_huang@hotmail.com"
FIRST_NAME = "james"
LAST_NAME = "huang"
SHIPPING_ADDRESS = "Blk 123 Singapore"
UNIT_NUMBER = "#01-01"
POSTAL_CODE = "100100"
PHONE_NUMBER = "9999 9999" #中间需要空格
CARD_NUMBER = "1234 5678 1234 5678"
NAME_ON_CARD = "james huang"
CARD_EXPIRY_DATE = "01/99"
CARD_SECURITY_CODE = "000"


def default_chrome_path():

    driver_dir = getattr(utils_settings, "DRIVER_DIR", None)
    if platform.system() == "Windows":
        if driver_dir:
            return os.path.abspath(os.path.join(driver_dir, "chromedriver.exe"))

        raise Exception("The chromedriver drive path attribute is not found.")
    else:
        if driver_dir:
            return os.path.abspath(os.path.join(driver_dir, "chromedriver"))

        raise Exception("The chromedriver drive path attribute is not found.")



class ChromeDrive:

    def __init__(self, chrome_path=default_chrome_path(), seckill_time=None, password=None):
        self.chrome_path = chrome_path
        self.seckill_time = seckill_time
        self.seckill_time_obj = datetime.strptime(self.seckill_time, '%Y-%m-%d %H:%M:%S')
        self.password = password

    def start_driver(self):
        try:
            driver = self.find_chromedriver()
        except WebDriverException:
            print("Unable to find chromedriver, Please check the drive path.")
        else:
            return driver

    def find_chromedriver(self):
        try:
            driver = webdriver.Chrome(options=self.build_chrome_options())

        except WebDriverException:
            try:
                driver = webdriver.Chrome(options=self.build_chrome_options(),executable_path=self.chrome_path, chrome_options=self.build_chrome_options())


            except WebDriverException:
                raise

        # 设置全屏浏览器
        driver.maximize_window()
        return driver

    def build_chrome_options(self):
        """配置启动项"""
        chrome_options = webdriver.ChromeOptions()
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium - 20210105实验证明对于阿里淘宝来说没用，一样被识别出来了
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

        chrome_options.accept_untrusted_certs = True
        chrome_options.assume_untrusted_cert_issuer = True
        arguments = ['--no-sandbox', '--disable-impl-side-painting', '--disable-setuid-sandbox', '--disable-seccomp-filter-sandbox',
                     '--disable-breakpad', '--disable-client-side-phishing-detection', '--disable-cast',
                     '--disable-cast-streaming-hw-encoding', '--disable-cloud-import', '--disable-popup-blocking',
                     '--ignore-certificate-errors', '--disable-session-crashed-bubble', '--disable-ipv6',
                     '--allow-http-screen-capture', '--start-maximized','--ignore-ssl-errors'
                     ]
        for arg in arguments:
            chrome_options.add_argument(arg)
        chrome_options.add_argument(f'--user-agent={choice(get_useragent_data())}')
        return chrome_options

    def _fetch_item_page(self, item_url):
        if item_url:
            self.driver = self.start_driver()
            self.driver.get(item_url)
        else:
            print("Please input the login url.")
            raise Exception("Please input the login url.")

    def _keep_waiting(self, item_url):
        print("等待到点抢购...")
        while True:
            current_time = datetime.now()
            # 此处修判断
            if (self.seckill_time_obj.second - current_time.second) > 120:
                self.driver.get(item_url)
                print("每分钟刷新一次界面，防止登录超时...")
                sleep(60)
            else:
                print("抢购时间点将近，停止自动刷新，准备进入抢购阶段...")
                break
   
    def enter_input(self, input_box, value):
        input_box.clear()
        input_box.send_keys(value)
        assert value == input_box.get_attribute("value"), "%s没有被填对，变成了%s" % (value, input_box.get_attribute("value"))

    def sec_kill(self, item_url: str="https://popmart.sg/collections/pre-order/products/pre-order-pop-mart-yoki-rose-prince"):
        self._fetch_item_page(item_url)
        self._keep_waiting(item_url)
                
        submit_succ = False
        retry_count = 0

        while True:
            now = datetime.now()
            if now >= self.seckill_time_obj:
                print(f"开始抢购, 尝试次数： {str(retry_count)}")
                retry_count = retry_count + 1
                if submit_succ:
                    print("订单已经提交成功，无需继续抢购...")
                    break
                if retry_count > MAX_RETRY_COUNT:
                    print("重试抢购次数达到上限，放弃重试...")
                    break
                
                add_to_cart_button = self.driver.find_element_by_name("add")
                if add_to_cart_button and add_to_cart_button.is_enabled():
                    try:
                        add_to_cart_button.click()
                        print("已经点击add to cart按钮...")
                    except Exception as e:
                        print("add to cart失败, 重试...")
                        print(e)
                        continue
                    
                    while True:
                        if submit_succ:
                            break
                        
                        checkout_button = self.driver.find_element_by_name("checkout")
                        if checkout_button and checkout_button.is_enabled():
                            try:
                                checkout_button.click()
                                print("已经点击checkout按钮...")
                                # TODO: 这边经常没有点击成功，需要检查
                            except Exception as e:
                                print("checkout失败, 重试...")
                                print(e)
                                continue
                            
                            while True:
                                try:
                                    self.driver.find_element_by_id("checkout_email") # 等待checkout界面加载
                                    break
                                except Exception as e:
                                    print("等待checkout界面加载...")
                                    sleep(0.01)
                            self.enter_input(self.driver.find_element_by_id("checkout_email"), CHECKOUT_EMAIL)
                            self.enter_input(self.driver.find_element_by_id("checkout_shipping_address_first_name"), FIRST_NAME)
                            self.enter_input(self.driver.find_element_by_id("checkout_shipping_address_last_name"), LAST_NAME)
                            self.enter_input(self.driver.find_element_by_id("checkout_shipping_address_address1"), SHIPPING_ADDRESS)
                            self.enter_input(self.driver.find_element_by_id("checkout_shipping_address_address2"), UNIT_NUMBER)
                            self.enter_input(self.driver.find_element_by_id("checkout_shipping_address_zip"), POSTAL_CODE)
                            self.enter_input(self.driver.find_element_by_id("checkout_shipping_address_phone"), PHONE_NUMBER)
                            
                            while True:
                                if submit_succ:
                                    break
                        
                                continue_button = self.driver.find_element_by_id("continue_button")
                                if continue_button and continue_button.is_enabled():
                                    continue_button.click()
                                    print("已经点击continue to shipping按钮")
                                    
                                    try:
                                        print("购物车总应付：%s" % self.driver.find_elements_by_xpath('.//span[@class = "payment-due__price"]')[0].text)
                                    except Exception as e:
                                        print(e)
                                        print("没发现购物车总应付，直接继续去付款")
                                    
                                    while True:
                                        if submit_succ:
                                            break
                                    
                                        continue_button = self.driver.find_element_by_id("continue_button")
                                        if continue_button and continue_button.is_enabled():
                                            continue_button.click()
                                            print("已经点击continue to payment按钮")
                                            
                                            # TODO: 这边的iframe逻辑还需要更新
                                            self.driver.switch_to.frame(self.driver.find_element_by_xpath(".//iframe[@title='Field container for: Card number']"))
                                            self.enter_input(self.driver.find_element_by_id("number"), CARD_NUMBER)
                                            self.driver.switch_to.defaultContent()
                                            self.driver.switch_to.frame(self.driver.find_element_by_xpath(".//iframe[@title='Field container for: Name on card']"))
                                            self.enter_input(self.driver.find_element_by_id("name"), NAME_ON_CARD)
                                            self.driver.switch_to.defaultContent()
                                            self.driver.switch_to.frame(self.driver.find_element_by_xpath(".//iframe[@title='Field container for: Expiration date (MM / YY)']"))
                                            self.enter_input(self.driver.find_element_by_id("expiry"), CARD_EXPIRY_DATE)
                                            self.driver.switch_to.defaultContent()
                                            self.driver.switch_to.frame(self.driver.find_element_by_xpath(".//iframe[@title='Field container for: Security code"))
                                            self.enter_input(self.driver.find_element_by_id("verification_value"), CARD_SECURITY_CODE)
                                            self.driver.switch_to.defaultContent()
                                        
                                            click_submit_times = 0
                                            while True:
                                                try:
                                                    continue_button = self.driver.find_element_by_id("continue_button")
                                                    if click_submit_times < 10 and continue_button.is_enabled():
                                                        continue_button.click()
                                                        print("已经点击提交订单按钮")
                                                        submit_succ = True
                                                        break
                                                    else:
                                                        print("提交订单失败...大于10次，直接就失败吧。试了也没用了。 ")
                                                        return
                                                except Exception as e:
                                                    # TODO 待优化，这里可能需要返回购物车页面继续进行,也可能结算按钮点击了但是还没有跳转
                                                    #     self.driver.find_element_by_link_text('我的购物车').click()
                                                    print("没发现提交按钮, 页面未加载, 重试...")
                                                    click_submit_times = click_submit_times + 1
                                                    sleep(0.01)
                                        else:
                                            print("没发现有效continue to payment按钮, 页面未加载, 重试...")
                                            sleep(0.01)
                                else:
                                    print("没发现有效continue to shipping按钮, 页面未加载, 重试...")
                                    sleep(0.01)
                        else:
                            print("没发现有效check out按钮, 页面未加载, 重试...")
                            sleep(0.01)
                else:
                    print("没发现有效add to cart按钮, 页面未加载, 重试...")
            else:
                sleep(0.1)
