import tkinter,webbrowser,requests,json,jdatetime,datetime
from tkinter import ttk,END,ANCHOR
from bs4 import BeautifulSoup
from tkcalendar import DateEntry

#Define time
now = datetime.datetime.now()
now = jdatetime.date.fromgregorian(day=now.day,month=now.month,year=now.year)

#Define window
root = tkinter.Tk()
root.title('Tasnim News')
root.iconbitmap('D:\\Project\\tkinter\\News scraping 2\\img\\news.ico')
root.geometry('700x500')
root.resizable(0,0)
root.config(bg=root_color)

#Define fonts and colors
my_font = ('Times New Roman',12)
root_color = '#6c1cbc'
button_color = '#e2cff4'

category_dict ={
'Political':1,
'Sports':3,
'International':8,
'Economic':7,
'Social':2,
'Cultural':4,
'Provinces':6,
'Media':9,
'Market': 1407}

#Define Functions
def open_link():
    """Open link """
    for i in my_listbox.curselection():
        webbrowser.open(my_listbox.get(i))


def clear_list():
    """Delete all items from the listbox """
    my_listbox.delete(0,END)

def save_as():
    """Save the list to a simple txt file """
    with open('newsData.txt','wb') as f:
        list_tuple = my_listbox.get(0,END)
        for item in list_tuple:
            item = item.encode('utf8')
            f.write(item+'\n'.encode())

def show_item():
    """Add items to listbox """
    temp = calander.get_date()
    datetime = jdatetime.date.fromgregorian(day=temp.day,month=temp.month,year=temp.year)
    year = datetime.year
    month = str(datetime.month).zfill(2)
    day = str(datetime.day).zfill(2)
    service = str(category_dict[input_comobox.get()])
    url =f"https://www.tasnimnews.com/fa/archive?service={service}&sub=-1&date={year}%2F{month}%2F{day}"
    req = requests.get(url)
    soup = BeautifulSoup(req.content,'html.parser')
    rows = soup.select('.news-container.archive-result .content .list-item')
    dataset = []
    for row in rows:
        d = dict()
        d['title'] = row.select_one('.title').text.strip()
        d['summary'] = row.select_one('.lead').text.strip()
        d['link'] = 'https://www.tasnimnews.com' + row.select_one('a')['href']
        dataset.append(d)
    for data in dataset:
        my_listbox.insert(END,data['title'])
        my_listbox.insert(END,data['link'])
    print(url)

#Define layout
#Create frames
input_frame = tkinter.Frame(root,bg=root_color)
output_frame = tkinter.LabelFrame(root,bg=root_color,text='Today :' + str(now),fg='white')
button_frame = tkinter.Frame(root,bg=root_color)
input_frame.pack()
output_frame.pack()
button_frame.pack()

#Input Frame Layout
input_comobox = ttk.Combobox(input_frame,value=list(category_dict.keys()),font=my_font)
input_comobox.grid(row=0,column=2,padx=10,pady=10)
input_comobox.set('Service Selection')

calander = DateEntry(input_frame,width=10,font=my_font,background=button_color,forground='#ffffff')
calander.grid(row=0,column=1,padx=10,pady=10)

btn_search = tkinter.Button(input_frame,font=my_font,bg=button_color,text='Search',width=10,command=show_item)
btn_search.grid(row=0,column=0,padx=10,pady=10)

#Output Frame Layout
my_scrollbar = tkinter.Scrollbar(output_frame)
my_listbox = tkinter.Listbox(output_frame,height=18,width=80,borderwidth=3,font=my_font,yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_listbox.yview)
my_listbox.grid(row=0,column=0)
my_scrollbar.grid(row=0,column=1,sticky='NS')

#Button Frame Layout
openLink_button = clear_button= tkinter.Button(button_frame,text='Open Link',borderwidth=2,bg=button_color,font=my_font,command=open_link)
clear_button= tkinter.Button(button_frame,text='Clear List',borderwidth=2,bg=button_color,font=my_font,command=clear_list)
save_button = tkinter.Button(button_frame,text='Save List',borderwidth=2,bg=button_color,font=my_font,command=save_as)
quit_button = tkinter.Button(button_frame,text='Quit',borderwidth=2,bg=button_color,font=my_font,command=root.destroy)
openLink_button.grid(row=0,column=0,padx=5,pady=5)
clear_button.grid(row=0,column=1,padx=5,pady=5)
save_button.grid(row=0,column=2,padx=5,pady=5)
quit_button.grid(row=0,column=3,padx=5,pady=5)

#Run the root windows's main loop
root.mainloop()
