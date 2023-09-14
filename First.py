import os
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


class UserSelection:
    def __init__(self):
        self.username = None
        self.is_new = False

    def get_users(self):
        return [os.path.splitext(f)[0] for f in os.listdir("./user/") if os.path.isfile(os.path.join("./user/", f))]

    def choose_user(self):
        window = tk.Tk()
        window.title("Choose a user")

        users = self.get_users()

        var = tk.StringVar()

        for user in users:
            tk.Radiobutton(window, text=user, variable=var, value=user).pack()

        tk.Radiobutton(window, text="新しく登録する", variable=var, value="new").pack()

        def command():
            selected = var.get()

            if selected == "new":
                new_user = simpledialog.askstring("新規ユーザ", "ユーザ名を入力してください")
                selected = f"{new_user}"
                self.is_new = True

            if selected:  # If a selection has been made
                window.destroy()
                self.username = selected
            else:  # If no selection has been made
                messagebox.showwarning("Warning", "ユーザを選択してください")

        tk.Button(window, text="選択", command=command).pack()

        window.mainloop()

    def get_username(self):
        while not self.username:
            self.choose_user()
        return self.username


if __name__ == "__main__":
    user_selection = UserSelection()
    username = user_selection.get_username()
    print(username)  # ここで選択したユーザ名が出力されます

