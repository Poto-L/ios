# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# 关于 m3u8 处理
import sys
import os
import m3u8
import requests
import time

theNeed = {"CCTV-1": {"match": "CCTV-1", "link": "", "speed": "0"},
           "CCTV-2": {"match": "CCTV-2", "link": "", "speed": "0"},
           "CCTV-3": {"match": "CCTV-3", "link": "", "speed": "0"},
           "CCTV-4": {"match": "CCTV-4", "link": "", "speed": "0"},
           "CCTV-5": {"match": "CCTV-5", "link": "", "speed": "0"},
           "CCTV-6": {"match": "CCTV-6", "link": "", "speed": "0"},
           "CCTV-7": {"match": "CCTV-7", "link": "", "speed": "0"},
           "CCTV-8": {"match": "CCTV-8", "link": "", "speed": "0"},
           "CCTV-9": {"match": "CCTV-9", "link": "", "speed": "0"},
           "CCTV-10": {"match": "CCTV-10", "link": "", "speed": "0"},
           "CCTV-11": {"match": "CCTV-11", "link": "", "speed": "0"},
           "CCTV-12": {"match": "CCTV-12", "link": "", "speed": "0"},
           "CCTV-13": {"match": "CCTV-13", "link": "", "speed": "0"},
           "东方卫视": {"match": "东方卫视", "link": "", "speed": "0"},
           "东南卫视": {"match": "东南卫视", "link": "", "speed": "0"},
           "北京卫视": {"match": "北京卫视", "link": "", "speed": "0"},
           "甘肃卫视": {"match": "甘肃卫视", "link": "", "speed": "0"},
           "广东卫视": {"match": "广东卫视", "link": "", "speed": "0"},
           "广西卫视": {"match": "广西卫视", "link": "", "speed": "0"},
           "贵州卫视": {"match": "贵州卫视", "link": "", "speed": "0"},
           "河北卫视": {"match": "河北卫视", "link": "", "speed": "0"},
           "黑龙江卫视": {"match": "黑龙江卫视", "link": "", "speed": "0"},
           "湖北卫视": {"match": "湖北卫视", "link": "", "speed": "0"},
           "湖南卫视": {"match": "湖南卫视", "link": "", "speed": "0"},
           "浙江卫视": {"match": "浙江卫视", "link": "", "speed": "0"},
           "吉林卫视": {"match": "吉林卫视", "link": "", "speed": "0"},
           "江苏卫视": {"match": "江苏卫视", "link": "", "speed": "0"},
           "江西卫视": {"match": "江西卫视", "link": "", "speed": "0"},
           "辽宁卫视": {"match": "辽宁卫视", "link": "", "speed": "0"},
           "安徽卫视": {"match": "安徽卫视", "link": "", "speed": "0"},
           "重庆卫视": {"match": "重庆卫视", "link": "", "speed": "0"},
           "内蒙古卫视": {"match": "内蒙古卫视", "link": "", "speed": "0"},
           "宁夏卫视": {"match": "宁夏卫视", "link": "", "speed": "0"},
           "青海卫视": {"match": "青海卫视", "link": "", "speed": "0"},
           "山东卫视": {"match": "山东卫视", "link": "", "speed": "0"},
           "山西卫视": {"match": "山西卫视", "link": "", "speed": "0"},
           "陕西卫视": {"match": "陕西卫视", "link": "", "speed": "0"},
           "优漫卡通": {"match": "优漫卡通", "link": "", "speed": "0"},
           "卡酷少儿": {"match": "卡酷少儿", "link": "", "speed": "0"},
           "金鹰卡通": {"match": "金鹰卡通", "link": "", "speed": "0"},
           "中国气象": {"match": "中国气象", "link": "", "speed": "0"},
           "番禺综合": {"match": "番禺综合", "link": "", "speed": "0"},
           "佛山综合": {"match": "佛山综合", "link": "", "speed": "0"},
           "韶关综合": {"match": "韶关综合", "link": "", "speed": "0"},
           "珠海综合": {"match": "珠海综合", "link": "", "speed": "0"},
           "东莞综合": {"match": "东莞综合", "link": "", "speed": "0"},
           "惠州综合": {"match": "惠州综合", "link": "", "speed": "0"}}

# 检查链接数据
# ok? speed 链接速度
def toCheckLink(link):
    ok = False
    speed = 0
    try:
        now = time.time()
        req = requests.get(link)
        speed = int((time.time() - now)*1000)
        if "200" in str(req):
            ok = True
        else:
            pass
    except requests.exceptions.ConnectionError:
        pass
    return ok, speed

# 获取文件信息
def toGetM3U8(path):
    list = m3u8.load(path, timeout=30)

    for item in list.segments:
        name = item.title
        link = item.absolute_uri

        if name in theNeed:
            match = theNeed[name]
            if match:
                # 验证链接是否可用
                ok, newSp = toCheckLink(link)
                if ok:
                    speed = int(match["speed"])
                    if speed == 0 or newSp < speed:
                        match["link"] = link
                        match["speed"] = str(newSp)

# 获取m3u8文件
def toGetM3U8FileInDoc(doc):
    results = []
    for root, dirs, files in os.walk(doc, topdown=False):
        for obj in files:
            if obj.endswith(".m3u"):
                path = root + obj
                results.append(path)
    return results

# 保存m3u8文件
def toSaveM3U8WithNeed(need):
    list = m3u8.loads("")

    for obj in need.values():
        link = obj["link"]
        if len(link) > 0:
            seg = m3u8.Segment(obj["link"], title=obj["match"], duration=-1)
            list.segments.append(seg)
        else:
            # 标记失效的界面
            seg = m3u8.Segment("http://", title=(obj["match"] + " 失效"), duration=-1)
            list.segments.append(seg)
    list.dump("电信ISP.m3u")
    print(need)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    doc = sys.path[0] + "/file/"
    files = toGetM3U8FileInDoc(doc)
    #url = "https://raw.githubusercontent.com/cai23511/yex/master/TVlist/20210808384.m3u"
    toGetM3U8(files[0])
    toSaveM3U8WithNeed(theNeed)
