import requests
import tkinter as tk
from tkinter import filedialog
from app.config.constants import port, host


def select_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()


def upload_file(file_path="", url=''.join(["http://", host, ':', port, "/upload"])):
    if not file_path:
        file_path = select_file()
    r = requests.post(url,
                      files={
                          'file': (file_path.split('/')[-1],
                                   open(file_path, "rb"),
                                   {'Expires': '0'})})
    return r.text


