import cv2
import tkinter as tk
from PIL import Image, ImageTk


class Application(tk.Frame):#GUIの設定
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.img_frame = tk.Frame(self, width=320, height=240)
        self.img_frame.grid(row=0, column=0)
        self.btn_frame = tk.Frame(self, width=80, height=240)
        self.btn_frame.grid(row=0, column=1, sticky = tk.N+tk.S)
        self.cnfirm_frame = tk.Frame(self, width=400, height=30)
        self.cnfirm_frame.grid(row=1, column=0, columnspan=2)
        self.button_frame = tk.Frame(self.cnfirm_frame)
        self.button_frame.pack(side='bottom')

        self.img_label = tk.Label(self.img_frame)
        self.img_label.pack()
        self.create_buttons()

        self.mode = 0

        img = cv2.imread("fig/load.png")
        img = cv2.resize(img,(300,300))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.img_label.imgtk = imgtk
        self.img_label.configure(image=imgtk)

        load_fig = cv2.imread("fig/white.png")
        cv2.putText(load_fig,"data nothing",(0,100),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3,1)
        cv2.imwrite("fig/fig.png",load_fig)



    def set_image(self, img):
        if self.mode == 0:
            # OpenCVのBGR画像をRGBに変換
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.img_label.imgtk = imgtk
            self.img_label.configure(image=imgtk)
        else:
            img = cv2.imread("fig/fig.png")
            img = cv2.resize(img,(320,240))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.img_label.imgtk = imgtk
            self.img_label.configure(image=imgtk)


    def switch_mode(self):
        self.mode = (self.mode+1) % 2
        if self.mode == 1:
            self.change_button["text"] = 'ビデオ表示'
        else:
            self.change_button["text"] = 'グラフ表示'

    def create_buttons(self):
        self.quit_button = tk.Button(self.btn_frame)
        self.quit_button["text"] = "Quit"
        self.quit_button["command"] = self.master.destroy  # Quitボタンをクリックするとウィンドウが閉じる
        self.quit_button["bg"] = "red" 
        self.quit_button.pack(side='bottom')

        #グラフとの切り替え
        self.change_button = tk.Button(self.btn_frame)
        self.change_button["text"] = '表示画像切り替え'
        self.change_button["command"] = self.switch_mode
        self.change_button.pack(side='top', pady=10)
        # アラーム停止ボタン（最初は非表示）
        self.alarm_stop_button = tk.Button(self.btn_frame)
        self.alarm_stop_button["text"] = "Stop Alarm"

        #imgのモード切替(顔が映るかどうか)
        self.img_change_button = tk.Button(self.btn_frame)
        self.img_change_button["text"] = "顔を映さない"
        self.img_change_button.pack(side='top', pady=10)
        self.img_change_button["command"] = self.img_change

        #休憩するか尋ねる文章
        self.rest_question = tk.Label(self.cnfirm_frame,text = "休憩しますか？")

        #休憩か続行かを選択するボタン
        self.rest_button = tk.Button(self.button_frame, text="Rest")
        self.continue_button = tk.Button(self.button_frame, text="Continue")

        validate_command = self.register(self.validate_input)
        #休憩時間を入力する
        var = tk.StringVar(self.button_frame)
        self.entry = tk.Entry(self.button_frame, textvariable=var, validate="key", validatecommand=(validate_command, '%P'),width = 3)
        self.label = tk.Label(self.button_frame, text="分")

        self.button = tk.Button(self.button_frame, text="Get Input", command=self.get_input)

        #休憩からの復帰 OKボタン
        self.confirm_label = tk.Label(self.cnfirm_frame, text="休憩から復帰する場合はOKボタンを押してください")
        self.ok_button = tk.Button(self.cnfirm_frame, text = "OK")


    def img_set(self, landmark):
        self.landmark = landmark
        self.img_mode = 0


    def img_change(self):
        self.landmark.change_mode()
        self.img_mode = (self.img_mode+1) % 2
        if self.img_mode == 1:
            self.img_change_button["text"] = "顔を映す"
        else:
            self.img_change_button["text"] = "顔を映さない"


    def show_alarm_button(self):  # アラームボタンを表示する
        self.rest_button.pack(side='left', padx=10)
        self.continue_button.pack(side='right', padx=10)
        self.rest_question.pack(side='bottom')


    def hide_alarm_button(self):  # アラームボタンを非表示にする
        self.rest_button.pack_forget()
        self.continue_button.pack_forget()
        self.rest_question.pack_forget()


    def update_image(self, img):
        self.master.after(0, self.set_image, img)


    ############################alarmで休憩か継続か###############################################
    def take_rest(self):
        # Restボタンがクリックされたときの処理
        self.entry.pack(side='left')
        self.label.pack(side='left')
        self.button.pack(side='right',padx=10)
        self.hide_alarm_button()
        print("Resting...")
        

    ##################休憩時間の入力###############
    def get_input(self):
        input_value = self.entry.get()
        #print(input_value)
        self.entry.pack_forget()
        self.label.pack_forget()
        self.button.pack_forget()
        if not input_value:
            print("string is empty")
            self.value = 0
        else:
            self.value = int(input_value)
        self.rest.set_value(self.value)
    
    def reset_value(self):
        del self.value

    def validate_input(self,input_str):
        return input_str.isdigit() or input_str == ''
    
    def add_setting(self,rest):
        self.rest = rest
