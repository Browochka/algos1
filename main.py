import random
import pandas as pd
import datetime
import tkinter
from tkinter.ttk import Entry
supermarket=[]
alcohol=[]
books=[]
electronics=[]

shops=[]
with open('shops.txt','r',encoding='utf-8') as f:
    f.seek(0)
    for i in f:
        t = i.split(' | ')
        t[2]=t[2][:-2]

        shops.append(t)

with open('products.txt','r',encoding='utf-8') as f:
    for i in f:
        t = i.split(' | ')
        t[3]=t[3].rstrip()
        t[3] = int(''.join([char for char in t[3] if char.isdigit()]))


        if t[0]=='alcohol':
            alcohol.append([t[1],t[2],t[3]])
        elif t[0]=='supermarket':
            supermarket.append([t[1], t[2], t[3]])
        elif t[0]=='books':
            books.append([t[1], t[2], t[3]])
        elif t[0]=='electronics':
            electronics.append([t[1], t[2], t[3]])



def num_of_card(pay_system, bank):
    card_format = '{fig} {fig2} {fig3} {fig4}'

    if pay_system == 'Мир':
        if bank == 'Сбербанк':
            figures = '2202'
        elif bank == 'Тинькофф':
            figures = '2200'
        elif bank == 'ВТБ':
            figures = '2204'
        else:
            figures = '2206'
    elif pay_system == 'MasterCard':
        if bank == 'Сбербанк':
            figures = '5469'
        elif bank == 'Тинькофф':
            figures = '5489'
        elif bank == 'ВТБ':
            figures = '5443'
        else:
            figures = '5406'
    else:
        if bank == 'Сбербанк':
            figures = '4276'
        elif bank == 'Тинькофф':
            figures = '4277'
        elif bank == 'ВТБ':
            figures = '4272'
        else:
            figures = '4279'

    argz = {'fig': figures,
            'fig2': str(random.randint(1000, 9999)),
            'fig3': str(random.randint(1000, 9999)),
            'fig4': str(random.randint(1000, 9999))}

    return card_format.format(**argz)

def form_purchases(category,amount):
    purchases=[]
    money=0
    brand=[]
    temp=[]

    if category=='alcohol':
        temp=random.choices(alcohol,k=amount)
    elif category=='supermarket':
        temp=random.choices(supermarket,k=amount)
    elif category=='books':
        temp=random.choices(books,k=amount)
    elif category=='electronics':
        temp=random.choices(electronics,k=amount)
    for i in temp:
        purchases.append(i[1])
        brand.append(i[0])
        money+=i[2]
    return [set(brand),set(purchases),money]

def gen_time():
    start_date = datetime.datetime(2023, 1, 1, 9, 0, 0)  # 1 января 2023, 9:00
    end_date = datetime.datetime(2024, 9, 9, 22, 0, 0)  # 9 сентября 2024, 22:00

    # Генерируем случайную дату в диапазоне
    random_date = start_date + (end_date - start_date) * random.random()

    # Корректируем время, чтобы оно попадало в диапазон от 9:00 до 22:00
    if random_date.hour < 9:
        random_date = random_date.replace(hour=random.randint(9,21), minute=random.randint(0,59), second=random.randint(0,59))
    elif random_date.hour > 22:
        random_date = random_date.replace(hour=random.randint(9,21), minute=random.randint(0,59), second=random.randint(0,59))
    return random_date


def gen_dataset(MC, Visa, Mir, Sb, Tk, Vtb, Alp, size):
    ds=pd.DataFrame({'Магазин':[],'Координаты':[],'Время покупки':[],'Категории':[],'Бренды':[],'Номер карточки':[],'Количество товаров':[],'Стоимость покупок':[]})
    for i in range(size):
        print(i)
        temp1=random.choice(shops)
        coord=temp1[1]
        shop=temp1[0]
        timing=gen_time()
        amount=random.randint(5,25)
        temp2=form_purchases(temp1[2],amount)
        category=temp2[0]
        brands=temp2[1]
        money=temp2[2]
        bank = random.choices(['Сбербанк', 'Тинькофф', 'ВТБ', 'Альфа'], weights=[Sb, Tk, Vtb, Alp])[0]
        pay_system = random.choices(['Мир', 'MasterCard', 'Visa'], weights=[Mir, MC, Visa])[0]
        card=num_of_card(pay_system,bank)

        ds.loc[len(ds.index)]=[shop,coord,timing,category,brands,card,amount,money]
    ds.to_csv('purchases.csv', index=False)

def click():
    try:
        #if entrys < 50000:
         #   return

        gen_dataset(int(entry1.get()),int(entry2.get()),int(entry3.get()),int(entry4.get()),int(entry5.get()),int(entry6.get()),int(entry7.get()),int(entrys.get()))
        lk = tkinter.Label(root, text='Датасет сгенерирован', font='Arial 11')
        lk.place(relx=0.5, rely=0.65, anchor='center')
    except:
        lk = tkinter.Label(root, text='Не смогли сгенерировать. Генерируем по умолчанию.', font='Arial 11')
        lk.place(relx=0.5, rely=0.65, anchor='center')
        gen_dataset(1,1,1,1,1,1,1,50000)

root = tkinter.Tk()
root.geometry('450x500')
l=tkinter.Label(root,text='Введите значения',font='Arial 16 bold')
l.place(relx=0.5, rely=0.1, anchor='center')

l1=tkinter.Label(root,text='MC',font='Arial 11')
l1.place(relx=0.3, rely=0.15, anchor='center')
entry1=tkinter.ttk.Entry()
entry1.place(relx=0.5, rely=0.15, anchor='center')

l2=tkinter.Label(root,text='Visa',font='Arial 11')
l2.place(relx=0.3, rely=0.19, anchor='center')
entry2=tkinter.ttk.Entry()
entry2.place(relx=0.5, rely=0.19, anchor='center')

l3=tkinter.Label(root,text='Мир',font='Arial 11')
l3.place(relx=0.3, rely=0.23, anchor='center')
entry3=tkinter.ttk.Entry()
entry3.place(relx=0.5, rely=0.23, anchor='center')

l4=tkinter.Label(root,text='Сбер',font='Arial 11')
l4.place(relx=0.3, rely=0.29, anchor='center')
entry4=tkinter.ttk.Entry()
entry4.place(relx=0.5, rely=0.29, anchor='center')

l5=tkinter.Label(root,text='Тиньк',font='Arial 11')
l5.place(relx=0.3, rely=0.33, anchor='center')
entry5=tkinter.ttk.Entry()
entry5.place(relx=0.5, rely=0.33, anchor='center')

l6=tkinter.Label(root,text='ВТБ',font='Arial 11')
l6.place(relx=0.3, rely=0.37, anchor='center')
entry6=tkinter.ttk.Entry()
entry6.place(relx=0.5, rely=0.37, anchor='center')

l7=tkinter.Label(root,text='Альфа',font='Arial 11')
l7.place(relx=0.3, rely=0.41, anchor='center')
entry7=tkinter.ttk.Entry()
entry7.place(relx=0.5, rely=0.41, anchor='center')

ls=tkinter.Label(root,text='Введите размер таблицы',font='Arial 16 bold')
ls.place(relx=0.5, rely=0.48, anchor='center')
entrys=tkinter.ttk.Entry()
entrys.place(relx=0.5, rely=0.54, anchor='center')

button=tkinter.Button(root,text='Создать',command=click)
button.place(relx=0.5,rely=0.6,anchor='center')

root.mainloop()
