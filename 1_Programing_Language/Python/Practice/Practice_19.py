class MusicPlayer:

    def __new__(cls, *args, **kwargs):

        # 为对象分配空间
        instance = super().__new__(cls)
        # 返回对象引用
        return instance

    def __init__(self):
        print("播放器初始化")



player = MusicPlayer()

print(player)