class SessionHelper:

    def __init__(self, app):
        self.app = app


    def login(self, username, password):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_name("userEmail").click()
        wd.find_element_by_name("userEmail").clear()
        wd.find_element_by_name("userEmail").send_keys(username)
        wd.find_element_by_name("userPassword").click()
        wd.find_element_by_name("userPassword").clear()
        wd.find_element_by_name("userPassword").send_keys(password)
        wd.find_element_by_id("loginButton").click()


    def logout(self):
        wd = self.app.wd
        self.app.open_home_page()
        wd.find_element_by_link_text("Logout").click()




