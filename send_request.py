from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import controlBar


class send_request(ttk.Frame):

    def __init__(self, parent, controller, log):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.log = log
        self.information_entity = {}
        self.information = {}
        self.str_information = {}
        self.count = 0
        default_x = 100
        default_y = 150

        main_title = ttk.Frame(self, style='TFrame', width=1100, height=600)
        main_title.place(x=default_x, y=default_y)

        main_label = ttk.Label(self, text='요청하기', width=21, style='TButton', foreground="maroon", font="굴림 30")
        main_label.place(x=default_x, y=default_y)
        # id_start

        #   id_label_start
        x_st = 40
        x_nd = 140
        y_st = 130

        # label
        label_list = ['사유', '내용']
        self.size = len(label_list)
        for i in range(self.size):
            label = ttk.Label(self, text=label_list[i], style='TButton', width=9, foreground="maroon")
            label.place(x=default_x + x_st, y=default_y + y_st)

            if i == 0:
                self.information_entity[i] = Entry(self, font="굴림 20", width=50)
                self.information_entity[i].place(x=default_x + x_nd, y=default_y + y_st)

            else:
                self.information_entity[i] = Text(self, font="굴림 20", width=50, height=10)
                self.information_entity[i].place(x=default_x + x_nd, y=default_y + y_st)
            y_st += 60
        y_st += 300
        label_list = ['전송', '취소']
        default_x += 60
        for i, label_i in enumerate(label_list):
            default_x += 100
            if label_i == '전송':
                label = ttk.Button(self, text=label_list[i], width=15, style='TButton',
                                   command=self.insert)
            else:
                label = ttk.Button(self, text=label_list[i], width=15, style='TButton',
                                   command=self.home_put)
                label.bind("<Button-1>", self.clearTextInput)
            label.place(x=default_x, y=default_y + y_st)
            default_x += x_nd
        controlBar.controlBar(self)

    def home_put(self):
        job_log = {'관리자': lambda: self.controller.controller.show_frame('manager_login'),
                   '경비원': lambda: self.controller.controller.show_frame('security_login'),
                   '택배기사': lambda: self.controller.controller.show_frame('delivery_login'),
                   '주민': lambda: self.controller.controller.show_frame('residents_login')}
        if self.log[2] in job_log.keys():
            job_log[self.log[2]]()
        self.clearTextInput()

    def insert(self):
        try:
            self.controller.controller.cur.execute('select * from 요청목록')
            self.count = len(self.controller.controller.cur.fetchall())
        except:
            self.count = 0

        for i in range(self.size):
            if i == 0:
                self.information[i] = self.information_entity[i].get()
            else:
                self.information[i] = self.information_entity[i].get('1.0', END)
        b = list(self.information.values())
        b.insert(0, '/'.join(self.controller.controller.update_clock()[0:3]) + '-' + str(self.count))
        b.insert(1, self.log[0])
        b.append('X')


        b[3]=b[3].replace('\n', ' ')
        self.controller.controller.cur.execute('insert into 요청목록 values %s' % str(tuple(b)))
        self.controller.controller.cur.execute('commit')

        self.clearTextInput()

    def clearTextInput(self, event=0):
        for i in range(self.size):
            if i == 0:
                self.information_entity[i].delete(0, END)
            else:
                self.information_entity[i].delete('1.0', END)