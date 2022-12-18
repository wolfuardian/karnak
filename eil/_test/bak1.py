def set_to(self):
    self.setObjectName('MainWindow')
    self.setWindowTitle('Karnak')
    display = 1
    screen_size = (1920, 1080)
    windows_size = (720, 640)
    pivot = (
        (display * screen_size[0]) + screen_size[0] / 2 - windows_size[0] / 2,
        screen_size[1] / 2 - windows_size[1] / 2
    )
    self.setGeometry(pivot[0], pivot[1], windows_size[0], windows_size[1])