# -*- coding: utf-8 -*-
import threading
import time
import tkinter
import pygame
from use_sqlite import *
from weather_api import weathernow
from I2C import *


ss = Test()
ss.function_test(20, 70, 10)  # li add code

# str_a = 'aurora - 森罗万象.mp3'
# print(str_a.encode('utf-8'))
# pygame.mixer.init()
# pygame.mixer.music.load(str_a.encode('utf-8'))
# pygame.mixer.music.play()
# pygame.mixer.music.set_volume(1.0)
# print(pygame.mixer.music.get_busy())  # 判断是否在播放音乐,返回1为正在播放。
# lists = ['aurora - 森罗万象.mp3']
# # 'Bad Apple!! - Golden City Factory.mp3',
# # for x in lists:
# # pygame.mixer.music.queue('Bad Apple!! - Golden City Factory.mp3')
# # print(pygame.mixer.music.get_busy())

# pygame.mixer.music.pause()
# print(pygame.mixer.music.get_busy())
# pygame.mixer.music.unpause()
# while True:
#     if not pygame.mixer.music.get_busy():
#         pygame.mixer.music.load('Bad Apple!! - Golden City Factory.mp3')
#         pygame.mixer.music.play()
# # pygame.mixer.music.queue('aurora - 森罗万象.mp3')
# time.sleep(1000)

root = tkinter.Tk()
root.title('车载系统音乐播放器v1.0')
root.geometry('800x600')  # 整体大小
root.resizable(True, True)  # 不允许更改应用大小

play_status = False
song_type = True  # True 为单曲, False 为歌单

# 通过先将lists复制一边来来避免直接使用数据库的生成器,造成多线程操控数据库,直接报错
temp_list_songlist = get_songlist(ss)
temp_list_song = get_songs(ss)


def yield_music_list(temp_list):  # 一个歌曲路径列表的生成器
    for temp in temp_list:
        yield temp


def yield_music(temp_list):
    for temp in temp_list:
        yield temp


item_song = yield_music(temp_list_song)
item_song_list = yield_music_list(temp_list_songlist)


def button_play_click():
    global play_status
    global song_type
    song_type = True
    play_status = True
    t = threading.Thread(target=play_music)  # 新建一个线程来运行 pygame 播放音乐
    t.setDaemon(True)
    t.start()

    play_button['state'] = 'disabled'
    play_list_button['state'] = 'disabled'
    stop_button['state'] = 'normal'
    pause_button['state'] = 'normal'
    next_button['state'] = 'normal'


def button_play_songlist_click():
    global play_status
    global song_type
    play_status = True
    song_type = False
    t = threading.Thread(target=play_music_list)
    t.setDaemon(True)
    t.start()

    play_button['state'] = 'disabled'
    play_list_button['state'] = 'disabled'
    stop_button['state'] = 'normal'
    pause_button['state'] = 'normal'
    next_button['state'] = 'normal'


def button_stop_click():
    global play_status
    play_status = False
    pygame.mixer.music.stop()
    music_name.set('暂时没有播放音乐...')

    play_button['state'] = 'normal'
    play_list_button['state'] = 'normal'
    stop_button['state'] = 'disabled'
    pause_button['state'] = 'disabled'
    next_button['state'] = 'disabled'


def button_pause_click():
    if play_pause.get() == '暂停':
        pygame.mixer.music.pause()
        play_pause.set('继续')
    elif play_pause.get() == '继续':
        pygame.mixer.music.unpause()
        play_pause.set('暂停')


def button_next_click():  # 下一首的话,实际为关闭之后,再重新play
    global play_status
    play_status = False
    pygame.mixer.stop()
    pygame.mixer.quit()
    if song_type:
        button_play_click()
    else:
        button_play_songlist_click()


def play_music():  # 该函数为点击播放按钮时触发,因为主线程是loop,所以该函数需放入一个新子线程
    pygame.mixer.init()  # 初始化设备...
    while play_status:  # 如果触发play, 那么将进入无限循环,直至触发关闭...
        if not pygame.mixer.music.get_busy():  # 如果当前没有歌曲播放(包括暂停中的歌曲)
            try:
                next_song_path = next(item_song)  # 调用生成器
                pygame.mixer.music.load(next_song_path.encode('utf-8'))  # 注意,这里必须使用encode,否则遇中文则报错
                pygame.mixer.music.play()
                music_name.set('正在播放: ' + next_song_path.split('/')[-1])  # 取出音乐名
            except StopIteration:
                music_name.set('歌曲播放完毕...')
                # 这个地方仍旧有一个BUG, 如果播放完毕..我们需要改变按钮的形式,
                # 而且最重要的一点是...如果让 play_status 变为 False, 这涉及进程之间的共享变量问题
                # 如果播放完毕..之后点击 "下一首", 会直接卡死.....
                # 重大 BUG
        else:
            time.sleep(0.3)
            # del item_song


def play_music_list():  # 该函数为点击播放按钮时触发,因为主线程是loop,所以该函数需放入一个新子线程
    pygame.mixer.init()  # 初始化设备...
    while play_status:  # 如果触发play, 那么将进入无限循环,直至触发关闭...
        if not pygame.mixer.music.get_busy():  # 如果当前没有歌曲播放(包括暂停中的歌曲)
            try:
                next_song_path = next(item_song_list)  # 调用生成器
                pygame.mixer.music.load(next_song_path.encode('utf-8'))  # 注意,这里必须使用encode,否则遇中文则报错
                pygame.mixer.music.play()
                music_name.set('正在播放: ' + next_song_path.split('/')[-1])  # 取出音乐名
            except StopIteration:
                music_name.set('歌单播放完毕...')
        else:
            time.sleep(0.3)
            # del item_song_list


music_name = tkinter.StringVar(root, value="暂时没有播放音乐...")
label_name = tkinter.Label(root, textvariable=music_name, justify='left')
label_name.grid(row=0, column=1, columnspan=11, pady=10)

weather_info = tkinter.StringVar(root, value=weathernow)
label_weather = tkinter.Label(root, textvariable=weather_info, font=('黑体', 10))
label_weather.grid(row=3, column=1, columnspan=10, pady=50)

Labelg0 = tkinter.Label(root)  # 我用来拓宽左边距。。 # 无常write
Labelg0.grid(row=1, column=0, padx=40)

play_button = tkinter.Button(root, text='歌曲播放', command=button_play_click)
play_list_button = tkinter.Button(root, text='歌单播放', command=button_play_songlist_click)
stop_button = tkinter.Button(root, text='停止播放', command=button_stop_click)
play_pause = tkinter.StringVar(root, value='暂停')
pause_button = tkinter.Button(root, textvariable=play_pause, command=button_pause_click)
next_button = tkinter.Button(root, text='下一首', command=button_next_click)

play_button['state'] = 'normal'
play_list_button['state'] = 'normal'
stop_button['state'] = 'disabled'
pause_button['state'] = 'disabled'
next_button['state'] = 'disabled'

play_button.grid(row=1, column=1)
play_list_button.grid(row=1, column=3)
stop_button.grid(row=1, column=5)
pause_button.grid(row=1, column=7)
next_button.grid(row=1, column=9)


if __name__ == '__main__':
    root.mainloop()
    # for x in session.query(Songs).all():
    #     print(x.name)
    #     print(x.belong_list)
    # for y in session.query(SongLists).all():
    #     print(y.name)
    #     for x in y.songs:
    #         print(x.name)
    pass
