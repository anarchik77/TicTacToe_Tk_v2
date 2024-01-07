# Готово для Git
import time
import numpy as np
from tkinter import *
from tkinter import messagebox
from math import inf as infinity
from random import choice

is_running = True
game_type = 2
rez_count_ai = {'PLAYER_WIN': 0, 'AI_WIN': 0, 'DRAW': 0}
rez_count_two = {'X_WIN': 0, 'O_WIN': 0, 'DRAW': 0}


class PerfectPlayer:
    """
    Класс алгоритма минимакс
    """

    # Функция конструктор алгоритма
    def __init__(self, _board, computer_sign=2, player_sign=1):

        self.p_sign = player_sign
        self.c_sign = computer_sign
        self.board = _board
        self.EMPTY = 0

    # Функция получения очков за ход
    def get_score(self, _state):

        if self.is_sign_win(_state, self.c_sign):
            score = 1
        elif self.is_sign_win(_state, self.p_sign):
            score = -1
        else:
            score = 0
        return score

    # Функция проверки победы одного из знаков
    @staticmethod
    def is_sign_win(_state, sign):

        for i in range(3):
            if _state[i][0] == _state[i][1] == _state[i][2] == sign:
                return True
            if _state[0][i] == _state[1][i] == _state[2][i] == sign:
                return True
        if _state[0][0] == _state[1][1] == _state[2][2] == sign:
            return True
        if _state[0][2] == _state[1][1] == _state[2][0] == sign:
            return True
        else:
            return False

    # Функция проверки окончания игры
    def game_over(self, board_state):

        return self.is_sign_win(board_state, self.p_sign) or self.is_sign_win(board_state, self.c_sign)

    # Функция получения списка координат пустых клеточек
    @staticmethod
    def empty_cells(board_state):

        cells = []
        for x, row in enumerate(board_state):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])
        return cells

    def pass_move(self, turn):

        return self.c_sign if turn == self.p_sign else self.p_sign

    # Функция минимакс алгоритма
    def minimax(self, _state, depth, turn):

        if turn == self.c_sign:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or self.game_over(_state):
            score = self.get_score(_state)
            return [-1, -1, score]

        for cell in self.empty_cells(_state):
            y, x = cell[0], cell[1]
            _state[y][x] = turn
            score = self.minimax(_state, depth - 1, self.pass_move(turn))
            _state[y][x] = 0
            score[0], score[1] = y, x
            if turn == self.c_sign:
                if score[2] > best[2]:
                    best = score
            else:
                if score[2] < best[2]:
                    best = score
        return best

    # Функция получения хода алгоритма
    def ai_turn(self):

        depth = len(self.empty_cells(self.board))
        if depth == 0 or self.game_over(self.board):
            return
        if depth == 9:
            y = choice([0, 1, 2])
            x = choice([0, 1, 2])
            move = [y, x]
        else:
            move = self.minimax(self.board, depth, self.c_sign)
        return move


class GameWindow:
    """
    Класс игры
    """
    # Функция конструктор игрового окна
    def __init__(self, win_title, win_width, win_height, win_cell_size):

        # Выбираем цвета для нашей игры
        self.bg_color = "#2a283d"
        self.line_color = "#444365"
        self.nought_color = "#c95b5c"
        self.cross_color = "#47bd80"

        # Инициализируем координаты нажатой ячейки
        self.click_x = None
        self.click_y = None

        # Крестики - 1, Нолики - 2, Пустые ячейки - 0
        # Инициализируем игровую доску
        self.X = 1
        self.O = 2
        self.EMPTY = 0
        self.board = np.full((3, 3), self.EMPTY)

        # Количество сделаных ходов
        # Установка первого хода для Крестика
        self.moves_count = 0
        self.turn = self.X
        self.is_win = False

        # Определение типа игры
        self.get_game_type()

        # Инициализируем ширину, высоту, заголовок и размер ячейки
        self.width = win_width
        self.height = win_height
        self.cell_size = win_cell_size
        self.dlt = self.cell_size * 0.2
        self.title = win_title

        # При запуске выполнить все необходимые функции
        self.run()

    # Функция для настройки игрвого окна
    def set_win(self):

        # Создаем окно с названием "self.win"
        self.win = Tk()
        # Устанавливаем размер и заголовок окна
        self.win.geometry(f"{self.width}x{self.height}+300+100")
        self.win.title(self.title)
        # Отключаем возможность изменять размер окна
        self.win.resizable(False, False)
        # Изменяем функцию закрытия окна
        self.win.protocol("WM_DELETE_WINDOW", self.close_window)

    # Функция для запуска игры
    def run(self):

        # Создание и настройка игрового окна
        self.set_win()
        # Создание обьектов графического интерфейса
        self.create_tools()
        # Размещение обьектов графического интерфейса
        self.place_tools()
        # Отрисовка начального игрового окна
        self.draw_canvas()
        self.bind_click()
        # self.fight()
        self.win.mainloop()

    # Функция для создания обьектов графического интерфейса
    def create_tools(self):

        # Создаем холст на игровом окне
        self.cnvs = Canvas(self.win, width=self.width,
                           height=self.height, bg=self.bg_color)
        # Создаем кнопку перезапуска игры
        self.btn_restart = Button(self.win, text="Начать заново!",
                                  command=self.restart, bg=self.line_color,
                                  fg=self.bg_color)
        # Создаем кнопку изменения типа игры
        self.btn_chng_type = Button(self.win, text=self.chng_type_text,
                                    command=self.chng_type, bg=self.line_color,
                                    fg=self.bg_color)

    def get_game_type(self):

        global game_type
        if game_type == 1:
            self.chng_type_text = "Играть вдвоём"
        elif game_type == 2:
            self.chng_type_text = "Играть c ИИ"

    def chng_type(self):

        global game_type
        if self.moves_count == 0:
            if game_type == 1:
                game_type = 2
            elif game_type == 2:
                game_type = 1
            self.get_game_type()
            self.btn_chng_type['text'] = self.chng_type_text

    # Функция для отрисовки крестика на игровом поле
    def draw_cross(self, x_0, y_0, x_1, y_1):

        self.cnvs.create_line(x_0 + self.dlt, y_0 + self.dlt,
                              x_1 - self.dlt, y_1 - self.dlt,
                              width=10, fill=self.cross_color)
        self.cnvs.create_line(x_1 - self.dlt, y_0 + self.dlt,
                              x_0 + self.dlt, y_1 - self.dlt,
                              width=10, fill=self.cross_color)

    # Функция для отрисовки нолика на игровом поле
    def draw_nought(self, x_0, y_0, x_1, y_1):

        self.cnvs.create_oval(x_0 + self.dlt, y_0 + self.dlt,
                              x_1 - self.dlt, y_1 - self.dlt,
                              width=10, outline=self.nought_color)

    # Отобразить знак ходившего
    def draw_sign(self, y, x):

        if self.board[y][x] == self.X:
            self.draw_cross((x + 0.5) * self.cell_size, (y + 0.5) * self.cell_size,
                            (x + 1.5) * self.cell_size, (y + 1.5) * self.cell_size)

        elif self.board[y][x] == self.O:
            self.draw_nought((x + 0.5) * self.cell_size, (y + 0.5) * self.cell_size,
                             (x + 1.5) * self.cell_size, (y + 1.5) * self.cell_size)

    # Отобразить все знаки на доске
    def draw_state(self):

        for n in range(3):
            for m in range(3):
                self.draw_sign(m, n)

    def draw_score(self, h, score_type):

        global rez_count_ai, rez_count_two, game_type

        self.cnvs.create_text(self.cell_size * 3.95, self.cell_size * (0.3 + h),
                              text=f"Счет игры {score_type}", fill=self.line_color,
                              font="Verdana 9", anchor=NW)  # против компьютера, на двоих
        self.cnvs.create_rectangle(self.cell_size * 4, self.cell_size * (0.5 + h),
                                   self.cell_size * 5.5, self.cell_size * (1 + h),
                                   width=3, outline=self.line_color)
        self.cnvs.create_rectangle(self.cell_size * 4, self.cell_size * (0.75 + h),
                                   self.cell_size * 5.5, self.cell_size * (1.25 + h),
                                   width=3, outline=self.line_color)
        self.cnvs.create_line(self.cell_size * 5, self.cell_size * (0.5 + h),
                              self.cell_size * 5, self.cell_size * (1.25 + h),
                              width=3, fill=self.line_color)
        if score_type == "с компьютером":
            self.cnvs.create_text(self.cell_size * 4.05, self.cell_size * (0.5 + h),
                                  text=f"Побед x    {rez_count_ai['PLAYER_WIN']}",
                                  fill=self.cross_color, font="Verdana 15", anchor=NW)
            self.cnvs.create_text(self.cell_size * 4.05, self.cell_size * (0.75 + h),
                                  text=f"Побед o    {rez_count_ai['AI_WIN']}",
                                  fill=self.nought_color, font="Verdana 15", anchor=NW)
            self.cnvs.create_text(self.cell_size * 4.05, self.cell_size * (1 + h),
                                  text=f"Ничьих     {rez_count_ai['DRAW']}",
                                  fill=self.line_color, font="Verdana 15", anchor=NW)
        elif score_type == "на двоих":
            self.cnvs.create_text(self.cell_size * 4.05, self.cell_size * (0.5 + h),
                                  text=f"Побед x    {rez_count_two['X_WIN']}",
                                  fill=self.cross_color, font="Verdana 15", anchor=NW)
            self.cnvs.create_text(self.cell_size * 4.05, self.cell_size * (0.75 + h),
                                  text=f"Побед o    {rez_count_two['O_WIN']}",
                                  fill=self.nought_color, font="Verdana 15", anchor=NW)
            self.cnvs.create_text(self.cell_size * 4.05, self.cell_size * (1 + h),
                                  text=f"Ничьих     {rez_count_two['DRAW']}",
                                  fill=self.line_color, font="Verdana 15", anchor=NW)

    # Функция для рисования конечного экрана
    def draw_end_screen(self):

        win_text = None

        # Если победил крестик, указать текст победы крестика
        if PerfectPlayer.is_sign_win(self.board, self.X):
            win_text = "Крестики выиграли"
            if game_type == 1:
                rez_count_ai['PLAYER_WIN'] += 1
            elif game_type == 2:
                rez_count_two['X_WIN'] += 1

        # Если победил нолик, указать текст победы нолика
        elif PerfectPlayer.is_sign_win(self.board, self.O):
            win_text = "Нолики выиграли"
            if game_type == 1:
                rez_count_ai['AI_WIN'] += 1
            elif game_type == 2:
                rez_count_two['O_WIN'] += 1

        # Если поле заполнено, указать текст ничьей
        elif self.moves_count >= 9:
            win_text = "Ничья"
            if game_type == 1:
                rez_count_ai['DRAW'] += 1
            elif game_type == 2:
                rez_count_two['DRAW'] += 1

        # Если игра закончена нарисовать конечный екран
        if win_text is not None:
            self.is_win = True
            self.cnvs.create_rectangle(self.cell_size * 0.5, self.cell_size * 0.5,
                                       self.cell_size * 3.5, self.cell_size * 3.5,
                                       fill=self.bg_color)
            self.draw_state()
            self.cnvs.create_text(self.cell_size * 2, self.dlt / 5, text=win_text,
                                  fill=self.line_color, font="Times 30", anchor=N)

    # Функция для рисования содержимого игрового окна
    def draw_canvas(self):

        self.cnvs.create_rectangle(self.cell_size * 0.5, self.cell_size * 0.5,
                                   self.cell_size * 3.5, self.cell_size * 3.5,
                                   width=3, outline=self.line_color)
        self.cnvs.create_line(self.cell_size * 1.5, self.cell_size * 0.5,
                              self.cell_size * 1.5, self.cell_size * 3.5,
                              width=5, fill=self.line_color)
        self.cnvs.create_line(self.cell_size * 2.5, self.cell_size * 0.5,
                              self.cell_size * 2.5, self.cell_size * 3.5,
                              width=5, fill=self.line_color)
        self.cnvs.create_line(self.cell_size * 0.5, self.cell_size * 1.5,
                              self.cell_size * 3.5, self.cell_size * 1.5,
                              width=5, fill=self.line_color)
        self.cnvs.create_line(self.cell_size * 0.5, self.cell_size * 2.5,
                              self.cell_size * 3.5, self.cell_size * 2.5,
                              width=5, fill=self.line_color)

    # Функция для размещения обьектов графического интерфейса
    def place_tools(self):

        self.cnvs.place(x=0, y=0)
        self.btn_restart.place(x=self.cell_size * 2.25, y=self.cell_size * 3.8,
                               width=self.cell_size * 1.5, height=self.dlt * 2)
        self.btn_chng_type.place(x=self.cell_size * 0.25, y=self.cell_size * 3.8,
                                 width=self.cell_size * 1.5, height=self.dlt * 2)

        self.draw_score(0.25, "с компьютером")
        self.draw_score(1.75, "на двоих")

    # Функция для рестарта игры
    def restart(self):

        self.win.destroy()
        GameWindow(self.title, self.width, self.height, self.cell_size)

    # Функция для закрытия игрового окна
    def close_window(self):

        global is_running
        if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
            is_running = False
            self.win.destroy()

    # Функция для определения координат выбраной ячейки
    def coordinates_clicked_cell(self, event):

        # Нахождение координат выбраной ячейки
        poss_x = int(((self.cnvs.winfo_pointerx() - self.cnvs.winfo_rootx()) - self.cell_size * 0.5) // self.cell_size)
        poss_y = int(((self.cnvs.winfo_pointery() - self.cnvs.winfo_rooty()) - self.cell_size * 0.5) // self.cell_size)
        if poss_x in [0, 1, 2] and poss_y in [0, 1, 2]:
            self.click_x = poss_x
            self.click_y = poss_y
        self.play()

    # Функция для привязки функций к нажатию кнопок мыши
    def bind_click(self):

        self.cnvs.bind_all("<Button-1>", self.coordinates_clicked_cell)  # ЛКМ
        self.cnvs.bind_all("<Button-3>", self.coordinates_clicked_cell)  # ПКМ

    def fight(self):

        while not self.is_win:
            comp1 = PerfectPlayer(self.board, self.X, self.O)
            comp2 = PerfectPlayer(self.board, self.O, self.X)
            if self.turn == self.X:
                move1 = comp1.ai_turn()
                self.board[move1[0], move1[1]] = self.X
                self.moves_count += 1
                self.draw_sign(move1[0], move1[1])
                if self.moves_count > 4:
                    self.draw_end_screen()
                self.turn = self.O
            elif self.turn == self.O:
                move2 = comp2.ai_turn()
                self.board[move2[0], move2[1]] = self.O
                self.moves_count += 1
                self.draw_sign(move2[0], move2[1])
                if self.moves_count > 4:
                    self.draw_end_screen()
                self.turn = self.X

    def play(self):

        if not self.is_win:
            if self.board[self.click_y, self.click_x] == self.EMPTY:
                if self.turn == self.X:
                    self.board[self.click_y, self.click_x] = self.X
                    self.moves_count += 1
                    self.draw_sign(self.click_y, self.click_x)
                    if self.moves_count > 4:
                        self.draw_end_screen()
                    self.turn = self.O
                    if game_type == 1 and not self.is_win:
                        computer = PerfectPlayer(self.board)
                        ai_move = computer.ai_turn()
                        self.board[ai_move[0], ai_move[1]] = self.O
                        self.moves_count += 1
                        self.draw_sign(ai_move[0], ai_move[1])
                        if self.moves_count > 4:
                            self.draw_end_screen()
                        self.turn = self.X
                elif self.turn == self.O:
                    self.board[self.click_y, self.click_x] = self.O
                    self.moves_count += 1
                    self.draw_sign(self.click_y, self.click_x)
                    if self.moves_count > 4:
                        self.draw_end_screen()
                    self.turn = self.X


if __name__ == "__main__":
    game_run = GameWindow("Крестики нолики", 600, 450, 100)
    game_run.play()
