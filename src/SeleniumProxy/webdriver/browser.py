from selenium.webdriver import Chrome as _Chrome


class Chrome(_Chrome):

    def __init__(self, *args, options=None, **kwargs):
        print("init")
        super().__init__(*args, **kwargs)

    def quit(self):
        super().quit()