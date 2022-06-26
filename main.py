import tkinter
import pyautogui  # �O�����C�u����
from PIL import Image, ImageTk, ImageDraw  # �O�����C�u����
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
    # �f�U�C���e�[�}�̐ݒ�

    # �E�B���h�E�ɔz�u����R���|�[�l���g
    layout = [  [sg.Text('Settings Menu')],
                [sg.Text('Screenshot shortcut key'), sg.InputText(default_text=config['DEFAULT']['shortcutkey'])],
                [sg.Text('Drag Box Color'), sg.InputText(default_text=config['DEFAULT']['color'])],
                [sg.Text('File Name (.y for year .m for month \n.d for day .h for hour\n.m for minute .s for second)'), sg.InputText(config['DEFAULT']['filename'])],
                [sg.Text('Settings window theme'), sg.Combo(['Light', 'Dark'],default_value=config['DEFAULT']['settingwindowtheme'], readonly=True)],
                [sg.Button('Cancel'),sg.Button('OK')]]

    # �E�B���h�E�̐���
    window = sg.Window('�T���v���v���O����', layout,disable_close=True)

    # �C�x���g���[�v
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


RESIZE_RETIO = 2 # �k���{���̋K��

# �h���b�O�J�n�������̃C�x���g - - - - - - - - - - - - - - - - - - - - - - - - - - 
def start_point_get(event):
    global start_x, start_y # �O���[�o���ϐ��ɏ������݂��s�Ȃ����ߐ錾

    canvas1.delete("rect1")  # ���ł�"rect1"�^�O�̐}�`������΍폜

    # canvas1��Ɏl�p�`��`��irectangle�͋�`�̈Ӗ��j
    config.read('config.ini')
    canvas1.create_rectangle(event.x,
                             event.y,
                             event.x + 1,
                             event.y + 1,
                             outline=str(config['DEFAULT']['color']),
                             tag="rect1")
    # �O���[�o���ϐ��ɍ��W���i�[
    start_x, start_y = event.x, event.y

# �h���b�O���̃C�x���g - - - - - - - - - - - - - - - - - - - - - - - - - - 
def rect_drawing(event):

    # �h���b�O���̃}�E�X�|�C���^���̈�O�ɏo�����̏���
    if event.x < 0:
        end_x = 0
    else:
        end_x = min(img.width, event.x)
    if event.y < 0:
        end_y = 0
    else:
        end_y = min(img.height, event.y)

    # "rect1"�^�O�̉摜���ĕ`��
    canvas1.coords("rect1", start_x, start_y, end_x, end_y)

# �h���b�O�𗣂����Ƃ��̃C�x���g - - - - - - - - - - - - - - - - - - - - - - - - - - 
def release_action(event):

    # "rect1"�^�O�̉摜�̍��W�����̏k�ڂɖ߂��Ď擾
    # * RESIZE_RETIO
    start_x, start_y, end_x, end_y = [
        n for n in canvas1.coords("rect1")
    ]
    config.read('config.ini')
    img.crop((start_x, start_y, end_x, end_y)).save(str(datetime.datetime.now().strftime(str(config['DEFAULT']['filename'].replace('.','%')))) + '.png', quality=95)
    root.destroy()
    # �擾�������W��\��
    # pyautogui.alert("start_x : " + str(start_x) + "\n" + "start_y : " +
                    # str(start_y) + "\n" + "end_x : " + str(end_x) + "\n" +
                    # "end_y : " + str(end_y))

# ���C������ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def quit_app():
    os.abort()
def settingswindow():
    threading.Thread(target=settingwindow).start()
def iconmain():
    im = Image.new("RGB",(16,16),"blue")# Image�C���X�^���X�����
    draw = ImageDraw.Draw(im)# im���ImageDraw�C���X�^���X�����
    draw.text((6,2),"S")
    menu = Menu(MenuItem('Settings', settingswindow),MenuItem('Quit', quit_app))
    icon = Icon(name='Screenshotter', icon=im, title='Screenshotter',menu=menu)
    icon.run()
threading.Thread(target=iconmain).start()
while True:
    config.read('config.ini')
    if keyboard.read_key() == str(config['DEFAULT']['shortcutkey']):
        # �\������摜�̎擾�i�X�N���[���V���b�g�j
        img = pyautogui.screenshot()
        # �X�N���[���V���b�g�����摜�͕\��������Ȃ��̂ŉ摜���T�C�Y
        # img = img.resize(size=(int(img.width / RESIZE_RETIO),
        #                                int(img.height / RESIZE_RETIO)),
        #                          resample=Image.BILINEAR)

        root = tkinter.Tk()
        root.attributes("-topmost", True) # tkinter�E�B���h�E����ɍőO�ʂɕ\��
        root.attributes('-fullscreen', True) 

        # tkinter�ŕ\���ł���悤�ɉ摜�ϊ�
        img_tk = ImageTk.PhotoImage(img)

        # Canvas�E�B�W�F�b�g�̕`��
        canvas1 = tkinter.Canvas(root,
                                bg="black",
                                width=img.width,
                                height=img.height)
        # Canvas�E�B�W�F�b�g�Ɏ擾�����摜��`��
        canvas1.create_image(0, 0, image=img_tk, anchor=tkinter.NW)

        # Canvas�E�B�W�F�b�g��z�u���A�e��C�x���g��ݒ�
        canvas1.pack()
        canvas1.bind("<ButtonPress-1>", start_point_get)
        canvas1.bind("<Button1-Motion>", rect_drawing)
        canvas1.bind("<ButtonRelease-1>", release_action)

        root.mainloop()
