from bs4 import BeautifulSoup
import requests


def get_domain(url):
    split_url = url.split('/')
    for i in range(len(split_url)):
        if 'http' not in split_url[i] and len(split_url[i]) > 0:
            return split_url[i]

def crawl_page(url, base_domain=None, suppress_errors=True):
    if not suppress_errors:
        print("crawling page: {}".format(url))
    
    protocol = 'http:'
    if 'https' in url:
        protocol = 'https:'
    pre_www = 'www' in url
    
    if protocol not in url:
        url = protocol + '//' + url

    if base_domain is None:
        base_domain = get_domain(url)
    
    resp = requests.get(url, timeout=15, allow_redirects=True)
    soup = BeautifulSoup(resp.text, 'lxml')

    # look for links
    outbound_links = 0
    internal_links = []
    calls_to_action = 0
    
    external_sources = ["qgiv", "paypal", "blackbaud", "classy", "onecause", "mobilecause", "networkforgood", "givelively", "giveeffect", "engagingnetworks", "donordrive", "stripe", "securegive", "facebook", "twitter", "instagram"]
    
    link_targets = {}
    iframe_srcs = {}
    script_sources = {}
    for t in external_sources:
        iframe_srcs["iframe_source_{}".format(t)] = 0 
        link_targets["link_target_{}".format(t)] = 0
        script_sources["script_source_{}".format(t)] = 0
        
        
    for link in soup.find_all('a', href=True):        
        if len(link['href'].replace('#', '')) > 0 and link['href'].replace('#', '')[-4:] not in ['.pdf', '.jpg', '.gif', '.png', '.mov', '.mp4', '.wmv', '.avi', '.mkv']:
            if ('http' in link['href'] and base_domain in link['href']) or ('http' not in link['href'] and link['href'][0] == '/'):
                if 'http' not in link['href'] and link['href'][0] == '/':
                    _url = protocol + '://'
                    if pre_www:
                        _url += 'www.'
                    _url += base_domain + link['href']
                else:
                    _url = link['href']

                internal_links.append(_url)
            else:
                outbound_links += 1
        
        # look for calls to action
        for call_to_action in ["give", "donate", "register", "join", "gift", "get started", "be a part", "be part", "help", "change"]:
            if call_to_action in link.text.lower():
                calls_to_action += 1
                break
                
        # look for categorized link targets
        for target in external_sources:
            if target in link['href'].lower() or target in link.text.lower():
                link_targets["link_target_{}".format(target)] += 1
    
    for iframe in soup.find_all('iframe', src=True):
        # iterate through all iframes looking for references to Qgiv or competitors
        for target in external_sources:
            if target in iframe['src']:
                iframe_srcs["iframe_source_{}".format(target)] += 1
            
    # look for scripts
    for script in soup.find_all('script'):
        # trying to account for static script includes as well as dynamic loading,
        # so we look at the script content if there is no SRC attribute
        if 'src' in script:
            js_check = script['src']
        else:
            js_check = script.text
        
        for source in external_sources:
            if source in js_check:
                script_sources["script_source_{}".format(source)] += 1
    
    # word & image count
    word_count = len(soup.text.replace('\n', '').replace('\r', ''))
    image_count = len(soup.find_all('img'))
            
    return_data = {
        'url': url,
        'outbound_links': outbound_links, 
        'internal_links': len(internal_links),
        'calls_to_action': calls_to_action,
        'word_count': word_count,
        'image_count': image_count,
        '_other_pages': internal_links
    }
    return_data.update(script_sources)
    return_data.update(link_targets)
    return_data.update(iframe_srcs)
    
    return return_data


def crawl(url, suppress_errors=True):
    base_domain = get_domain(url)
    
    if base_domain is None or 'qgiv.com' in base_domain:
        return []
    
    pages = []
    pages_to_crawl = []
    pages_crawled = [url]
    
    # scrape home page
    try:
        page_stats = crawl_page(url, base_domain=base_domain, suppress_errors=suppress_errors)
    except:
        #if not suppress_errors:
        print("\t\tcould not crawl url: {}".format(url))
        return []
    
    pages.append(page_stats)
    pages_to_crawl = page_stats['_other_pages']
    
    # crawl through sub pages
    for p in pages_to_crawl:
        if len(pages_crawled) >= 100:
            # hardcoded limit to 100 pages
            break
        if p not in pages_crawled:
            pages_crawled.append(p)
            
            try:
                page_stats = crawl_page(p, base_domain=base_domain)
                pages.append(page_stats)
            except:
                if not suppress_errors:
                    print("could not open url: {}".format(url))
                continue
    
            ''' restricting to top level links only
            for new_page in page_stats['_other_pages']:
                if new_page not in pages_to_crawl and new_page not in pages_crawled:
                    pages_to_crawl.append(new_page)
            '''
    # process page stats
    for i in pages:
        del(i['_other_pages'])
        
    return pages