import requests
import json
from tkinter import ttk
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb


def get_token ():
    value = need_token.get()
    need_token.delete(0, tk.END)
    return value

logwin=tk.Tk()
photo = tk.PhotoImage(file="icon.png")
logwin.iconphoto(False, photo)
logwin.config(bg='#25db7a')
logwin.title("Сканирование чеков")
logwin.geometry(f"450x250+100+100")
logwin.minsize(300,400)
#logwin.maxsize(1200,600)
logwin.resizable(True, True)

tk.Label(logwin, text='Токен: ').grid(row=0, column=0, stick='we')
need_token=tk.Entry(logwin)
need_token.grid(row=0, column=1, stick='we')
tk.Button(logwin, text="Ввести", activebackground="grey", command=get_token).grid(row=0, column=2, stick='we')
logwin.grid_columnconfigure(0,minsize=150)
logwin.grid_columnconfigure(1,minsize=170)
logwin.grid_columnconfigure(2,minsize=150)


menubar = tk.Menu(logwin)
logwin.config(menu=menubar)
def opennewdialog():
    newbox = mb.showinfo(title='Справка', message=""" Для получения токена зарегистируйтесь на сайте proverkacheka.com .
    В разделе "Личный кабинет" получите токен доступа к API.
    Программа Арефьева А. Курсовая работа за 4 семестр.
    """)
menubar.add_command(label='Справка', command=opennewdialog)

def openfn():
    filename = filedialog.askopenfilename(title='Выберите файл jpg', filetypes=[('*.jpeg *.jpg')])

    url = 'https://proverkacheka.com/api/v1/check/get'
    data = {'token': '14023.uQ0uGby7nN3VXKV99'}
    print(filename)
    files = {'qrfile': open(filename, 'rb')}
    r = requests.post(url, data=data, files=files)
    py_data = json.loads(r.text)

    tempList = []

    with open('try_fujson.json', 'w') as f:
        json.dump(py_data, f, indent=3, ensure_ascii=False)

    with open("try_fujson.json") as jsonFile:
        data1 = json.load(jsonFile)
        jsonItems = data1["data"]["json"]["items"]

    for item in data1["data"]["json"]["items"]:
        if (item == ['nds']):
            del item['nds']
        if (item == ['ndsSum']):
            del item['ndsSum']
        if (item == ['paymentType']):
            del item['paymentType']
        if (item == ['modifiers']):
            del item['modifiers']
        tempList.append([item['name'], item['sum'], item['price']])
    print(tempList)

    logwin.geometry(f"800x550+100+100")


    def show():
        for i, (name, sum, price) in enumerate(tempList, start=1):
            listBox.insert("", "end", values=(i, name, sum, price))


    cols = ('№','Название', 'Сумма', 'Цена')
    listBox = ttk.Treeview(logwin, columns=cols, show='headings', )
    for col in cols:
        listBox.heading(col, text=col)
    listBox.grid(row=3, column=0, columnspan=3)
    showScores = tk.Button(logwin, text="Показать данные чека", width=20, command=show).grid(row=4, column=1)


    return filename

def open_img():
    x = openfn()
    img = Image.open(x)
    img = img.resize((230, 230), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(logwin, image=img)
    panel.image = img
    panel.grid(row=1, column=1, stick='we')


btn_load = tk.Button(logwin, text='Загрузить фото чека',
                 bg="white",
                 fg="Black",
                 activebackground="grey",
                 command=open_img
                 ).grid(row=2, column=0, pady= 25, columnspan=3,rowspan=2, stick='s')

logwin.mainloop()
