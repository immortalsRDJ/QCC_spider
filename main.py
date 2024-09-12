import requests
from bs4 import BeautifulSoup
from lxml import etree
from urllib.parse import quote
import csv
import requests
import time
import random
from openpyxl import load_workbook
from JSreverse import get_header


def get_com_l(csv_file):
    companylist = []
    with open(csv_file) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            if row != [] and row[0] != "None":
                companylist.append(str(row[0]))
    return companylist


def get_innerpage_url(com_str, cookies):
    com_encode = quote(com_str)
    url = f'https://www.qcc.com/web/search?key={com_encode}'

    headers = get_header(url)

    res = requests.get(url=url, headers=headers, cookies=cookies, timeout=(2, 2)).content

    tree = etree.HTML(res)
    url = (tree.xpath('//span[@class="copy-title"]/a/@href') + [''])[0]
    return url, res


def into_excel(filename, l_item):
    ## excel filename, ends with ".xlsx"
    wb = load_workbook(filename)
    ws = wb.active
    ##l_item is a list transfered from a dict, including one row info.
    ws.append(l_item)
    print(l_item)
    print('add completed')

    wb.save(filename)


def url_check(url, com_str):
    global nul_num, basic_file, share_file
    ## when there is no match company
    if url == '':
        l_item = []
        l_item.append(com_str)
        into_excel(basic_file, l_item)
        into_excel(share_file, l_item)
        print(com_str + '搜寻无果，自动跳过')
        nul_num += 1

        time.sleep(random.randint(3, 5))

    else:
        return url


def get_response(url):
    global cookies
    l = []
    headers = get_header(url)
    response = requests.get(url=url, cookies=cookies, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    td_tags = soup.find_all('td')
    for td_tag in td_tags:
        data = td_tag.get_text().strip()
        # print(data)
        l.append(data)
    return l


def get_basic_info(qccl):
    table_key = ['统一社会信用代码', '企业名称', '法定代表人', '登记状态', '成立日期', '注册资本', '实缴资本',
                 '组织机构代码', '工商注册号', '纳税人识别号', '企业类型', '营业期限', '纳税人资质', '人员规模',
                 '参保人数', '核准日期', '所属地区', '登记机关', '进出口企业代码', '国标行业', '英文名', '注册地址',
                 '通信地址', '经营范围']
    d = {}
    d['运营单位'] = str(com_str)
    for key in table_key:
        if key in qccl:
            indd = qccl.index(key)
            d[key] = qccl[indd + 1]
        else:
            d[key] = ""
    print(d)
    l_item = []
    for key in d:
        l_item.append(d[key])

    into_excel(basic_file, l_item)


def get_share_info(qccl):
    sharenum = [str(i) for i in range(1, 31)]
    keyname = ["公司名称", "序号", "股东名称", "持股比例", "认缴出资额(万元)", "认缴出资日期", "首次持股日期",
               "关联产品/机构"]
    k = 0
    while qccl[7 * k] == sharenum[k]:
        d = {}
        c = 0
        d['公司名称'] = com_str
        for aaa in keyname[1:]:
            d[aaa] = qccl[7 * k + c]
            c += 1
        l_item = []
        for key in d:
            l_item.append(d[key])

        into_excel(share_file, l_item)
        k += 1



if __name__ == "__main__":

    cookies = {
            "QCCSESSID": "d0e5ed5fb948c828489e647fb5",
            "qcc_did": "6ff485cc-79b0-44df-b439-338d132d6e24"
        }
    l_item = []
    nul_num = 0
    csv_file = "com_list.csv"

    basic_file = 'Layer1_basic.xlsx'
    share_file = 'Layer1_share.xlsx'

    companylist = get_com_l(csv_file)
    for com_str in companylist:
        l_item = []
        l = []
        url, res = get_innerpage_url(com_str, cookies)
        url = url_check(url, com_str)

        if nul_num >= 100:
            print('Some error occurred, plz check.')
            break

        decoded_html = res.decode('utf-8')
        if "用户验证" in decoded_html:
            print("账号使用异常，已限制继续访问，使用企查查APP扫码解除限制。")
            break

        l = get_response(url)

        try:
            ind = l.index("经营范围")
        except ValueError:
            try:
                ind = l.index("宗旨和业务范围")
            except ValueError:
                print("Error ocurred.")
                
            else:
                # 如果第二个 try 块没有引发异常，执行这个 else
                qccl = l[:ind + 2]
                lccq = l[ind+2:]
                get_basic_info(qccl)
                get_share_info(lccq)
                time.sleep(random.randint(20, 25))
                
        else:
            # 如果第一个 try 块没有引发异常，执行这个 else
            qccl = l[:ind + 2]
            lccq = l[ind+2:]
            get_basic_info(qccl)
            get_share_info(lccq)
            time.sleep(random.randint(20, 25))
            
        