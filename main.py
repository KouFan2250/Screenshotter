import tkinter
import pyautogui  # 外部ライブラリ
from PIL import Image, ImageTk, ImageDraw  # 外部ライブラリ
import os
import datetime
import keyboard
import configparser
import threading
from pystray import Icon, Menu, MenuItem
import PySimpleGUI as sg

# config
config = configparser.ConfigParser()
if os.path.isfile('config.ini') == False:
    config['DEFAULT']['shortcutkey'] = 'p'
    config['DEFAULT']['color'] = 'red'
    config['DEFAULT']['filename'] = '.Y-.m-.d-.H-.M-.S'
    config['DEFAULT']['settingwindowtheme'] = 'dark'
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
config.read('config.ini')





def settingwindow():
    config.read('config.ini')

    if str(config['DEFAULT']['settingwindowtheme']) == 'Dark':
        sg.change_look_and_feel('Dark2')
    elif 'Light':
        sg.change_look_and_feel('DefaultNoMoreNagging')
    # デザインテーマの設定

    # ウィンドウに配置するコンポーネント
    layout = [  [sg.Text('Settings Menu')],
                [sg.Text('Screenshot shortcut key'), sg.InputText(default_text=config['DEFAULT']['shortcutkey'])],
                [sg.Text('Drag Box Color'), sg.InputText(default_text=config['DEFAULT']['color'])],
                [sg.Text('File Name (.y for year .m for month \n.d for day .h for hour\n.m for minute .s for second)'), sg.InputText(config['DEFAULT']['filename'])],
                [sg.Text('Settings window theme'), sg.Combo(['Light', 'Dark'],default_value=config['DEFAULT']['settingwindowtheme'], readonly=True)],
                [sg.Button('Cancel'),sg.Button('OK')]]

    # ウィンドウの生成
    window = sg.Window('サンプルプログラム', layout,disable_close=True)

    # イベントループ
    while True:
        event, values = window.read()
        if event == 'Cancel':
            break
        elif event == 'OK':
            config['DEFAULT']['shortcutkey'] = values[0]
            config['DEFAULT']['color'] = values[1]
            config['DEFAULT']['filename'] = values[2]
            config['DEFAULT']['settingwindowtheme'] = values[3]
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            break

    window.close()


RESIZE_RETIO = 2 # 縮小倍率の規定

# ドラッグ開始した時のイベント - - - - - - - - - - - - - - - - - - - - - - - - - - 
def start_point_get(event):
    global start_x, start_y # グローバル変数に書き込みを行なうため宣言

    canvas1.delete("rect1")  # すでに"rect1"タグの図形があれば削除

    # canvas1上に四角形を描画（rectangleは矩形の意味）
    config.read('config.ini')
    canvas1.create_rectangle(event.x,
                             event.y,
                             event.x + 1,
                             event.y + 1,
                             outline=str(config['DEFAULT']['color']),
                             tag="rect1")
    # グローバル変数に座標を格納
    start_x, start_y = event.x, event.y

# ドラッグ中のイベント - - - - - - - - - - - - - - - - - - - - - - - - - - 
def rect_drawing(event):

    # ドラッグ中のマウスポインタが領域外に出た時の処理
    if event.x < 0:
        end_x = 0
    else:
        end_x = min(img.width, event.x)
    if event.y < 0:
        end_y = 0
    else:
        end_y = min(img.height, event.y)

    # "rect1"タグの画像を再描画
    canvas1.coords("rect1", start_x, start_y, end_x, end_y)

# ドラッグを離したときのイベント - - - - - - - - - - - - - - - - - - - - - - - - - - 
def release_action(event):

    # "rect1"タグの画像の座標を元の縮尺に戻して取得
    # * RESIZE_RETIO
    start_x, start_y, end_x, end_y = [
        n for n in canvas1.coords("rect1")
    ]
    config.read('config.ini')
    img.crop((start_x, start_y, end_x, end_y)).save(str(datetime.datetime.now().strftime(str(config['DEFAULT']['filename'].replace('.','%')))) + '.png', quality=95)
    root.destroy()
    # 取得した座標を表示
    # pyautogui.alert("start_x : " + str(start_x) + "\n" + "start_y : " +
                    # str(start_y) + "\n" + "end_x : " + str(end_x) + "\n" +
                    # "end_y : " + str(end_y))

# メイン処理 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def quit_app():
    os.abort()
def settingswindow():
    threading.Thread(target=settingwindow).start()
def iconmain():
    im = Image.new("RGB",(16,16),"blue")# Imageインスタンスを作る
    draw = ImageDraw.Draw(im)# im上のImageDrawインスタンスを作る
    draw.text((6,2),"S")
    menu = Menu(MenuItem('Settings', settingswindow),MenuItem('Quit', quit_app))
    icon = Icon(name='Screenshotter', icon=im, title='Screenshotter',menu=menu)
    icon.run()
threading.Thread(target=iconmain).start()
while True:
    config.read('config.ini')
    if keyboard.read_key() == str(config['DEFAULT']['shortcutkey']):
        # 表示する画像の取得（スクリーンショット）
        img = pyautogui.screenshot()
        # スクリーンショットした画像は表示しきれないので画像リサイズ
        # img = img.resize(size=(int(img.width / RESIZE_RETIO),
        #                                int(img.height / RESIZE_RETIO)),
        #                          resample=Image.BILINEAR)

        root = tkinter.Tk()
        root.attributes("-topmost", True) # tkinterウィンドウを常に最前面に表示
        root.attributes('-fullscreen', True) 

        # tkinterで表示できるように画像変換
        img_tk = ImageTk.PhotoImage(img)

        # Canvasウィジェットの描画
        canvas1 = tkinter.Canvas(root,
                                bg="black",
                                width=img.width,
                                height=img.height)
        # Canvasウィジェットに取得した画像を描画
        canvas1.create_image(0, 0, image=img_tk, anchor=tkinter.NW)

        # Canvasウィジェットを配置し、各種イベントを設定
        canvas1.pack()
        canvas1.bind("<ButtonPress-1>", start_point_get)
        canvas1.bind("<Button1-Motion>", rect_drawing)
        canvas1.bind("<ButtonRelease-1>", release_action)

        root.mainloop()
