import re

# Merge list of string into a long text.
def join_txt(list_txt):
    # Join list of content into 1 simple paragraph
    seperator = ', '
    return seperator.join(list_txt)


# Split Url out of content
def get_url(regex, sample):
    result = re.search(regex, sample)

    if result:
        print(result[0])
        return result[0]

    return ''

# Split text out of content
def split_txt_form_url(regex, sample):
    url = get_url(regex, sample)
    result = sample.strip(url)
    
    return result

# Get hastags out of string.
def get_hastags_out(regex, sample):

    # Find all possible hastags
    result = re.findall(regex,sample)

    return result

# Strip "#" within string
def stript_hastags(sample):
    return sample.replace("#",'')



# Scrapt content base on xpath command.
def scrapt_w_xpath(xpath_cmd):
    result = dict()
    
    # Content
    contents = xpath_selector.xpath(xpath_cmd[0]).extract()
    result.update({'Contents': contents})
    
    # Tags
    tags = xpath_selector.xpath(xpath_cmd[1]).extract()
    result.update({'Tags': tags})
    
    return result


title_attempt = True

def fetch_contents(target_url, target_df, list_xpath):
    for key, url in enumerate(target_url):

        # Start the connection
        res = requests.get(url)

        # Initialize XPath
        xpath_selector = Selector(text=res.text)

        # Get return content as text
        text_html = res.text

        # Check return header
        if res.status_code == 200:
            print("Header:  ", 200)
    #         soup = BeautifulSoup(res.content, 'lxml')
            xpath_selector = Selector(text=text_html)

            # Scrapt content with XPath
            list_scrapt = scrapt_w_xpath(xpath_bbc)

            count_xp_scrapt = len(list_scrapt)


            if count_xp_scrapt:

                # Add new columns
                if title_attempt:
                    df_temp = pd.DataFrame(columns = list(list_scrapt.keys()))
                    target_df = pd.concat([bbc, df_temp])
                    print(target_df.columns)
                    title_attempt = False

                # Add to dataFrame
                for k_, v_ in list_scrapt.items():
                    target_df[k_].iloc[key] = v_

            else:
                print("Return list is emptied ! ({})".format(url))
        else:
            print("['ERRORS'] {} , at {}".format(res.status_code, url))