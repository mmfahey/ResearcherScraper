'''
Web-scraper for Reasearcher, an app that is used to aggregate scientific 
literature and find papers you may be interested in reading. This version
requires that the Researcher account is linked to a Facebook account.

Once the script has signed into the users account, it locates the saved papers
and bins them by publisher. Each publisher has a different loop for locating
the pdf and then downloading the pdf to a specified folder. Some publishers have 
tricky captchas, so those are just taken the url of and opened in a new tab.

Current implemented publishers include: ACS, RSC, PNAS, Nature, Wiley, IOP, DOI, 
AIP, but others will be added as needed.
'''

from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

import os

load_dotenv()

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", "G:\\My Drive\\Literature\\Papers2Read\\09.16.21")
fp.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
fp.set_preference("pdfjs.disabled", True)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

opts = Options()
#opts.headless = True

driver = webdriver.Firefox(firefox_profile = fp, options = opts)

driver.get('https://www.researcher-app.com/login')
sleep(5)
driver.find_element_by_css_selector('button.ModalComponents__Button-sc-niweq8-0:nth-child(3)').click()

win = driver.window_handles
main_page = win[0]
login_page = win[1]
driver.switch_to.window(login_page)

sleep(5)

username_box = driver.find_element_by_id('email') 
username_box.send_keys(os.environ.get('RESEARCHER_ID'))   
password_box = driver.find_element_by_id('pass') 
password_box.send_keys(os.environ.get('RESEARCHER_PASS')) 
login_box = driver.find_element_by_id('loginbutton') 
login_box.click() 

driver.switch_to.window(main_page)

sleep(10)

driver.get('https://www.researcher-app.com/library')

sleep(10)

elems = driver.find_elements_by_tag_name('a')

acspapers = []
rscpapers = []
aippapers = []
arxivpapers = []
naturepapers = []
pnaspapers = []
frontierpapers = []
medrxivpapers = []
miscpapers = []
non_downloadable = []
papers = []

for elem in elems:
    href = elem.get_attribute('href')
    print(href)
    if href is not None:
        if 'researcher' not in href:
            if 'acs' in href:
                acspapers.append(href)
                papers.append(href)
            elif 'rsc' in href:
                rscpapers.append(href)
                papers.append(href)
            elif 'pnas' in href:
                pnaspapers.append(href)
                papers.append(href)
            elif 'doi.org' in href:
                non_downloadable.append(href)
                papers.append(href)
            elif 'wiley' in href:
                non_downloadable.append(href)
                papers.append(href)
            elif 'iop' in href:
                non_downloadable.append(href)
                papers.append(href)
            elif 'aip' in href:
                aippapers.append(href)
                papers.append(href)
            elif 'arxiv' in href:
                arxivpapers.append(href)
                papers.append(href)
            elif 'nature' in href:
                naturepapers.append(href)
                papers.append(href)
            elif 'frontier' in href:
                frontierpapers.append(href)
                papers.append(href)
            elif 'medrxiv' in href:
                medrxivpapers.append(href)
                papers.append(href)
            else:
                miscpapers.append(href)
                papers.append(href)

for paper in acspapers:
    doi = paper.split('/')[4:]
    pdf = 'https://pubs.acs.org/doi/pdf/' + '/'.join(doi)
    try:
        driver.set_page_load_timeout(5)
        driver.get(pdf)
    except TimeoutException:
        pass

for paper in rscpapers:
    try:
        driver.set_page_load_timeout(5)
        driver.get(paper)
    except TimeoutException:
        pass

for paper in aippapers:
    try:
        driver.set_page_load_timeout(5)
        driver.get(paper)
    except TimeoutException:
        pass

for paper in arxivpapers:
    try:
        driver.set_page_load_timeout(5)
        driver.get(paper)
    except TimeoutException:
        pass

for paper in naturepapers:
    try:
        driver.set_page_load_timeout(5)
        driver.get(paper)
    except TimeoutException:
        pass

for paper in pnaspapers:
    try:
        driver.set_page_load_timeout(5)
        driver.get(paper)
    except TimeoutException:
        pass

for paper in frontierpapers:
    try:
        driver.set_page_load_timeout(5)
        driver.get(paper)
    except TimeoutException:
        pass

for paper in medrxivpapers:
    try:
        driver.set_page_load_timeout(5)
        driver.get(paper)
    except TimeoutException:
        pass

print(len(papers))

with open('G:\\My Drive\\Literature\\Papers2Read\\09.16.21\\non_downloadble.txt', 'a') as writer:
    for paper in non_downloadable:
        writer.write(f'{paper}\n')

with open('G:\\My Drive\\Literature\\Papers2Read\\09.16.21\\test.txt', 'a') as writer:
    for paper in papers:
        writer.write(f'{paper}\n')

print(f'papers that were uncategorized {miscpapers}')
driver.get('https://www.researcher-app.com/library')
sleep(10)
close = driver.find_elements_by_css_selector('div.FeedCardBasic___StyledDiv8-n2e83z-7')
print(len(close))
while len(close) != 0:
    sleep(5)
    close = driver.find_elements_by_css_selector('div.FeedCardBasic___StyledDiv8-n2e83z-7')
    print(len(close))
    for x in range(len(close)):
        driver.find_element_by_xpath(f'/html/body/div[4]/div[3]/ul/li[2]').click()
driver.close()


