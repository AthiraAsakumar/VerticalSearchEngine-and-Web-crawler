import pandas as pd
from requests import get 
from bs4 import BeautifulSoup as soup
import warnings
warnings.filterwarnings('ignore')

url = 'https://pureportal.coventry.ac.uk/en/organisations/coventry-university/persons/?filter=Computational+Science+and+Mathematical+Modelling'
src_url= get(url)
html_txt = soup(src_url.text, 'html.parser')
pub_links_url = []

for heading in html_txt.find_all('h3', class_='title'):
    anchor_with_link = heading.find('a')
    web_link = anchor_with_link['href']
    pub_links_url.append(web_link)

pagestotal = 'https://pureportal.coventry.ac.uk/en/organisations/coventry-university/persons/?filter=Computational+Science+and+Mathematical+Modelling&page='


details_map = []

for page in range(1, 2):
    url_page = pagestotal + str(page)
    res_page = get(url_page)
    html_txt1 = soup(res_page.text, 'html.parser')
    
    title = 'title'
    for heading1 in html_txt1.find_all("h3", class_=title):
        anchor_with_link1 = heading1.find('a')
        link1 = anchor_with_link1.attrs['href']
        details_map.append(link1)

pub_links_url = pub_links_url + details_map

publications_c = []

for url_conference_journal in pub_links_url:
    conference_journal_page = get(url_conference_journal)
    html_content = conference_journal_page.text
    page = soup(html_content, "html.parser")
    for heading in page.find_all('h3', class_ ='title'): 
        path_url= heading.find('a')
        url_conference_journal= path_url['href']
        pub_journal='https://pureportal.coventry.ac.uk/en/publications/'
        if pub_journal not in url_conference_journal:
          continue
        publications_c.append(url_conference_journal)
        
publications_c1= []
publications= []

for url_art in publications_c:
    try:
      journal_content = get(url_art)
      html_journal_content = journal_content.text
      h_txt2 = soup(html_journal_content, "html.parser")
      row_parse= 'row'
      render_page='rendering'
      for heading in h_txt2.findAll('div', class_=row_parse):
        found_div= heading.findChild('div', class_= render_page)
        title1 = found_div.find('h1')
        publications_c1.append(title1.text)
      relations='relations persons'
      for heading in h_txt2.findAll('p', class_= relations):
          text= heading.findChild('span').text
          publications.append(text)
    except:
      pass

print(publications)

min_val=min([len(publications_c1),len(publications),len(publications_c)])
coventry_df = pd.DataFrame({'Title':publications_c1[:min_val], 'Authors':publications[:min_val], 'Publication Link':publications_c[:min_val] })

coventry_df['id'] = list(range(1, len(coventry_df) + 1))

coventry_df.to_csv('publicationurls.csv',index=False)
