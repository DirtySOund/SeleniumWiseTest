import unittest
from selenium import webdriver

from faker import Faker

faker = Faker()


def random_user():
    return "INSERT INTO Customers (CustomerName, ContactName, City) " \
           "VALUES (\""+faker.first_name()+"\", \""+faker.last_name()+"\", \""+faker.city()+"\");"


class Variables:
    SQL_link = 'https://www.w3schools.com/sql/trysql.asp?filename=trysql_select_all'

    css_name = '#divResultSQL > div > table > tbody > tr:nth-child(50) > td:nth-child(3)'
    css_adress = '#divResultSQL > div > table > tbody > tr:nth-child(50) > td:nth-child(4)'
    css_list = '#divResultSQL > div > table > tbody > tr:nth-child(50)'

    sql_request = 'SELECT CustomerName, City FROM Customers WHERE city=\"London\";'
    css_num_records = '#divResultSQL > div > div'
    css_table = '.w3-table-all'

    sql_request_insert = \
        "INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country) VALUES " \
        "(\"Frodo Beggins\", \"Bilbo Beggens\", \"Buckland\", \"Shire\", \"0100101\", \"Middle-earth\")"
    sql_request_select_1 = 'SELECT * FROM Customers WHERE CustomerName=\"Frodo Beggins\";'

    sql_request_update = \
        "UPDATE Customers SET CustomerName = \"Aragorn\", ContactName = \"Arahorn\", Address = \"BigStreeet\", " \
        "City = \"Kiev\", PostalCode = \"22222\", Country = \"Brazil\" WHERE CustomerID = \"10\";"
    sql_request_select_2 = 'SELECT * FROM Customers WHERE CustomerName=\"Aragorn\";'


class Page_configs(unittest.TestCase):
    def driver(self):
        self.driver = webdriver.Chrome()

    def click_run_sql(self):
        driver = self.driver
        driver.find_element_by_css_selector('.w3-green.w3-btn').click()
        driver.implicitly_wait(2)

    def restore_db(self):
        driver = self.driver
        driver.find_element_by_id('restoreDBBtn').click()
        driver.switch_to.alert.accept()
        driver.implicitly_wait(2)

    def find_css(self, selector):
        driver = self.driver
        driver.find_element_by_css_selector(selector)
