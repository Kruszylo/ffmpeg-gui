#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

from mainwindow import Application
from mainwindow import is_tool
def main():
    app = Application(None)
    print(app.initialize().__doc__)
    print(is_tool('').__doc__)
    app.title("FFmpeg")
    app.mainloop()


if __name__ == "__main__":
    main()
