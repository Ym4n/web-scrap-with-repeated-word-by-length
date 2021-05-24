import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
repeated word by length limit
""" 

class Web_Scraper_module():
    def __init__(self,URLs):
        self.URLs =URLs
    
    def page_to_text(self,URL):
        # request html page
        try:
            page = requests.get(URL)
        except:
            return "URL does not exist"
        
        soup = BeautifulSoup(page.content, 'html.parser')
        all_text = soup.get_text(separator=' ')

        # cleaning raw data
        all_text = all_text.replace('\t',' ')
        all_text = all_text.replace('\n',' ')
        all_text = all_text.replace('\xa0',' ')

        all_words = all_text.split(' ')
        return all_words
    
    def Word_Sorting(self,all_words):
        # mapping words by Length and Quantity
        word_dict = {}
        word_dict = { 'Length':[] , 'Words':[] , 'Quantity':[] }
        
        for word in all_words:
            if (word==' ' or word==''):
                continue
            if (word in word_dict['Words']):
                index = word_dict['Words'].index(word)
                word_dict['Quantity'][index] += 1 
            else:
                word_dict['Words'].append(word) 
                word_dict['Quantity'].append(1)
                word_dict['Length'].append(len(word))

       
        # convert dict to table 
        df = pd.DataFrame.from_dict(word_dict)
        
        # get repeated word for each lenght with groups 
        groups = df.groupby(by=['Length'])
        idx= []
        for group in groups:
            if (group[0]==1):
                continue
            if (group[0]>15):
                break
            idx += [group[1].Quantity.idxmax()]

        return df.iloc[idx]

    def Run(self):
        text =[]
        for URL in self.URLs:
            text += self.page_to_text(URL)

        return self.Word_Sorting(text)
    
URLs = ['https://he.wikipedia.org/wiki','https://www.ynet.co.il/','http://www.talniri.co.il/']
test = Web_Scraper_module(URLs)
print(test.Run())
