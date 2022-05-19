from selenium.webdriver.remote import webelement
from selenium.webdriver.common.by import By

# class to arrange a report for results


class BookingReport:
    def __init__(self, search_results: webelement):
        self.search_results = search_results
        self.deals_results = self.result_boxes()

    def result_boxes(self):
        return self.search_results.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')

    def pull_deal_results(self):
        collection_results = []

        for deal in self.deals_results:
            try:

                hotel_title = deal.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text

                hotel_score = deal.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]').text

                hotel_price = deal.find_element(By.CSS_SELECTOR,
                                            'div[data-testid="price-and-discounted-price"]').find_element(By.TAG_NAME,
                                                                                                          'span').text

                hotel_link = deal.find_element(By.CSS_SELECTOR,
                                                                '[data-testid="title-link"]').get_attribute('href')

                collection_results.append([hotel_title, hotel_score, hotel_price, hotel_link])

            except:
                continue

        return collection_results



