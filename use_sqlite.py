import os

from models import *

Session = sessionmaker(bind=engine)
session = Session()
basedir = os.path.abspath(os.curdir) + '/song'


def add_song_list():
    name = input('请输入歌单名: ')
    arg_a = int(input('输入arg_a: '))
    arg_b = int(input('输入arg_b: '))
    arg_c = int(input('输入arg_c: '))
    if isinstance(name, str):
        try:
            list_object = SongLists(name=name, arg_a=arg_a, arg_b=arg_b, arg_c=arg_c)
            session.add(list_object)
            session.commit()
        except IntegrityError:
            print('该歌单名已经存在...')
    else:
        print('歌单名类型错误....')


def add_song():  # 太低效率了.....
    temp_list = []
    for current_song_name in os.listdir(basedir):
            temp_list.append(current_song_name)
    for each_item in session.query(Songs).all():  # 这里其实还需要一个...如果文件不存在的except
        temp_list.remove(each_item.name)

    if len(temp_list):
        print('请输入歌曲名: ', end='')
        for name in temp_list:
            print('当前歌曲名为: ' + name)
            arg_a = int(input('输入arg_a: '))
            arg_b = int(input('输入arg_b: '))
            arg_c = int(input('输入arg_c: '))
            list_name = input('输入所属歌单名(若无,直接键入回车): ')
            songlist_item = session.query(SongLists).filter_by(name=list_name).first()
            if songlist_item:
                session.add(
                    Songs(name=name, arg_a=arg_a, arg_b=arg_b, arg_c=arg_c,
                          belong_list=session.query(SongLists).filter_by(name=list_name).first()))
                session.commit()
            else:
                print('该歌单不存在...')
    else:
        print('当前音乐文件夹...无需更新...')

        # if isinstance(name, str):
        #     list_object = Songs(name=name, arg_a=arg_a, arg_b=arg_b, arg_c=arg_c)
        #     session.add(list_object)
        #     session.commit()
        # else:
        #     print('歌曲名类型错误....')


# a_list = SongLists(name='A', arg_a=75, arg_b=20, arg_c=5)
# session.add(a_list)
# session.commit()

# for name in os.listdir(basedir):
#     session.add(
#         Songs(name=name, arg_a=random.randint(0, 100), arg_b=random.randint(0, 100), arg_c=random.randint(0, 100),
#               belong_list=session.query(SongLists).filter_by(name='A').first()))
#     session.commit()

# sum_num = 0
# for lists in session.query(SongLists).all():
#     sum_num += 1
#     print(sum_num)
#     print('歌单名称: ', lists.name, lists.arg_a, lists.arg_b, lists.arg_c)
#     for x in lists.songs:
#         print('下属歌曲: ', x.name, x.arg_a, x.arg_b, x.arg_c)
#         print(x.belong_list.name)

# for each_item in session.query(Songs).all():
#     print(each_item.name, each_item.arg_a, each_item.arg_b, each_item.arg_c)


def create_database():
    Base.metadata.create_all(engine)


def yield_data(dict_ordered):
    for x, y in dict_ordered.items():
        yield x, y


def get_songs(cls):
    lists = []
    data_dict = {
        'arg_a': cls.arg_a,
        'arg_b': cls.arg_b,
        'arg_c': cls.arg_c
    }
    dict_ordered = OrderedDict(sorted(data_dict.items(), key=lambda t: t[1], reverse=True))
    temp = yield_data(dict_ordered)
    k = next(temp)
    x = k[0]
    y = k[1]
    # filter((getattr(Songs, x) - y <= 5) & (getattr(Songs, x) - y >= -5))
    for each in session.query(Songs).order_by(func.abs(getattr(Songs, x) - y)):  # 不会做主次关键字查询
        # print(each.arg_b)
        lists.append(basedir + '/' + each.name)
        # print(each.arg_a, each.arg_b, each.arg_c)
    # for x in lists:
    #     print(x)
    return lists


def get_songlist(cls):
    lists = []
    data_dict = {
        'arg_a': cls.arg_a,
        'arg_b': cls.arg_b,
        'arg_c': cls.arg_c
    }
    dict_ordered = OrderedDict(sorted(data_dict.items(), key=lambda t: t[1], reverse=True))
    temp = yield_data(dict_ordered)
    k = next(temp)
    x = k[0]
    y = k[1]
    song_list = session.query(SongLists).order_by(func.abs(getattr(SongLists, x) - y)).first()
    for temp_song in song_list.songs:
        lists.append(basedir + '/' + temp_song.name)
        # print(temp_song.arg_a, temp_song.arg_b, temp_song.arg_c)
    # for x in lists:
    #     print(x)
    return lists


if __name__ == '__main__':
#     # create_database()
#     # add_song_list()
    add_song()
    pass
