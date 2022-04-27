from bs4 import BeautifulSoup
import requests
from consts import *
import re
import traceback


# Function to calculate percentage of attendance
def cal_per(pre, absent) -> str:
    try:
        percentage = round((pre / (pre + absent)) * 100)
        return str(percentage) + "%"
    except ZeroDivisionError:
        return "0%"


# Function to scrape the attendance data and return a dictionary
def get_attendance_data(s, url) -> dict:
    attendanceDict = {"totalPresent": 0, "totalAbsent": 0, "percentage": "0%", "stillToGo": 0,
                      "presentClasses": [], "absentClasses": []}
    res = s.get(url).text

    attData = BeautifulSoup(res, "html.parser")
    try:
        attendanceDict["totalPresent"] = attData.find(
            "span", {"class": "uk-label cn-color-green"}).get_text().split()[1].strip()
    except (AttributeError, IndexError):
        pass
    try:
        attendanceDict["totalAbsent"] = attData.find(
            "span", {"class": "uk-label cn-color-red"}).get_text().split()[1].strip()
    except (AttributeError, IndexError):
        pass
    try:
        attendanceDict["stillToGo"] = attData.find(
            "span", {"class": "uk-label cn-still cn-color-grey"}).get_text().split()[-1].replace("[", "").replace("]",
                                                                                                                  "").strip()
    except (AttributeError, IndexError):
        pass
    try:
        attendanceDict["percentage"] = cal_per(
            int(attendanceDict["totalPresent"]), int(attendanceDict["totalAbsent"])).strip()
    except (AttributeError, IndexError):
        pass

    # Parse through the table consisting of present and absent classes date and retrieve the dates
    try:
        presentTable = attData.find(
            "table", {"class": "uk-table uk-table-small cn-attend-list1 uk-table-striped"}).find_all("tr")

        for row in presentTable[1:]:
            dayObj = {}
            entry = row.find_all('td')
            dayObj['slNo'] = entry[0].get_text().strip()
            dayObj['date'] = entry[1].get_text().strip()
            dayObj["time"] = re.sub(
                "[\n\r\s]+", " ", entry[2].get_text()).strip()
            attendanceDict["presentClasses"].append(dayObj)
    except (AttributeError, IndexError):
        pass

    try:
        absentTable = attData.find("table", {
            "class": "uk-table uk-table-small cn-attend-list2 uk-table-striped"}).find_all("tr")
        for row in absentTable[1:]:
            dayObj = {}
            entry = row.find_all('td')
            dayObj['slNo'] = entry[0].get_text().strip()
            dayObj['date'] = entry[1].get_text().strip()
            dayObj["time"] = re.sub(
                "[\n\r\s]+", " ", entry[2].get_text()).strip()
            attendanceDict["absentClasses"].append(dayObj)
    except (AttributeError, IndexError):
        pass
    return attendanceDict


# Function to scrape the cie data and return a dictionary

def get_cie_data(s, url):
    cieDict = {"tests": {}, "assignments": {}, "final": "-"}
    res = s.get(url).text
    cieData = BeautifulSoup(res, "html.parser")
    try:
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
        except (AttributeError, IndexError):
            pass
    except(AttributeError, IndexError):
        pass
    return cieDict


# Function to check the dob is in yyyy-mm-dd formate
def check_usn_and_dob_formate(usn, date) -> bool:
    regex = re.compile("[0-9]{4}\-[0-9]{2}\-[0-9]{2}")

    if len(usn) == 10 and usn.startswith('1ms') and re.match(regex, date):
        return True
    return False


# Function to set basic values to a dictionary
def setBasicvalues(url, data):
    finalDict = {"success": "True", "name": "", "usn": "", "course": "", "semester": "", "batch": "", "last_updated": "", "image_url": "",
                 "courses": []}
    try:
        vals = data.find(
            "table", {"class": "uk-table uk-table-divider cn-stu-info uk-table-responsive"}).find_all("tr")

    except AttributeError:
        return 0

    try:
        finalDict["name"] = vals[0].find_all("td")[0].get_text().split(": ")[1]
        finalDict["semester"] = vals[0].find_all(
            "td")[2].get_text().split(": ")[1]
        finalDict["usn"] = vals[1].find_all("td")[0].get_text().split(": ")[1]
        finalDict["course"] = vals[2].find_all(
            "td")[0].get_text().split(": ")[1]
        finalDict["batch"] = vals[3].find_all(
            "td")[0].get_text().split(": ")[1]
        finalDict["last_updated"] = data.find(
            "p", {"class": "uk-text-right cn-last-update"}).get_text().split(": ")[1]
        finalDict["image_url"] = url + \
            data.find("img", {"class": "uk-preserve-width uk-border"})["src"]
        return finalDict

    except AttributeError:
        return 0


def get_sis_data(usn, dob, isfirstyear=False) -> dict:
    if not check_usn_and_dob_formate(usn.lower(), dob):
        return {"success": False, "error": "Invalid credentials formate\ndob should be in yyyy-mm-dd formate"}

    loginData = LoginParams(usn, dob)
    loginUrl = loginData.getLoginUrl(isfirstyear)
    payload = loginData.getLoginPayload()

    try:
        # Create a session
        s = requests.Session()
        # Make a post request within the session
        response = s.post(loginUrl, data=payload)
        data = BeautifulSoup(response.text, "html.parser")

        # Set some basic values like name and dob available in dashboard
        studentData = setBasicvalues(loginUrl, data)
        if not studentData:
            return {"success": False, "error": "Cannot login maybe invalid credentials"}

        # Get the html code of home page where attendance and CIE details are stored
        response = s.get(loginUrl + loginData.dash_url)
        subjects = BeautifulSoup(response.text, "html.parser").find("table", {
            "class": "dash_even_row uk-table uk-table-striped uk-table-hover cn-pay-table uk-table-middle uk-table-responsive"})
        if subjects is None:
            subjects = BeautifulSoup(response.text, "html.parser").find("table", {
                "class": "dash_od_row uk-table uk-table-striped uk-table-hover cn-pay-table uk-table-middle uk-table-responsive"})

        subjects = subjects.find_all('tr')
        for subject in subjects[1:]:
            subDict = {}
            links = subject.find_all('td')
            course_code = links[0].get_text()
            course_name = links[1].get_text()
            attendance_url = links[4].find("a")["href"]
            cie_url = links[5].find("a")["href"]
            subDict['name'] = course_name
            subDict['code'] = course_code
            print(f"Scraping {course_name}")
            subDict['attendance'] = get_attendance_data(
                s, loginUrl + attendance_url)
            subDict['cie'] = get_cie_data(s, loginUrl + cie_url)
            studentData['courses'].append(subDict)
        s.post(loginUrl, loginData.logoutPayload)
        return studentData
    except Exception:
        return {"success": False, "error": traceback.format_exc()}
