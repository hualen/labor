import tkinter as tk
from tkinter.constants import CENTER
win = tk.Tk() # 如果使用直譯器的話，在這行Enter後就會先看到一個視窗了！
win.title('點餐機') # 更改視窗的標題
win.geometry('720x640') # 修改視窗大小(寬x高)
win.resizable(False, False) # 如果不想讓使用者能調整視窗大小的話就均設為False



num_egg1 = tk.IntVar()
num_egg1.set(0)
num_tea1 = tk.IntVar()
num_tea1.set(0)
num_puff1 = tk.IntVar()
num_puff1.set(0)

num_egg2 = tk.IntVar()
num_egg2.set(0)
num_tea2 = tk.IntVar()
num_tea2.set(0)
num_puff2 = tk.IntVar()
num_puff2.set(0)

num_egg3 = tk.IntVar()
num_egg3.set(0)
num_tea3 = tk.IntVar()
num_tea3.set(0)
num_puff3 = tk.IntVar()
num_puff3.set(0)

num_egg4 = tk.IntVar()
num_egg4.set(0)
num_tea4 = tk.IntVar()
num_tea4.set(0)
num_puff4 = tk.IntVar()
num_puff4.set(0)

final_order = [ [0,0,0],
                [0,0,0],
                [0,0,0],
                [0,0,0]  ]

def add(item):
    if item.get() < 9:
        item.set(item.get()+1)
    else:
        pass
def sub(item):
    if item.get() > 0:
        item.set(item.get()-1)
    else:
        pass

def clear_window():
    for widget in win.winfo_children():
        widget.destroy()    

def finish():
    # 奇趣蛋
    final_order[0][0] = num_egg1.get()
    final_order[0][1] = num_tea1.get()
    final_order[0][2] = num_puff1.get()
    # 麥香
    final_order[1][0] = num_egg2.get()
    final_order[1][1] = num_tea2.get()
    final_order[1][2] = num_puff2.get()
    # 泡芙
    final_order[2][0] = num_egg3.get()
    final_order[2][1] = num_tea3.get()
    final_order[2][2] = num_puff3.get()
    
    final_order[3][0] = num_egg4.get()
    final_order[3][1] = num_tea4.get()
    final_order[3][2] = num_puff4.get()
    
    total_egg = final_order[0][0] + final_order[1][0] + final_order[2][0] + final_order[3][0]
    total_tea = final_order[0][1] + final_order[1][1] + final_order[2][1] + final_order[3][1]
    total_puff = final_order[0][2] + final_order[1][2] + final_order[2][2] + final_order[3][2]
    if total_egg > 9 or total_tea > 9 or total_puff > 9:
        clear_window()
        retext = tk.Label(win,text='物品需求超過庫存!\n請重新下訂!',font=('標楷體',32))
        retext.place(x=360,y=200,anchor=CENTER)
        resbutton = tk.Button(win,text="重新下訂",font=('Time New Roman',28),command = restart)
        resbutton.place(x=360,y=350,anchor=CENTER)
    elif total_egg == 0 and total_tea == 0 and total_puff == 0:
        clear_window()
        retext = tk.Label(win,text='訂單內無任何物品!\n請重新下訂!',font=('標楷體',32))
        retext.place(x=360,y=200,anchor=CENTER)
        resbutton = tk.Button(win,text="重新下訂",font=('Time New Roman',28),command = restart)
        resbutton.place(x=360,y=350,anchor=CENTER)
    else:
        win.destroy()
        return final_order
    
def restart() :
    clear_window()

    num_egg1.set(0)
    num_tea1.set(0)
    num_puff1.set(0)

    num_egg2.set(0)
    num_tea2.set(0)
    num_puff2.set(0)

    num_egg3.set(0)
    num_tea3.set(0)
    num_puff3.set(0)

    num_egg4.set(0)
    num_tea4.set(0)
    num_puff4.set(0)

    title = tk.Label(win,text='瘋狂吉娃娃的自助點餐機',bg = 'black',
                    fg = 'white',font=('標楷體',40))
    title.place(x=360,y=30,anchor=CENTER)
    order1()

def order1():
    start.destroy()
    last_order.destroy()
    # 訂單
    order = tk.Label(win,text='訂單1',font=('標楷體',32))
    order.place(x=360,y=110,anchor=CENTER)
    # 奇趣蛋
    egg = tk.Label(win,text='奇趣蛋',font=('標楷體',32))
    egg.place(x=120,y=200,anchor=CENTER)

    add1 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_egg1))
    add1.place(x=300,y=200,anchor=CENTER)

    negg = tk.Label(win,textvariable=num_egg1,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    negg.place(x=450,y=200,anchor=CENTER)

    sub1 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_egg1))
    sub1.place(x=600,y=200,anchor=CENTER)

    # 麥香
    tea = tk.Label(win,text='麥香紅茶',font=('標楷體',32))
    tea.place(x=120,y=290,anchor=CENTER)

    add2 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_tea1))
    add2.place(x=300,y=290,anchor=CENTER)

    ntea = tk.Label(win,textvariable=num_tea1,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    ntea.place(x=450,y=290,anchor=CENTER)

    sub2 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_tea1))
    sub2.place(x=600,y=290,anchor=CENTER)

    # 泡芙
    puff = tk.Label(win,text='泡芙',font=('標楷體',32))
    puff.place(x=120,y=380,anchor=CENTER)

    add3 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_puff1))
    add3.place(x=300,y=380,anchor=CENTER)

    npuff = tk.Label(win,textvariable=num_puff1,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    npuff.place(x=450,y=380,anchor=CENTER)

    sub3 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_puff1))
    sub3.place(x=600,y=380,anchor=CENTER)
    
    # 下一筆
    next_order = tk.Button(win,text="下一筆",font=('標楷體',28),command=order2)
    next_order.place(x=600,y=520,anchor=CENTER)

def order2():
    global last_order
    last_order.destroy()
    # 訂單
    order = tk.Label(win,text='訂單2',font=('標楷體',32))
    order.place(x=360,y=110,anchor=CENTER)
    # 奇趣蛋
    egg = tk.Label(win,text='奇趣蛋',font=('標楷體',32))
    egg.place(x=120,y=200,anchor=CENTER)

    add1 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_egg2))
    add1.place(x=300,y=200,anchor=CENTER)

    negg = tk.Label(win,textvariable=num_egg2,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    negg.place(x=450,y=200,anchor=CENTER)

    sub1 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_egg2))
    sub1.place(x=600,y=200,anchor=CENTER)

    # 麥香
    tea = tk.Label(win,text='麥香紅茶',font=('標楷體',32))
    tea.place(x=120,y=290,anchor=CENTER)

    add2 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_tea2))
    add2.place(x=300,y=290,anchor=CENTER)

    ntea = tk.Label(win,textvariable=num_tea2,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    ntea.place(x=450,y=290,anchor=CENTER)

    sub2 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_tea2))
    sub2.place(x=600,y=290,anchor=CENTER)

    # 泡芙
    puff = tk.Label(win,text='泡芙',font=('標楷體',32))
    puff.place(x=120,y=380,anchor=CENTER)

    add3 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_puff2))
    add3.place(x=300,y=380,anchor=CENTER)

    npuff = tk.Label(win,textvariable=num_puff2,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    npuff.place(x=450,y=380,anchor=CENTER)

    sub3 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_puff2))
    sub3.place(x=600,y=380,anchor=CENTER)
    
    # 下一筆
    next_order = tk.Button(win,text="下一筆",font=('標楷體',28),command=order3)
    next_order.place(x=600,y=520,anchor=CENTER)
    
    # 上一筆
    last_order = tk.Button(win,text="上一筆",font=('標楷體',28),command=order1)
    last_order.place(x=120,y=520,anchor=CENTER)
    
def order3():
    global last_order
    fin_order.destroy()
    last_order.destroy()
    # 訂單
    order = tk.Label(win,text='訂單3',font=('標楷體',32))
    order.place(x=360,y=110,anchor=CENTER)
    # 奇趣蛋
    egg = tk.Label(win,text='奇趣蛋',font=('標楷體',32))
    egg.place(x=120,y=200,anchor=CENTER)

    add1 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_egg3))
    add1.place(x=300,y=200,anchor=CENTER)

    negg = tk.Label(win,textvariable=num_egg3,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    negg.place(x=450,y=200,anchor=CENTER)

    sub1 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_egg3))
    sub1.place(x=600,y=200,anchor=CENTER)

    # 麥香
    tea = tk.Label(win,text='麥香紅茶',font=('標楷體',32))
    tea.place(x=120,y=290,anchor=CENTER)

    add2 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_tea3))
    add2.place(x=300,y=290,anchor=CENTER)

    ntea = tk.Label(win,textvariable=num_tea3,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    ntea.place(x=450,y=290,anchor=CENTER)

    sub2 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_tea3))
    sub2.place(x=600,y=290,anchor=CENTER)

    # 泡芙
    puff = tk.Label(win,text='泡芙',font=('標楷體',32))
    puff.place(x=120,y=380,anchor=CENTER)

    add3 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_puff3))
    add3.place(x=300,y=380,anchor=CENTER)

    npuff = tk.Label(win,textvariable=num_puff3,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    npuff.place(x=450,y=380,anchor=CENTER)

    sub3 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_puff3))
    sub3.place(x=600,y=380,anchor=CENTER)
    
    # 下一筆
    next_order = tk.Button(win,text="下一筆",font=('標楷體',28),command=order4)
    next_order.place(x=600,y=520,anchor=CENTER)
    
    # 上一筆
    last_order = tk.Button(win,text="上一筆",font=('標楷體',28),command=order2)
    last_order.place(x=120,y=520,anchor=CENTER)

def order4():
    global fin_order,last_order
    last_order.destroy()
    # 訂單
    order = tk.Label(win,text='訂單4',font=('標楷體',32))
    order.place(x=360,y=110,anchor=CENTER)
    # 奇趣蛋
    egg = tk.Label(win,text='奇趣蛋',font=('標楷體',32))
    egg.place(x=120,y=200,anchor=CENTER)

    add1 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_egg4))
    add1.place(x=300,y=200,anchor=CENTER)

    negg = tk.Label(win,textvariable=num_egg4,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    negg.place(x=450,y=200,anchor=CENTER)

    sub1 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_egg4))
    sub1.place(x=600,y=200,anchor=CENTER)

    # 麥香
    tea = tk.Label(win,text='麥香紅茶',font=('標楷體',32))
    tea.place(x=120,y=290,anchor=CENTER)

    add2 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_tea4))
    add2.place(x=300,y=290,anchor=CENTER)

    ntea = tk.Label(win,textvariable=num_tea4,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    ntea.place(x=450,y=290,anchor=CENTER)

    sub2 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_tea4))
    sub2.place(x=600,y=290,anchor=CENTER)

    # 泡芙
    puff = tk.Label(win,text='泡芙',font=('標楷體',32))
    puff.place(x=120,y=380,anchor=CENTER)

    add3 = tk.Button(win,text="+",font=('Time New Roman',28),command=lambda:add(num_puff4))
    add3.place(x=300,y=380,anchor=CENTER)

    npuff = tk.Label(win,textvariable=num_puff4,bg = '#E0E0E0',font=('Time New Roman',28)
                    ,padx= 90)
    npuff.place(x=450,y=380,anchor=CENTER)

    sub3 = tk.Button(win,text="-",font=('Time New Roman',28),command=lambda:sub(num_puff4))
    sub3.place(x=600,y=380,anchor=CENTER)
    
    # 結束
    fin_order = tk.Button(win,text="完成訂單",font=('標楷體',28),command=finish)
    fin_order.place(x=600,y=520,anchor=CENTER)
    
    # 上一筆
    last_order = tk.Button(win,text="上一筆",font=('標楷體',28),command=order3)
    last_order.place(x=120,y=520,anchor=CENTER)        

def start_order():
    global  start,next_order,last_order,fin_order  
    # 標題
    title = tk.Label(win,text='瘋狂吉娃娃的自助點餐機',bg = 'yellow',font=('標楷體',40),padx=720)
    title.place(x=360,y=30,anchor=CENTER)

    next_order = tk.Button(win,text="下一筆",font=('標楷體',28))
    last_order = tk.Button(win,text="上一筆",font=('標楷體',28))
    fin_order = tk.Button(win,text="完成訂單",font=('標楷體',28),command=finish)

    start = tk.Button(win,text="開始點餐",font=('Time New Roman',28),command=order1)
    start.place(x=360,y=320,anchor=CENTER)

    win.mainloop() # 在一般python xxx.py的執行方式中，呼叫mainloop()才算正式啟動
    return(fin_order)
    
if __name__ == '__main__'  :
    start_order()
    