import requests
import lxml.html as html
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//h2[@class="headline"]/a/@href'
XPATH_TITLE = '//h1[@class="headline"]/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="articleWrapper  "]/p[not(@class)]/text()'


# Función para obtener el contenido de una url
def response_to_parse(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            parsed = html.fromstring(content)
            return parsed
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


# Obtener el título, resumen y el cuerpo de cada artículo
def parse_notice(link, today):
    parsed = response_to_parse(link)
    try:
        title = parsed.xpath(XPATH_TITLE)[0]
        title = title.replace('\"', '')
        summary = parsed.xpath(XPATH_SUMMARY)[0]
        body = parsed.xpath(XPATH_BODY)
    except IndexError:
        return
    with open(f'data/{today}/{title}.txt', 'w', encoding='utf-8') as f:
        f.write(title)
        f.write('\n\n')
        f.write(summary)
        f.write('\n\n')
        for p in body:
            f.write(p)
            f.write('\n')


# Obtener las url desde el home y crear carpeta
def parse_home():
    parsed = response_to_parse(HOME_URL)
    links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)

    today = datetime.date.today().strftime('%d-%m-%Y')
    path = f'./data/{today}'
    if not os.path.isdir(path):
        os.mkdir(path)

    for link in links_to_notices:
        parse_notice(link, today)


def run():
    parse_home()


if __name__ == '__main__':
    run()