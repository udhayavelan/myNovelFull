import requests
from bs4 import BeautifulSoup
import json
from functools import reduce
import novelapp.EpubMainFunction  as ep
import re


def wuxia_world_convertion(link):
    fn_result = {}
    check = True
    try:
        novelName = link.split("/")[-2]
        baselink = 'https://www.wuxiaworld.com'

        chap_list = []
        while True:
            chap_dict = {}
            page = requests.get(link).text
            # print(link)
            soup = BeautifulSoup(page, 'html.parser')
            if not [i for i in soup.findAll("script") if "var CHAPTER" in i.text]:
                break
            novelmap = json.loads([i for i in soup.findAll("script") if "var CHAPTER" in i.text][0] \
                                  .text.strip().replace("var", "").replace("CHAPTER", "").replace("=", "") \
                                  .replace(";", ""))
            # print(novelmap)
            chapter = novelmap.get("name")
            nextchapter = novelmap.get("nextChapter")
            has_chapter = novelmap.get("isTeaser")
            if has_chapter or has_chapter == None:
                break
            link = baselink + nextchapter
            if not [i for i in soup.find_all(class_="fr-view") if len(i) > 30]:
                continue
            dataList = [i.text for i in [i for i in soup.find_all(class_="fr-view") if len(i) > 30][0] \
                .find_all("p")]
            chapter_content = reduce((lambda x, y: str(x) + "##~##" + str(y)), dataList)
            if len(chapter_content) > 50:
                chapter = re.sub(r'[?|$|"\'|!]',r'',chapter)
                chap_dict[chapter] =   re.sub(r'[?|$|"\'|!]',r'', chapter_content)
                chap_list.append(chap_dict)

        file_list = ep.clean(chap_list)
        filepath = ep.generate(file_list, novelName, "dbz")
        fn_result["path"] = filepath
    except Exception:
        print("error")
        check = False
    fn_result["check"] = check
    return fn_result


def novel_full(link):
    fn_result = {}
    check = True
    try:
        novelName = link.split("/")[-2]

        baselink = 'http://novelfull.com'

        chap_list = []
        while True:
            try:
                chap_dict = {}
                page = requests.get(link).text
                soup = BeautifulSoup(page, 'html.parser')

                chapter = reduce((lambda x, y: str(x) + "##~##" + str(y))
                                 , [i.text for i in soup.find(class_="cha-words").findAll('p')])
                # print(chapter)
                check_next_chapter = False
                try:
                    next_chap = soup.find(id="next_chap")['href']
                except Exception as ex:
                    check_next_chapter = True
                    print(ex)
                title = soup.find("title").text.replace("online free - NovelFull", "") \
                    .replace("Read", "").strip()
                print(title)
                print(check_next_chapter)
                title = re.sub(r'[?|$|"\'|!]',r'',title)
                chap_dict[title] = re.sub(r'[?|$|"\'|!]',r'',chapter)
                chap_list.append(chap_dict)
                if check_next_chapter:
                    break
                else:
                    link = baselink + next_chap


            except Exception as ex:
                print(ex)
                break
        file_list = ep.clean(chap_list)
        filepath = ep.generate(file_list, novelName, "dbz")
        fn_result["path"] = filepath
    except Exception:
        print("error")
        check = False
    fn_result["check"] = check
    return fn_result


def get_novelmap(link):
    baselink = 'https://www.wuxiaworld.com'
    chap_list = []
    while True:
        chap_dict = {}
        page = requests.get(link).text
        soup = BeautifulSoup(page,'html.parser')
        if not [ i for i in soup.findAll("script") if "var CHAPTER" in i.text]:
            break
        novelmap =  json.loads(  [ i for i in soup.findAll("script") if "var CHAPTER" in i.text][0]\
                                  .text.strip().replace("var","").replace("CHAPTER","").replace("=","")\
                                  .replace(";",""))
        chapter = novelmap.get("name")
        nextchapter = novelmap.get("nextChapter")
        has_chapter = novelmap.get("isTeaser")
#        print(nextchapter,chapter)
        if has_chapter or has_chapter == None:
            break
        link = baselink+nextchapter
        if not [i for i in  soup.find_all(class_="fr-view") if len(i) > 30]:
            continue
        dataList = [ i.text for i in [i for i in  soup.find_all(class_="fr-view") if len(i) > 30][0]\
                                      .find_all("p")]
        chapter_content = reduce((lambda x, y: str(x) +"##~##"+ str(y)),dataList)
        if len(chapter_content) > 50:
                chap_dict[chapter] = chapter_content
                chap_list.append(chap_dict)
    return chap_list



def custom_novel(linklist):
    fn_result = {}
    try:
        chap_list = []
        for i in linklist:
            cc = i.split("/")[4]
            chap_list.append({"chapindex-" + cc: "You going to read " + cc})
            chap_list.extend(get_novelmap(i))

        file_list = ep.clean(chap_list)
        filepath = ep.generate(file_list, "wuxiacombi", "dbz")
        fn_result["path"] = filepath

    except Exception:
        print("error")
        check = False
        fn_result["check"] = check
    return fn_result