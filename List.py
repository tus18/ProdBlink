import matplotlib.pyplot as plt

class list_create:
    # 時間の経過
    def __call__(self,l):
        minutes = list(range(1, len(l)+1))
        # プロット作成
        plt.plot(minutes, l)

        # グラフのタイトルとラベル
        plt.title('Blink Count Over Time')
        plt.xlabel('Minutes')
        plt.ylabel('Blink Count')

        # グラフ表示
        plt.savefig('fig/fig.png')

if __name__ == '__main__':
    l = [8, -2, -8, 4, -6, -17, -12, -10, -16, -3, -10, 7, 0, -16, -28, -12, -15, -29, -12, -2, -9, 14, 23, 71, 68, 83, 80, 81, 81]
    lc =list_create()
    lc(l)