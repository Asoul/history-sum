import csv
import requests
from lxml import html

url = "http://www.twse.com.tw/ch/trading/indices/MI_5MINS_HIST/MI_5MINS_HIST.php"

output_file = open('output.csv', 'a')
csv_writer = csv.writer(output_file)

def crawl(date):
    # First date is 88/01/05
    if date[0] < 88:
        return

    params = {
        "myear": str(date[0]),
        "mmon": str(date[1]).zfill(2),
    }

    response = requests.post(url, params=params)
    tree = html.fromstring(response.content)
    trs = tree.xpath('//tr[@id="contentblock"]/td/table[3]/tr[position() > 2]')
    outputs = []
    for tr in trs:
        tds = [td.strip() for td in tr.xpath('td/text()')]
        outputs.append(tds)
    csv_writer.writerows(outputs)

    # Crawl previous month
    date[1] -= 1
    if date[1] == 0:
        date[1] = 12
        date[0] -= 1
    crawl(date)

if __name__ == '__main__':
    crawl([105, 07])
