"""
需求：
- 设计一个 Game 类
- 属性
    - 定义一个 类属性 top_score 记录游戏的历史最高分
    - 定义一个 实例属性 player_name 记录当前游戏的玩家姓名
- 方法：
    - 静态方法 show_help 显示游戏帮助信息
    - 类方法 show_top_score 显示历史最高分
    - 实例方法 start_game 开始当前玩家的游戏
- 主程序步骤
    - 查看帮助信息
    - 查看历史最高分
    - 创建游戏对象，开始游戏
"""

class Game:

    # 历史最高分
    top_score = 0

    def __init__(self, player_name):
        self.player_name = player_name

    @staticmethod
    def show_help():
        print("help message")

    @classmethod
    def show_top_score(cls):
        print(f"top score {cls.top_score}")

    def start_game(self):
        print(f"game start {self.player_name}")


# 查看帮助信息
Game.show_help()

# 查看历史最高分
Game.show_top_score()

# 创建游戏对象，开始游戏
game = Game("Kobayashi")
game.start_game()