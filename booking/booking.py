from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from booking import constants as cons
import os
from booking.booking_filteration import BookingFilteration
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from booking.booking_report import BookingReport
from prettytable import PrettyTable

# the main class for automation booking bot


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\seleniumdriver", tear_down=False):
        self.driver_path = driver_path
        os.environ['PATH'] = self.driver_path
        self.tear_down = tear_down
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        super(Booking, self).__init__(options=options)
        self.implicitly_wait(20)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.tear_down:
            self.quit()

    def land_page(self):
        self.get(cons.LAND_URL)

    def change_currency(self, currency=cons.CURRENCY):
        btn = self.find_element(By.CSS_SELECTOR, 'button[data-tooltip-text="Choose your currency"]')
        if not currency in btn.text:
            btn.click()
            selected_currency = self.find_element(By.CSS_SELECTOR,
                                                  f'a[data-modal-header-async-url-param*="selected_currency={currency}"]')
            selected_currency.click()

    def search_dest(self, city=cons.CITY):
        city_to_go = self.find_element(By.ID, 'ss')
        city_to_go.clear()
        city_to_go.send_keys(city)
        ignored_exceptions = (NoSuchElementException, TimeoutException)
        option = WebDriverWait(self, 20, ignored_exceptions).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li[data-i="0"]') ))
        option.click()

    def check_date(self, check_in_date=cons.IN_DATE, check_out_date=cons.OUT_DATE):
        select_in_date = self.find_element(By.CSS_SELECTOR, f'td[data-date="{check_in_date}"]')
        select_in_date.click()
        select_out_date = self.find_element(By.CSS_SELECTOR, f'td[data-date="{check_out_date}"]')
        select_out_date.click()

    def select_travel_options(self, adults=cons.ADULTS, children=cons.CHILDREN, rooms=cons.ROOMS):
        main = self.find_element(By.ID, "xp__guests__toggle")
        main.click()
        adults_count = int(main.find_element(By.CSS_SELECTOR, 'span[data-adults-count]').text.split()[0])

        children_count = int(main.find_element(By.CSS_SELECTOR, 'span[data-children-count]').text.split()[0])

        rooms_count = int(main.find_element(By.CSS_SELECTOR, 'span[data-room-count]').text.split()[0])

        if adults != adults_count:
            if adults > adults_count:
                diff = adults - adults_count
                btn_increase = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Increase number of Adults"]')
                for i in range(diff):
                    btn_increase.click()
            else:
                diff = adults_count - adults
                btn_decrease = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Decrease number of Adults"]')
                for i in range(diff):
                    btn_decrease.click()

                if children != children_count:
                    if children > children_count:
                        diff = children - children_count
                        btn_increase = self.find_element(By.CSS_SELECTOR,
                                                         'button[aria-label="Increase number of Children"]')
                        for i in range(diff):
                            btn_increase.click()
                    else:
                        diff = children_count - children
                        btn_decrease = self.find_element(By.CSS_SELECTOR,
                                                         'button[aria-label="Decrease number of Children"]')
                        for i in range(diff):
                            btn_decrease.click()

                if rooms != rooms_count:
                    if rooms > rooms_count:
                        diff = rooms - rooms_count
                        btn_increase = self.find_element(By.CSS_SELECTOR,
                                                         'button[aria-label="Increase number of Rooms"]')
                        for i in range(diff):
                            btn_increase.click()
                    else:
                        diff = rooms_count - rooms
                        btn_decrease = self.find_element(By.CSS_SELECTOR,
                                                         'button[aria-label="Decrease number of Rooms"]')
                        for _ in range(diff):
                            btn_decrease.click()

                search_btn = self.find_element(By.CLASS_NAME, 'sb-searchbox__button')
                search_btn.click()

    def apply_filters(self):
        booking_filter = BookingFilteration(driver=self)
        booking_filter.filter_stars(5)
        booking_filter.sort_results()

    def display_report(self):
        search_results = self.find_element(By.ID, "search_results_table")
        report = BookingReport(search_results)
        results_data = report.pull_deal_results()
        table = PrettyTable(field_names=['title', 'score', 'price', 'link'])
        table.add_rows(results_data)
        print(table)








