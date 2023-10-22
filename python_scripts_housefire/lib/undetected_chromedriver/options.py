from undetected_chromedriver import ChromeOptions


class Options(ChromeOptions):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.headless: bool = False
