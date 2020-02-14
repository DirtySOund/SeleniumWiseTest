import unittest
from selenium import webdriver

from tests import requests
from tests.requests import faker


class SQL_tests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(requests.Variables.SQL_link)

    def test_01_search_customer(self):
        # setUP [Restore DB and Show all Customers]
        d = self.driver
        requests.Page_configs.restore_db(self)
        requests.Page_configs.click_run_sql(self)

        # Search ContactName and Address
        # Type assertion №1
        assert d.find_element_by_css_selector(requests.Variables.css_name).text == 'Giovanni Rovelli'
        assert d.find_element_by_css_selector(requests.Variables.css_adress).text == 'Via Ludovico il Moro 22'

        # Type assertion №2
        assert d.find_element_by_css_selector(requests.Variables.css_list).text.count(
            'Giovanni Rovelli Via Ludovico il Moro 22')

    def test_02_search_city(self):
        # setUP [Restore DB]
        d = self.driver
        requests.Page_configs.restore_db(self)

        # Input custom SQL request
        d.execute_script("window.editor.setValue('" + requests.Variables.sql_request + "')")
        requests.Page_configs.click_run_sql(self)

        # Check results:
        assert d.find_element_by_css_selector(requests.Variables.css_num_records).text == 'Number of Records: 6'
        assert d.find_element_by_css_selector(requests.Variables.css_table).text.count('London') == 6

    def test_03_input_new_customer(self):
        # setUP [Restore DB]
        d = self.driver
        requests.Page_configs.restore_db(self)

        # Input custom SQL request with new Customer
        d.execute_script("window.editor.setValue('" + requests.Variables.sql_request_insert + "')")
        requests.Page_configs.click_run_sql(self)

        # Find new Customer
        d.execute_script("window.editor.setValue('" + requests.Variables.sql_request_select_1 + "')")
        requests.Page_configs.click_run_sql(self)

        # Check results:
        assert d.find_element_by_css_selector('#divResultSQL > div > div').text == 'Number of Records: 1'
        assert d.find_element_by_css_selector('.w3-table-all').text.count('Shire') == 1

    def test_04_update_any_customer(self):
        # setUP [Restore DB]
        d = self.driver
        requests.Page_configs.restore_db(self)

        # Update custom SQL request for exist Customer
        d.execute_script("window.editor.setValue('" + requests.Variables.sql_request_update + "')")
        requests.Page_configs.click_run_sql(self)

        # Find updated Customer
        d.execute_script("window.editor.setValue('" + requests.Variables.sql_request_select_2 + "')")
        requests.Page_configs.click_run_sql(self)

        # Check results:
        assert d.find_element_by_css_selector('#divResultSQL > div > div').text == 'Number of Records: 1'
        assert d.find_element_by_css_selector('.w3-table-all').text.count(
            '10 Aragorn Arahorn BigStreeet Kiev 22222 Brazil') == 1

    def test_05_add_random_user_after_delete_his(self):
        # setUP [Restore DB]
        d = self.driver
        requests.Page_configs.restore_db(self)

        # Add random customer to DB
        config = requests.random_user()
        d.execute_script("window.editor.setValue('" + config + "')")
        requests.Page_configs.click_run_sql(self)

        # Find him
        d.execute_script("window.editor.setValue("
                         "'SELECT * FROM Customers WHERE CustomerName=\""+faker.first_name()+"\";')")
        requests.Page_configs.click_run_sql(self)

        # ... and delete
        d.execute_script("window.editor.setValue("
                         "'DELETE FROM Customers WHERE CustomerName=\"" + faker.first_name() + "\";')")
        requests.Page_configs.click_run_sql(self)

        # Check results:
        d.execute_script("window.editor.setValue("
                         "'SELECT * FROM Customers WHERE CustomerName=\"" + faker.first_name() + "\";')")
        requests.Page_configs.click_run_sql(self)
        assert d.find_element_by_css_selector('#divResultSQL > div').text == 'No result.'

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
