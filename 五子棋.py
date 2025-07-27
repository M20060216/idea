import tkinter as tk
from tkinter import messagebox


class GomokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋游戏")
        self.root.geometry("500x550")  # 预留空间给开始界面

        # 游戏核心参数
        self.cell_size = 30  # 格子大小（像素）
        self.board_size = 15  # 棋盘尺寸（15x15）
        self.occupied = set()  # 记录已落子的位置编号
        self.black_record = []  # 黑棋落子记录（编号）
        self.white_record = []  # 白棋落子记录（编号）
        self.canvas = None  # 棋盘画布

        # 初始化开始界面
        self.create_start_screen()

    def create_start_screen(self):
        """创建初始界面（Start/Quit 按钮）"""
        # 清空原有控件
        for widget in self.root.winfo_children():
            widget.destroy()

        # 标题
        title = tk.Label(self.root, text="五子棋游戏", font=("Arial", 24, "bold"))
        title.pack(pady=80)

        # 按钮容器
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        # 开始游戏按钮
        start_btn = tk.Button(btn_frame, text="Start", font=("Arial", 14), command=self.start_game)
        start_btn.pack(side=tk.LEFT, padx=30)

        # 退出游戏按钮
        quit_btn = tk.Button(btn_frame, text="Quit", font=("Arial", 14), command=self.root.destroy)
        quit_btn.pack(side=tk.LEFT, padx=30)

    def start_game(self):
        """进入游戏界面，绘制棋盘并绑定事件"""
        # 清空原有控件
        for widget in self.root.winfo_children():
            widget.destroy()

        # 创建棋盘画布（15x15 网格）
        self.canvas = tk.Canvas(
            self.root,
            width=self.board_size * self.cell_size,
            height=self.board_size * self.cell_size,
            bg="lightgray"
        )
        self.canvas.pack()

        # 绘制棋盘网格
        self.draw_board()

        # 绑定鼠标事件：左键黑棋，右键白棋
        self.canvas.bind("<Button-1>", lambda e: self.place_stone(e, "black"))
        self.canvas.bind("<Button-3>", lambda e: self.place_stone(e, "white"))

    def draw_board(self):
        """绘制 15x15 棋盘网格"""
        for i in range(self.board_size):
            # 横线（y 方向）
            self.canvas.create_line(
                self.cell_size, self.cell_size + i * self.cell_size,
                                self.board_size * self.cell_size, self.cell_size + i * self.cell_size,
                width=1
            )
            # 竖线（x 方向）
            self.canvas.create_line(
                self.cell_size + i * self.cell_size, self.cell_size,
                self.cell_size + i * self.cell_size, self.board_size * self.cell_size,
                width=1
            )

    def place_stone(self, event, color):
        """落子逻辑：计算位置、判重、绘制棋子、判断胜负"""
        # 转换为棋盘坐标（网格索引）
        x = event.x - self.cell_size  # 偏移棋盘左边界
        y = event.y - self.cell_size  # 偏移棋盘上边界
        if x < 0 or x >= self.board_size * self.cell_size or y < 0 or y >= self.board_size * self.cell_size:
            return  # 点击超出棋盘范围

        # 计算网格索引（行、列）
        x_idx = x // self.cell_size  # 列索引（0-14）
        y_idx = y // self.cell_size  # 行索引（0-14）
        pos_id = y_idx * self.board_size + x_idx  # 唯一位置编号（0-224）

        # 检查是否重复落子
        if pos_id in self.occupied:
            return

        # 记录落子
        self.occupied.add(pos_id)
        if color == "black":
            self.black_record.append(pos_id)
        else:
            self.white_record.append(pos_id)

        # 绘制棋子（椭圆）
        center_x = self.cell_size + x_idx * self.cell_size
        center_y = self.cell_size + y_idx * self.cell_size
        radius = self.cell_size // 2 - 3  # 棋子半径（留出边界）
        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=color
        )

        # 判断是否五子连珠
        if self.check_win(x_idx, y_idx, color):
            messagebox.showinfo("游戏结束", f"{color}方获胜！")
            # 重置游戏（回到开始界面）
            self.occupied.clear()
            self.black_record.clear()
            self.white_record.clear()
            self.create_start_screen()

    def check_win(self, x, y, color):
        """检查五子连珠（四个方向：横、竖、两对角线）"""
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 水平、垂直、右下、左下

        for dx, dy in directions:
            count = 1  # 当前棋子本身
            # 正向遍历（沿方向延伸）
            for i in range(1, 5):
                nx = x + dx * i
                ny = y + dy * i
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    pos_id = ny * self.board_size + nx
                    # 检查当前颜色是否匹配
                    if (color == "black" and pos_id in self.black_record) or \
                            (color == "white" and pos_id in self.white_record):
                        count += 1
                    else:
                        break
            # 反向遍历（沿方向反方向延伸）
            for i in range(1, 5):
                nx = x + dx * i
                ny = y + dy * i
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    pos_id = ny * self.board_size + nx
                    # 检查当前颜色是否匹配
                    if (color == "black" and pos_id in self.black_record) or \
                            (color == "white" and pos_id in self.white_record):
                        count += 1
                    else:
                        break
                # 反向遍历（沿方向反方向延伸）
            for i in range(1, 5):
                nx = x - dx * i
                ny = y - dy * i
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    pos_id = ny * self.board_size + nx
                    if (color == "black" and pos_id in self.black_record) or \
                            (color == "white" and pos_id in self.white_record):
                        count += 1
                    else:
                        break
            if count >= 5:  # 五子连珠
                return True
            return False

if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGame(root)
    root.mainloop()