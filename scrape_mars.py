from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from IPython.display import display_html
import pandas as pd


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

# # Latest News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    titles = []
    paras = []
    lnks = []

    for x in soup.find_all('div', class_="list_text"):
        title = x.find('div', class_="content_title")
        par = x.find('div', class_="article_teaser_body")
        link = x.a['href']
        titles.append(title.text)
        paras.append(par.text)
        lnks.append(link)

    news = []
    if len(titles) > 4:
        max_rng = 4
    else:
        max_rng=len(titles)
    for x in range(0, max_rng):
        news.append({'title':titles[x], 'text':paras[x], '_url':"https://mars.nasa.gov" + lnks[x]})
    
# # Featured Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=mars&category=featured#submit/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    first_slide = soup.find('li', class_='slide').a['data-fancybox-href']

    featured_image_url = "https://www.jpl.nasa.gov" + first_slide

# # Background Image
    bgImage = soup.find_all(attrs={"data-title": "A Fresh Crater near Sirenum Fossae"})[0]['data-fancybox-href']
    bg_url = "https://www.jpl.nasa.gov" + bgImage

# # Latest Weather
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    tweets = soup.find_all('div', class_='content')

    marsWx_tweets = []
    for tw in tweets:
        if tw.a['href'] == "/MarsWxReport" :
            marsWx_tweets.append(tw)

    wx = marsWx_tweets[0].find('p', class_='tweet-text').get_text().replace('\n', ' ')
    mars_weather = wx

# # Mars Facts
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    table = soup.find_all('table', id="tablepress-mars")[0]

    table = f"""{table}"""
    display_html(table, raw=True)

    dfs = pd.read_html(table)
    tbl = dfs[0]
    tbl = tbl.set_index(0)

    html_table = tbl.to_html()
    html_table = html_table.replace('\n', '')

    tbl_strgs = html_table.split("""  <thead>    <tr style="text-align: right;">      <th></th>      <th>1</th>    </tr>    <tr>      <th>0</th>      <th></th>    </tr>  </thead>""")
    
    html_table = tbl_strgs[0]+tbl_strgs[1]
    html_table = html_table.replace("""class="dataframe">""", """class="dataframe table-hover table-light table-borderless">""")

# # Hemisphere Images
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars/"
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')

    images = soup.find_all('div', class_='item')

    lnks = [images[x].a['href'] for x in range(0, len(images))]
    
    image_links = []
    for x in lnks:
        url = 'https://astrogeology.usgs.gov/' + x
        browser.visit(url)
        
        html = browser.html
        soup = bs(html, 'html.parser')

        image_links.append("https://astrogeology.usgs.gov" + soup.find('img', class_='wide-image')['src'])

    hemisphere_image_urls = []
    for x in range(0, len(image_links)):
        hemisphere_image_urls.append({'title': images[x].h3.text, 'img_url': image_links[x]})

    mars_data = {'news': news, 'weather':mars_weather, 'featured_image':featured_image_url, 'bg_image':bg_url, 'facts':html_table, 'hemisphere_images':hemisphere_image_urls}
    browser.quit()

    return mars_data