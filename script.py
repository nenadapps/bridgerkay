import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from time import sleep
from random import randint,shuffle

def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except: 
        pass
        
    return html_content

def get_page_items(url):
    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('#Table1 td a'):
            item_link = item.get('href')
            if "Basic_Details.php?" in item_link: 
                item_link = item_link.replace('./', 'https://www.bridgerkay.com/')
                items.append(item_link)
    except: 
        pass

    try:
        next_items = html.find_all('a')
        for next_item in next_items:
            next_item_img = next_item.find('img')
            if next_item_img:
                next_img_src = next_item_img.get('src')
                if 'next.png' in next_img_src:
                    next_url = next_item.get('href').replace('./', 'https://www.bridgerkay.com/')
                    break
    except:
        pass

    shuffle(items)

    return items, next_url

def get_details(html, url, start_index):
    
    stamp = {}

    try:
       tr0 = html.select('#Table1 tr')[start_index]
       tr2 = html.select('#Table1 tr')[start_index + 2]
       tr1 = html.select('#Table1 tr')[start_index + 1]
       tr4 = html.select('#Table1 tr')[start_index + 4]
       tr5 = html.select('#Table1 tr')[start_index + 5]
    except:
       pass 

    try:
        price = get_td_value(tr5, 1)
        price = price.replace(",", "")
        stamp['price'] = price.replace('£','').strip()
    except:
        stamp['price'] = None

    try:
        country = get_td_value(tr0, 1)
        stamp['country'] = country
    except:
        stamp['country'] = None
        
    try:
        tags = get_td_value(tr0, 2)
        stamp['tags'] = tags
    except:
        stamp['tags'] = None

    try:
        sg = get_td_value(tr1, 0)
        sg = sg.replace('SG. No.', '').strip()
        stamp['SG'] = sg
    except:
        stamp['SG'] = None
        
    try:
        condition = get_td_value(tr2, 0)
        stamp['condition'] = condition
    except:
        stamp['condition'] = None

    try:
        scott_num = get_td_value(tr1, 1)
        scott_num = scott_num.replace('Scott No.', '').strip()
        stamp['scott_num'] = scott_num
    except:
        stamp['scott_num'] = None

    try:
        raw_text = get_td_value(tr4, 0)
        stamp['raw_text'] = raw_text.replace('\n',' ')
    except:
        stamp['raw_text'] = None

    stamp['currency'] = 'GBP'

    # image_urls should be a list
    images = []
    try:
        image_items = tr0.select('a')
        for image_item in image_items:
            img = image_item.get('href')
            if not 'nopicture.png' in img:
                img = img.replace('./', 'https://www.bridgerkay.com/')
                images.append(img)
    except:
        pass

    stamp['image_urls'] = images 

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(22,99))
    return stamp

def get_td_value(tr, index):
    td = tr.select('td')[index].get_text().strip()
    return td

# page url
page_url = 'https://www.bridgerkay.com/Basic_Gallery.php?cs=156218818750&cr=0'

# loop trough every item on current page
while(page_url):
    page_items, page_url = get_page_items(page_url)
    for page_item in page_items:
        # get all items on current details page
        try:
            html = get_html(page_item)
            total_rows = len(html.select('#Table1 tr'))
            total_items = total_rows // 7 
            for start_index in range(total_items):
                # get details for current item
                get_details(html, page_item, start_index * 7)
        except:
            continue
            
         