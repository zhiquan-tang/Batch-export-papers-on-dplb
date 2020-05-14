## coding:utf-8
## email: zqtang.chn@gmail.com
import requests, re, openpyxl
from html import unescape
from googletrans import Translator
import json

print("###################")
print("dblp论文批量导出工具")
print("     2019/10/26    ")
print("###################")
url = input('键入会议或论文地址(e.g.,https://dblp.org/db/conf/ndss/ndss2019.html)\n:')  # 会议URL
tran = input('默认翻译，键入0则不使用翻译\n:')
page = requests.get(url)
print("网页已下载......")
papers = re.findall(
    r'<span class=\"title\" itemprop=\"name\">(.*?)</span>|<header><h2>([\s\S]*?)</h2></header>',
    page.text,
)
print("正在导出并依次翻译......")
paperTitle, paperTitleZh = [], []
translator = Translator(service_urls=["translate.google.cn"])
for paper in papers:
    if paper[0] != "":
        paper = paper[0]
    else:
        paperTitle.append('')
        paperTitleZh.append('')
        paper = paper[1]
    paper = unescape(paper).replace('\n', '')
    paperTitle.append(paper)
    if tran == '0':
        paperTitleZh.append('')
    else:
        try:
            paperZh = translator.translate(paper, src="en", dest="zh-cn").text
        except json.decoder.JSONDecodeError:
            print(paper, '翻译失败')
            paperZh = '翻译失败'
        paperTitleZh.append(paperZh)
mywb = openpyxl.Workbook()
sheet = mywb.active
for i in range(len(paperTitle)):
    sheet["A" + str(i + 1)] = paperTitle[i]
    sheet["B" + str(i + 1)] = paperTitleZh[i]
mywb.save(url.split("/")[-1].split(".")[0] + ".xlsx")
print("完成！")
