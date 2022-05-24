import time
import csv

import pandas as pd
import os

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

bacheloe_link = 'https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors'

class ParsingBot():
    def __init__(self):
        self.data_row = []

        self.name_of_columns = []
        self.id_list = []
        self.name_list = []
        self.price_list_1 = []
        self.price_list_2 = []
        self.percent_lsit = []

    def open_site(self):
        self.driver = uc.Chrome()
        self.driver.get(bacheloe_link)
        self.wait()
        self.collect_header_row_names()

    def collect_header_row_names(self):
        '''Accept cookies'''
        try:
            self.driver.find_element(By.ID, value='onetrust-accept-btn-handler').click()
        except:
            quit()
            self.wait()
            self.wait()
            self.open_site()

        data_table = self.driver.find_element(By.CLASS_NAME, value='data-table')
        data_table_row = data_table.find_elements(By.CLASS_NAME, value='data-table__row')
        table_header = data_table.find_elements(By.CLASS_NAME, value='data-table__header')

        '''Gets the name of headers and appends it to the headers list'''
        for header in table_header:
            if len(header.text) < 1:
                pass
            else:
                self.name_of_columns.append(header.text)

        print(self.name_of_columns)


        r'''Create an empty list, then iterate over the data_table_row.
        replace \n with a # symbol to make the separating process easier'''
        new_list = []
        for x in data_table_row:
            new_list.append(x.text.replace('\n', '#'))

        '''Iterate over in new_list and collect 
        the necessary data using slice'''
        for item in new_list:
            id = item.split('#')[0]
            name = item.split('#')[1]
            price_1 = item.split('#')[2]
            percent = price_1.split(' ')[2]

            '''Remove percent from price'''
            price_2 = price_1.split(' ')[:2]

            '''Separates two price tag'''
            sub_pricce_1 = price_2[0]
            sub_pricce_2 = price_2[1]

            '''Appends each item to the correspponding list'''
            self.id_list.append(id)
            self.name_list.append(name)
            self.price_list_1.append(sub_pricce_1)
            self.price_list_2.append(sub_pricce_2)
            self.percent_lsit.append(percent)

        '''Manually rewrite last items ID from 24 to 25'''
        self.id_list[-1] = '25'

        '''Creating a new list - list_of_collection,
        and add the collected item names in order'''
        list_of_collection = []
        for each in range(len(self.id_list)):
            list_of_collection.append([
                self.id_list[each],
                self.name_list[each],
                self.price_list_1[each],
                self.price_list_2[each],
                self.percent_lsit[each]
            ])

        self.save_data(list_of_collection)

        '''Start reading (saved) file'''
        self.read_file()

    def save_data(self, list_of_collection):
        with open('data_bank.csv', 'w', encoding='UTF8', newline='') as file:
            write = csv.writer(file)
            write.writerow(self.name_of_columns)
            write.writerows(list_of_collection)

    def read_file(self):
        df = pd.read_csv('data_bank.csv')
        print(df.to_string())

        highest_early_carreer_pay = df.sort_values('Early Career Pay', ascending=False)
        sorted = highest_early_carreer_pay[['Major', 'Early Career Pay']]
        print(sorted.to_string())

    def wait(self):
        time.sleep(2)
        self.driver.implicitly_wait(2)


if __name__ == '__main__':
    parser_bot = ParsingBot()
    '''See if the file exists already and if doesnt, 
    then start the parsing process and collect + save the necessary data'''
    if os.path.isfile('data_bank.csv'):
        parser_bot.read_file()
    else:
        parser_bot.open_site()
    time.sleep(1000)
