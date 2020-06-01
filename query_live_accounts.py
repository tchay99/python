import urllib3
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import csv
""" Python script to check for live accounts from a list of corporate users"""

df = pd.read_excel(r'spreadsheet.xlsx') # we read the spreadsheet in a dataframe
names_series = df['email'].str.split(pat = "@").str[0] # we split the corporate email address and get username
names = names_series.tolist() # dropping names to iterable
writer = pd.ExcelWriter('results.xlsx', engine='xlsxwriter')

substring = "Do you have an account recovery code?" # If an account exists MS will ask for a recovery code

def get_text(soup): 
    """ Function to process html result of a request and strip out all garbage """
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
    return text    

def check_mailbox(name):
    """ Function to check a live mailbox - args: username """
    # First we build the url string
    # replace your domain.com with your domain in the URL string below
    url ="https://account.live.com/password/reset?wreply=https%3A%2F%2Flogin.live.com%2Flogin.srf%3Fwa%3Dwsignin1.0%26rpsnv%3D13%26ct%3D1561787618%26rver%3D7.0.6737.0%26wp%3DMBI_SSL%26wreply%3Dhttps%253a%252f%252foutlook.live.com%252fowa%252f%253fnlp%253d1%2526RpsCsrfState%253df91accaa-e96b-ee13-52ec-7bd10ae43fd1%26id%3D292841%26aadredir%3D1%26CBCXT%3Dout%26lw%3D1%26fl%3Ddob%252cflname%252cwld%26cobrandid%3D90015%26contextid%3D55D510099ED60F79%26bk%3D1561787619&id=292841&uiflavor=web&cobrandid=90015&uaid=b9cece3ccdc54586a6bd1347776f9f3c&mkt=EN-GB&lc=21514&bk=1561787619&mn=" + name + "%yourdomain.com"
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = bs(response.data, "lxml")
    # We call the url with a GET method to scrape the webpage
    text = get_text(soup) # we process the result with function get_text
    if -1 != text.find(substring): # if substring is found than we have an account!
        return True
    else:
        return False 

def __main__():
    while names: # iterating list with while & pop to preserve order
        name = names.pop(0)
        result = check_mailbox(name)
        has_mailbox.append(result)
        # We write the results to a csv file in the same order in which we iterate the list
        # That way we can concatenate the excel
        with open('processed.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerow([name,result])

if __name__ == "__main__":
    __main__()
