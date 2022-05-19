from selenium.webdriver.common.by import By

# class for add filterations

class BookingFilteration:
    def __init__(self, driver):
        self.driver = driver

    def filter_stars(self, *stars):
        stars_group = self.driver.find_element(By.CSS_SELECTOR, 'div[data-filters-group="class"]')
        stars_elements = stars_group.find_elements(By.CSS_SELECTOR, '*')
        for star in stars:
            for star_element in stars_elements:
                if star_element.get_attribute('data-filters-item') == "class:class=" + str(star):
                    star_element.click()


    def sort_results(self):
        element = self.driver.find_element(By.CSS_SELECTOR, 'li[data-id="price"]')
        element.click()
