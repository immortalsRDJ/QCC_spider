import aiohttp
import asyncio
from bs4 import BeautifulSoup
from lxml import etree
from urllib.parse import quote
from openpyxl import load_workbook
import random
import csv
import aiofiles
import pandas as pd
from JSreverse import get_header  
from merge import merge_share_info, merge_basic_info

async def get_com_l(csv_file):
    companylist = []
    async with aiofiles.open(csv_file, mode='r') as f:
        async for line in f:
            row = line.strip().split(',')
            if row and row[0] != "None":
                companylist.append(str(row[0]))
    return companylist


async def get_innerpage_url(com_str, cookies):
    com_encode = quote(com_str)
    url = f'https://www.qcc.com/web/search?key={com_encode}'
    headers = get_header(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, cookies=cookies) as response:
            res = await response.text()
            tree = etree.HTML(res)
            inner_url = (tree.xpath('//span[@class="copy-title"]/a/@href') + [''])[0]
    return inner_url, res


async def into_excel(filename, l_item):
    wb = load_workbook(filename)
    ws = wb.active
    ws.append(l_item)
    #print(f'写入: {l_item} 到文件 {filename}')
    wb.save(filename)


async def url_check(url, com_str, basic_file, share_file):
    if url == '':
        l_item = [com_str]
        await into_excel(basic_file, l_item)
        await into_excel(share_file, l_item)
        print(f'{com_str} 搜寻无果，自动跳过')
        await asyncio.sleep(random.randint(3, 5))
    else:
        return url


async def get_response(url, cookies):
    global ll
    headers = get_header(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, cookies=cookies, headers=headers) as response:
            html = await response.text()
    soup = BeautifulSoup(html, 'html.parser')
    td_tags = soup.find_all('td')
    th_tags = soup.find_all('th')
    l = [td.get_text().strip() for td in td_tags]
    ll = [th.get_text().strip() for th in th_tags]
    return l


async def get_basic_info(data, com_str, basic_file):
    global unique_id
    basic_d = {"运营单位":com_str, "统一社会信用代码":'', "企业名称":'', "法定代表人":'','登记状态':'','成立日期':'',
               '注册资本':'','实缴资本':'','组织机构代码':'','工商注册号':'','纳税人识别号':'','企业类型':'',"营业期限":"",'纳税人资质':'',
               '人员规模':'','参保人数':'','核准日期':'','所属地区':'','登记机关':'','进出口企业代码':'','国标行业':'','英文名':'','注册地址':'','通信地址':'','经营范围':''}
    for key in basic_d:
        if key in data:
            basic_index = data.index(key)
            basic_d[key] = data[basic_index+1]
    unique_id = basic_d["统一社会信用代码"]
    l_item = []
    for k in basic_d:
        l_item.append(basic_d[k])
    
    
    await into_excel(basic_file, l_item)



async def get_share_info(qccl, com_str, share_file):
    
    total_list = []
    index_dict = {}

    for index, value in enumerate(ll):
        if value in index_dict:
            index_dict[value].append(index)
        else:
            index_dict[value] = [index]

    index_start = index_dict["序号"][1]
    index_end = index_dict["序号"][2]
    keyname = ["公司名称"]
    keyname = keyname + ll[int(index_start):int(index_end)]
    qccl_ll = qccl[int(index_start):]

    sharenum = [str(i) for i in range(1, 51)]
    k = 0
    while (len(keyname) - 1) * k < len(qccl_ll) and str(qccl_ll[(len(keyname) - 1) * k]) == sharenum[k]:
        total_d = {
        "公司名称": com_str, "统一社会信用代码":unique_id, '序号': '', 
        '股东名称': '','合伙人名称':'', '持股比例': '', '出资比例':'',
        '认缴出资额(万元)': '', '认缴出资日期': '', '最终受益股份': '',
        '实缴出资额(万元)': '', '实缴出资日期': '', '首次持股日期': '', 
        '关联产品/机构': '', '股份类型': ''
        }
        d = {}
        c = 0
        for aaa in keyname[1:]:
            d[aaa] = qccl_ll[(len(keyname) - 1) * k + c]
            c += 1

        for kk, v in total_d.items():
            if kk in d:
                total_d[kk] = d[kk]
        
        l_item = []

        for key in total_d:
            l_item.append(total_d[key])
        total_list.append(total_d)
        await into_excel(share_file, l_item)  
        k += 1

    return total_list



async def fetch_company_and_shareholders(com_str, cookies, depth=1, max_depth=3):
    if depth > max_depth:
        print(f"已达到最大递归深度：{max_depth}")
        return

    
    basic_file = f'Layer{depth}_basic.xlsx'
    share_file = f'Layer{depth}_share.xlsx'

    print(f"正在爬取 {com_str} 的基本信息和股东信息，当前深度：{depth}")
    
    
    url, res = await get_innerpage_url(com_str, cookies)
    url = await url_check(url, com_str, basic_file, share_file)
    
    if not url:
        return

    
    response_data = await get_response(url, cookies)
    
    
    try:
        ind = response_data.index("经营范围")
    except ValueError:
        try:
            ind = response_data.index("宗旨和业务范围")
        except ValueError:
            print(f"未找到经营范围或业务范围: {com_str}")
            return
    
    qccl = response_data[:ind + 2]
    lccq = response_data[ind + 2:]
    
    
    await get_basic_info(qccl, com_str, basic_file)
    
    
    shareholder_info = await get_share_info(lccq, com_str, share_file)
    
    
    
    for shareholder in shareholder_info:
        shareholder_name = shareholder["股东名称"]
        
        if shareholder_name == '':
            shareholder_name = shareholder["合伙人名称"]


        if shareholder_name[1] == " ":
            continue
        
        if shareholder_name:
            print(f"正在递归爬取 {shareholder_name} 的信息，当前深度：{depth + 1}")
        
            await fetch_company_and_shareholders(
                shareholder_name, cookies, depth=depth + 1, max_depth=max_depth
            )
        
            

async def run_spider(csv_file, cookies):
    companylist = await get_com_l(csv_file)
    
    for com_str in companylist:
        await fetch_company_and_shareholders(com_str, cookies, max_depth=3)
        try:
            output_basic = 'basic_info_merged.xlsx'
            output_share = 'share_info_merged.xlsx'
            merge_basic_info('Layer1_basic.xlsx', 'Layer2_basic.xlsx', 'Layer3_basic.xlsx', output_basic)
            merge_share_info('Layer1_share.xlsx', 'Layer2_share.xlsx', 'Layer3_share.xlsx', output_share)
            
        except FileNotFoundError as e:
            print(f"合并时发生错误：{e}")



if __name__ == "__main__":
    cookies = {
        "QCCSESSID": "3a5beed4b6c4f1993186ad91d5",
        "qcc_did": "6ff485cc-79b0-44df-b439-338d132d6e24"
    }
    
    csv_file = "com_list.csv"

    asyncio.run(run_spider(csv_file, cookies))

