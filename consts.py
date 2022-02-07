class LoginParams:
    loginPayload = {"dd": "", "mm": "", "option": "com_user", "passwd": "", "remember": "No", "task": "login",
                    "username": "", "yyyy": ""}
    baseUrl = "http://parents.msrit.edu/"
    dash_url = "index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard"
    logoutPayload = {"option": "com_user", "task": "logout", "return": "�w^Ƙi"}

    def __init__(self, usn, dob):
        self.loginPayload['yyyy'], self.loginPayload['mm'], self.loginPayload['dd'] = dob.split("-")
        self.loginPayload['username'] = usn.lower()
        self.loginPayload['passwd'] = dob

    def getLoginPayload(self) -> dict:
        return self.loginPayload

    def getLoginUrl(self, isfirstyear):
        if isfirstyear:
            return self.baseUrl + "parents_even2021/"
        return self.baseUrl
