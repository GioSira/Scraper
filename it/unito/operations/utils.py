from lxml import html


def extract(page, key, type):
    if type == 'href':
        return extract_link(page, key)
    elif type == 'text':
        return extract_text(page, key)
    elif type == 'src':
        return extract_source(page, key)
    else:
        raise NotImplementedError(f'method for {type} has not been implemented yet')


def extract_text(page, key):
    text = page.xpath(f'{key}/text()')
    return clean_page(text)


def extract_link(page, key):
    return page.xpath(f'{key}/@href')


def extract_source(page, key):
    return page.xpath(f'{key}/@src')


def get_element(page, xpath):
    element = page.xpath(xpath)
    assert len(element) == 1, 'length element extracted is not 1'
    return html.fromstring(element[0])


def get_elements(page, xpath):
    elements = page.xpath(xpath)
    parsed_elements = []
    assert len(elements) >= 1, 'element list is empty'
    for element in elements:
        parsed_elements.append(html.fromstring(element))
    return parsed_elements


def clean_page(page):
    pagestring = str(page)
    pagestring = pagestring.replace('\s+', ' ')
    pagestring = pagestring.replace('\n+', '\n')
    pagestring = pagestring.replace('\t+', '\t')
    return pagestring
