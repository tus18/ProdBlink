import cv2
import time
import tkinter as tk
import threading
from Application import Application
from Fatigue import Fatigue
from Landmark import Landmark
from First import UserSelection
from Setting import EyeTracker


username = None

def main_thread(app):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    cap.set(cv2.CAP_PROP_FPS, 30)

    landmark = Landmark()
    fatigue = Fatigue()
    rest = Rest()

    rest.setting(fatigue,app)

    # ボタンが押されたらアラームを停止するようにコマンドを設定
    app.continue_button["command"] = fatigue.alarm_end
    app.rest_button["command"] = rest.rest
    app.img_set(landmark)

    fatigue.setting(username)
    print("user:",username)

    last_update_time = time.time()
    while True:
        _, img = cap.read()
        eye,img = landmark.face_landmark_find(img)
        count,flag = fatigue(eye)
        cv2.putText(img,str(count),(10,200),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3,1)
        cv2.putText(img,str(flag),(220,200),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),3,1)#テスト用
        
        # 60msごとに画像を更新
        try:
            if time.time() - last_update_time > 0.06:
                app.update_image(img)
                last_update_time = time.time()

            if fatigue.is_alarm_on:  # アラームが鳴っている場合
                app.show_alarm_button()  # アラーム停止ボタンを表示

            else:  # アラームが鳴っていない場合
                app.hide_alarm_button()  # アラーム停止ボタンを非表示に

        except Exception as e:#メインプロセスが終了している時
            break

        if rest.resting == True:
            time.sleep(rest.value)
            fatigue.alarm()
            app.ok_button.pack(side='bottom')
            app.ok_button["command"] = rest.rest_end
            app.confirm_label.pack(side='bottom')
            while True:
                if rest.resting == False:
                    break
            app.ok_button.pack_forget()
            app.confirm_label.pack_forget()
            fatigue.alarm_end()

    fatigue.end_process()
    print("exit success")
    cap.release()


class Rest:
    def setting(self,fatigue,app):
        self.fatigue = fatigue
        self.app = app
        app.add_setting(self)
        self.resting = False

    def rest(self):
        self.fatigue.alarm_end()
        self.app.take_rest()
        
    def set_value(self,v):
        self.value = v * 60
        self.resting = True
    
    def rest_end(self):
        self.resting = False



if __name__ == '__main__':
    user_selection = UserSelection()
    username = user_selection.get_username()
    print(username)  # ここで選択したユーザ名が出力されます
    if user_selection.is_new:
        e = EyeTracker()
        e.set_fname(username)
        e.window.mainloop()

    root = tk.Tk()
    
    app = Application(master=root)

    # メインループを別スレッドで実行
    thread = threading.Thread(target=main_thread, args=(app,))
    thread.start()

    # GUIループを実行
    root.mainloop()
