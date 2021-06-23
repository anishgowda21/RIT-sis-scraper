import pickle
from sys import path_importer_cache
import time
from bs4 import BeautifulSoup
import requests
from consts import *
import re
import json
import pprint


def cal_per(pre, abs):
    percetage = round((pre/(pre+abs))*100)
    return (str(percetage)+"%")


def get_att(s, suburl):
    attDict = {"totalPresent": 0, "totalAbsent": 0, "percentage": "0%", "stillToGo": 0,
               "presentClasses": [], "absentClasses": []}
    print(url+suburl)
    data = s.get(url+suburl).text
    attData = BeautifulSoup(data, "html.parser")
    try:
        attDict["totalPresent"] = attData.find(
            "span", {"class": "uk-label cn-color-green"}).get_text().split()[1]
    except Exception:
        pass
    try:
        attDict["totalAbsent"] = attData.find(
            "span", {"class": "uk-label cn-color-red"}).get_text().split()[1]
    except Exception:
        pass
    try:
        attDict["stillToGo"] = attData.find(
            "span", {"class": "uk-label cn-still cn-color-grey"}).get_text().split()[-1].replace("[", "").replace("]", "")
    except Exception:
        pass
    try:
        attDict["percentage"] = cal_per(
            int(attDict["totalPresent"]), int(attDict["totalAbsent"]))
    except Exception:
        pass

    preTable = attData.find(
        "table", {"class": "uk-table uk-table-small cn-attend-list1 uk-table-striped"}).find_all("tr")

    for entry in preTable[1:]:
        subObj = {}
        entry = entry.find_all("td")
        subObj["slNo"] = entry[0].get_text()
        subObj["date"] = entry[1].get_text()
        subObj["time"] = re.sub("[\n\r\s]+", " ", entry[2].get_text())
        attDict["presentClasses"].append(subObj)

    absTable = attData.find("table", {
                            "class": "uk-table uk-table-small cn-attend-list2 uk-table-striped"}).find_all("tr")

    for entry in absTable[1:]:
        subObj = {}
        entry = entry.find_all("td")
        subObj["slNo"] = entry[0].get_text()
        subObj["date"] = entry[1].get_text()
        subObj["time"] = re.sub("[\n\r\s]+", " ", entry[2].get_text())
        attDict["absentClasses"].append(subObj)

    return attDict


def get_cie(s, suburl):
    cieDict = {"tests": {}, "assignments": {}, "final": "-"}
    print(url+suburl)
    data = s.get(url+suburl).text
    cieData = BeautifulSoup(data, "html.parser")
    cieTable = cieData.find(
        "table", {"class": "uk-table cn-cie-table uk-table-responsive"}).find_all("tr")[1].find_all("td")
    for i, test in enumerate(cieTable[:4], 1):
        fieldData = test.get_text()
        if fieldData == "" or fieldData == "%" or fieldData == "-":
            cieDict['tests'][i] = "-"
        else:
            cieDict['tests'][i] = test.get_text()
    for i, assign in enumerate(cieTable[4:7], 1):
        cieDict['assignments'][i] = assign.get_text()
    try:
        cieDict['final'] = cieTable[7].get_text()
    except Exception:
        pass
    return(cieDict)



def set_basic_vals(data):
    final_dic = {"name": "", "usn": "", "course": "", "semister": "",
                 "batch": "", "last_updated": "", "image_url": "", "courses": []}
    try:
        vals = data.find(
            "table", {"class": "uk-table uk-table-divider cn-stu-info uk-table-responsive"}).find_all("tr")
    except Exception:
        return 0
    final_dic["name"] = vals[0].find_all("td")[0].get_text().split(": ")[1]
    final_dic["semister"] = vals[0].find_all("td")[2].get_text().split(": ")[1]
    final_dic["usn"] = vals[1].find_all("td")[0].get_text().split(": ")[1]
    final_dic["course"] = vals[2].find_all("td")[0].get_text().split(": ")[1]
    final_dic["batch"] = vals[3].find_all("td")[0].get_text().split(": ")[1]
    final_dic["last_updated"] = data.find(
        "p", {"class": "uk-text-right cn-last-update"}).get_text().split(": ")[1]
    print(url+data.find(
        "img", {"class": "uk-preserve-width uk-border"})["src"])
    final_dic["image_url"] = url+data.find(
        "img", {"class": "uk-preserve-width uk-border"})["src"]
    return final_dic


def get_data(usn, dob):
    try:
        parms["yyyy"], parms["mm"], parms["dd"] = dob.split("-")
        parms["username"] = usn.lower()
        parms["passwd"] = dob
    except Exception:
        return {"status": "error", "reason": "Invalid format"}

    s = requests.Session()
    po = s.post(baseUrl, data=parms)
    data = BeautifulSoup(po.text, "html.parser")
    finalDict = set_basic_vals(data)
    if finalDict == 0:
        return {"status": "error", "reason": "Invalid creds"}
    print(finalDict)

    po = s.get(dash_url)
    Subjects = BeautifulSoup(po.text, "html.parser").find("table", {
        "class": "dash_even_row uk-table uk-table-striped uk-table-hover cn-pay-table uk-table-middle uk-table-responsive"})
    if Subjects == None:
        Subjects = BeautifulSoup(po.text, "html.parser").find("table", {
            "class": "dash_od_row uk-table uk-table-striped uk-table-hover cn-pay-table uk-table-middle uk-table-responsive"})
    Subjects = Subjects.find_all('tr')
    for subject in Subjects[1:]:
        subDict = {}
        links = subject.find_all("td")
        ccode = links[0].get_text()
        cname = links[1].get_text()
        aurl = links[4].find("a")["href"]
        curl = links[5].find("a")["href"]
        subDict["name"] = cname
        subDict["code"] = ccode
        print("in ", cname)
        subDict["attendence"] = get_att(s, aurl)
        subDict["cie"] = get_cie(s, curl)
        finalDict["courses"].append(subDict)
    lo = s.post(url, data=params2)

    return finalDict
 
