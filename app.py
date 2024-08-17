import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QHBoxLayout, QGroupBox, QSizePolicy, QInputDialog
from PyQt5.QtCore import pyqtSignal, Qt

class ControlWindow(QWidget):
    number_selected = pyqtSignal(int)
    game_mode_selected = pyqtSignal(str)
    clear_selection = pyqtSignal()
    manual_mode_entered = pyqtSignal(str)
    draw_ball = pyqtSignal()
    reset_ball_selector = pyqtSignal()
    ball_selected = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # BINGO reference
        bingo_layout = QHBoxLayout()
        bingo_labels = ['B', 'I', 'N', 'G', 'O']
        for label in bingo_labels:
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("font-size: 24px; font-weight: bold;")
            bingo_layout.addWidget(lbl)
        main_layout.addLayout(bingo_layout)

        # Number buttons under each BINGO letter
        numbers_layout = QHBoxLayout()
        for i in range(5):
            column_layout = QVBoxLayout()
            start = i * 15 + 1
            for j in range(start, start + 15):
                btn = QPushButton(str(j))
                btn.setFixedSize(50, 50)
                btn.clicked.connect(lambda _, num=j: self.handle_number_selected(num))
                column_layout.addWidget(btn)
            numbers_layout.addLayout(column_layout)

        main_layout.addLayout(numbers_layout)

        # Call Ball, Odds, and Evens buttons
        button_layout = QGridLayout()
        button_size = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        draw_button = QPushButton('Call Ball')
        draw_button.setSizePolicy(button_size)
        draw_button.setFixedHeight(80)  # Double the current height
        draw_button.clicked.connect(self.draw_ball.emit)
        button_layout.addWidget(draw_button, 0, 0)

        odd_button = QPushButton('Odds')
        odd_button.setSizePolicy(button_size)
        odd_button.setFixedHeight(80)  # Double the current height
        odd_button.clicked.connect(self.select_odd)
        button_layout.addWidget(odd_button, 0, 1)

        even_button = QPushButton('Evens')
        even_button.setSizePolicy(button_size)
        even_button.setFixedHeight(80)  # Double the current height
        even_button.clicked.connect(self.select_even)
        button_layout.addWidget(even_button, 0, 2)

        main_layout.addLayout(button_layout)

        # Wild Number Ending Selector
        wild_layout = QHBoxLayout()
        wild_label = QLabel("Wild:")
        wild_layout.addWidget(wild_label)
        for i in range(10):
            btn = QPushButton(str(i))
            btn.setFixedSize(40, 40)
            btn.clicked.connect(lambda _, end=i: self.select_ending(end))
            wild_layout.addWidget(btn)
        main_layout.addLayout(wild_layout)

        # Game mode selection
        game_mode_group = QGroupBox("Choose or Enter Game Mode")
        game_mode_layout = QGridLayout()
        game_modes = [
            'Single Bingo', 'Double Bingo', 'Triple Bingo', 
            'Letter X', 'Corner Picture Frame', 'Check Mark', 
            'Four Corners', 'Heart', 'Postage Stamp', 'Block of 8', 'Blackout'
        ]
        for i, mode in enumerate(game_modes):
            btn = QPushButton(mode)
            btn.clicked.connect(lambda _, m=mode: self.game_mode_selected.emit(m))
            game_mode_layout.addWidget(btn, i // 2, i % 2)

        # Manual game mode entry
        manual_entry_button = QPushButton('Manual Entry')
        manual_entry_button.clicked.connect(self.manual_entry)
        game_mode_layout.addWidget(manual_entry_button, len(game_modes) // 2, len(game_modes) % 2)

        game_mode_group.setLayout(game_mode_layout)
        main_layout.addWidget(game_mode_group)

        clear_button = QPushButton('Reset')
        clear_button.clicked.connect(self.reset_all)
        main_layout.addWidget(clear_button)

        self.setLayout(main_layout)
        self.setWindowTitle('Stevens Bingo Game Master Controller')
        self.setMinimumSize(300, 800)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def handle_number_selected(self, num):
        self.number_selected.emit(num)
        self.ball_selected.emit(num)

    def select_odd(self):
        for i in range(1, 76, 2):
            self.handle_number_selected(i)

    def select_even(self):
        for i in range(2, 76, 2):
            self.handle_number_selected(i)

    def select_ending(self, end):
        for i in range(1, 76):
            if str(i).endswith(str(end)):
                self.handle_number_selected(i)

    def manual_entry(self):
        mode, ok = QInputDialog.getText(self, 'Manual Game Mode Entry', 'Enter custom game mode:')
        if ok and mode:
            self.manual_mode_entered.emit(mode)

    def reset_all(self):
        self.clear_selection.emit()
        self.reset_ball_selector.emit()

class UpNextWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.up_next_label = QLabel("UP NEXT")
        self.up_next_label.setAlignment(Qt.AlignCenter)
        self.up_next_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(self.up_next_label)

        self.up_next_ball = QLabel()
        self.up_next_ball.setAlignment(Qt.AlignCenter)
        self.up_next_ball.setFixedSize(200, 200)
        self.up_next_ball.setStyleSheet("font-size: 64px; font-weight: bold; border-radius: 100px; background-color: lightgray;")
        main_layout.addWidget(self.up_next_ball, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
        self.setWindowTitle('Up Next')
        self.setMinimumSize(250, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def update_up_next(self, color):
        color_mapping = {
            'B': 'blue',
            'I': 'red',
            'N': 'white',
            'G': 'green',
            'O': 'yellow'
        }
        
        if color in color_mapping:
            self.up_next_ball.setStyleSheet(f"font-size: 64px; font-weight: bold; border-radius: 100px; background-color: {color_mapping[color]};")
        else:
            self.up_next_ball.setStyleSheet("font-size: 64px; font-weight: bold; border-radius: 100px; background-color: lightgray;")

class BallSelectorWindow(QWidget):
    def __init__(self, up_next_window):
        super().__init__()
        self.init_ui()
        self.selected_balls = set()
        self.up_next_window = up_next_window
        self.next_color = None

    def init_ui(self):
        main_layout = QVBoxLayout()

        self.current_ball_label = QLabel("BINGO")
        self.current_ball_label.setAlignment(Qt.AlignCenter)
        self.current_ball_label.setFixedSize(215, 215)  # Make the label larger
        self.current_ball_label.setStyleSheet("font-size: 64px; font-weight: bold; border-radius: 100px; background-color: lightgray;")
        main_layout.addWidget(self.current_ball_label, alignment=Qt.AlignCenter)

        self.ball_stack = QVBoxLayout()
        self.stack_widget = QWidget()
        self.stack_widget.setLayout(self.ball_stack)
        main_layout.addWidget(self.stack_widget)

        self.setLayout(main_layout)
        self.setWindowTitle('Random Bingo Ball Selector')
        self.setMinimumSize(300, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def draw_ball(self):
        # Ensure we pick a valid next color
        available_colors = [color for color in ['B', 'I', 'N', 'G', 'O'] if self.has_available_balls(color)]
        if not available_colors:
            return None  # No balls left to draw

        if self.next_color is None or self.next_color not in available_colors:
            self.next_color = random.choice(available_colors)

        col_index = ['B', 'I', 'N', 'G', 'O'].index(self.next_color)
        color_balls = [num for num in range(1 + col_index * 15, 16 + col_index * 15) if num not in self.selected_balls]

        if not color_balls:
            return None

        ball = random.choice(color_balls)
        self.selected_balls.add(ball)
        color_mapping = self.get_color(col_index)
        text_color = 'black' if col_index == 4 else ('black' if col_index == 2 else 'white')
        ball_label = QLabel(f"{self.next_color} {ball}")
        ball_label.setAlignment(Qt.AlignCenter)
        ball_label.setStyleSheet(f"font-size: 24px; font-weight: bold; background-color: {color_mapping}; color: {text_color}; border-radius: 25px; width: 50px; height: 50px;")

        # Set the current ball label with larger circle style
        self.current_ball_label.setText(f"{self.next_color} {ball}")
        self.current_ball_label.setStyleSheet(f"font-size: 64px; font-weight: bold; border-radius: 100px; background-color: {color_mapping}; color: {text_color}; width: 200px; height: 200px;")

        if self.ball_stack.count() >= 5:
            self.ball_stack.takeAt(self.ball_stack.count() - 1).widget().deleteLater()

        self.ball_stack.insertWidget(0, ball_label)  # Add to the top of the stack

        # Prepare the next ball
        available_colors = [color for color in ['B', 'I', 'N', 'G', 'O'] if self.has_available_balls(color)]
        if available_colors:
            self.next_color = random.choice(available_colors)
            self.up_next_window.update_up_next(self.next_color)

        return ball

    def has_available_balls(self, color):
        col_index = ['B', 'I', 'N', 'G', 'O'].index(color)
        color_balls = [num for num in range(1 + col_index * 15, 16 + col_index * 15)]
        return any(num not in self.selected_balls for num in color_balls)

    def get_color(self, index):
        colors = ['blue', 'red', 'white', 'green', 'yellow']
        return colors[index]

    def reset(self):
        self.selected_balls.clear()
        self.current_ball_label.setText("BINGO")
        self.current_ball_label.setStyleSheet("font-size: 64px; font-weight: bold; border-radius: 100px; background-color: lightgray; width: 200px; height: 200px;")
        for i in reversed(range(self.ball_stack.count())):
            self.ball_stack.itemAt(i).widget().deleteLater()
        self.up_next_window.update_up_next('lightgray')  # Reset up next window

    def handle_manual_selection(self, ball):
        self.selected_balls.add(ball)

class DisplayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.selected_numbers = set()
        main_layout = QHBoxLayout()

        # Game template display (5x5 bingo card example)
        template_layout = QVBoxLayout()
        self.template_label = QLabel("Game:\n")
        self.template_label.setStyleSheet("font-size: 24px;")
        self.template_label.setWordWrap(True)  # Enable word wrapping
        template_layout.addWidget(self.template_label)

        self.template_card = QGridLayout()
        self.template_cells = {}
        for i in range(5):
            bingo_label = QLabel('BINGO'[i])
            bingo_label.setAlignment(Qt.AlignCenter)
            bingo_label.setStyleSheet(f"font-size: 18px; font-weight: bold; background-color: {self.get_color(i)}; color: black;")
            self.template_card.addWidget(bingo_label, 0, i + 1)
        
        for i in range(5):
            for j in range(5):
                if i == 2 and j == 2:
                    cell = QLabel('Free Space')
                    cell.setStyleSheet("background-color: gray; color: white;")
                else:
                    number = random.randint(1 + j * 15, 15 + j * 15)
                    cell = QLabel(str(number))
                cell.setAlignment(Qt.AlignCenter)
                cell.setFixedSize(60, 60)
                cell.setStyleSheet("border: 2px solid gray;")
                cell.mousePressEvent = lambda _, pos=(i, j): self.toggle_template_cell(pos)
                self.template_card.addWidget(cell, i + 1, j + 1)
                self.template_cells[(i, j)] = cell

        template_layout.addLayout(self.template_card)
        main_layout.addLayout(template_layout)

        # Number display grid
        display_layout = QVBoxLayout()
        self.grid = QGridLayout()

        self.labels = {}
        for i in range(5):
            bingo_label = QLabel('BINGO'[i])
            bingo_label.setStyleSheet(f"font-size: 24px; font-weight: bold; background-color: {self.get_color(i)}; color: black;")
            self.grid.addWidget(bingo_label, i, 0)

            for j in range(15):
                num = i * 15 + j + 1
                label = QLabel(str(num))
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(100, 100)
                self.grid.addWidget(label, i, j + 1)
                self.labels[num] = label

        display_layout.addLayout(self.grid)
        main_layout.addLayout(display_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Stevens Bingo Master Call Sheet')
        self.setMinimumSize(1000, 600)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def get_color(self, index):
        colors = ['blue', 'red', 'white', 'green', 'yellow']
        return colors[index]

    def update_display(self, number):
        label = self.labels.get(number)
        if label:
            if number in self.selected_numbers:
                self.selected_numbers.remove(number)
                label.setStyleSheet("font-size: 24px; font-weight: bold; color: black; background-color: none; border: none;")
            else:
                self.selected_numbers.add(number)
                col_index = (number - 1) // 15
                color_mapping = self.get_color(col_index)
                text_color = 'black' if col_index == 4 else ('black' if col_index == 2 else 'white')
                label.setStyleSheet(f"font-size: 24px; font-weight: bold; background-color: {color_mapping}; color: {text_color}; border: {'2px solid black' if col_index == 2 else 'none'};")

    def clear_display(self):
        self.selected_numbers.clear()
        for label in self.labels.values():
            label.setStyleSheet("font-size: 24px; font-weight: bold; color: black; background-color: none; border: none;")
        self.clear_template()

    def clear_template(self):
        for cell in self.template_cells.values():
            cell.setStyleSheet(cell.styleSheet().replace('background-color: orange;', '').replace('border-radius: 30px;', ''))

    def mark_n_column_as_called(self):
        for i in range(15):  # Marks all N column cells
            self.update_display(31 + i)  # 31 to 45 are the N column numbers

    def update_game_mode(self, mode):
        self.clear_template()
        self.template_label.setText(f"Game:\n{mode}")

        if mode == 'Single Bingo':
            self.highlight_template([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])

        elif mode == 'Double Bingo':
            # Corrected to have one horizontal and one vertical line
            self.highlight_template([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),  # Vertical
                                    (0, 1), (0, 2), (0, 3), (0, 4)])  # Horizontal

        elif mode == 'Triple Bingo':
            # Corrected to have one diagonal, one horizontal, and one vertical line
            self.highlight_template([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),  # Vertical
                                    (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),  # Horizontal
                                    (1, 1), (3, 3), (4, 4)])  # Diagonal

        elif mode == 'Letter X':
            # Draw all N balls and mark them on the master call sheet
            self.highlight_template([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4),  # Main diagonal
                                    (0, 4), (1, 3), (3, 1), (4, 0)])  # Cross diagonal
            self.mark_n_column_as_called()  # Custom function to mark all N balls

        elif mode == 'Corner Picture Frame':
            # First two and bottom two slots of B and O columns, top and bottom of I and G columns
            self.highlight_template([(0, 0), (1, 0), (3, 0), (4, 0),  # B Column
                                    (0, 4), (1, 4), (3, 4), (4, 4),  # O Column
                                    (0, 1), (4, 1),  # Top and bottom of I Column
                                    (0, 3), (4, 3)])  # Top and bottom of G Column
            self.mark_n_column_as_called()  # Custom function to mark all N balls

        elif mode == 'Check Mark':
            # Diagonal bottom B to top O, B's 3rd and 4th downs
            self.highlight_template([(4, 0), (3, 1), (2, 2), (1, 3), (0, 4),  # Diagonal
                                    (2, 0), (3, 0)])  # B's 3rd and 4th downs

        elif mode == 'Four Corners':
            self.highlight_template([(0, 0), (0, 4), (4, 0), (4, 4)])

        elif mode == 'Heart':
            # B's 2nd and 3rd, I's 1st and 4th, N's 2nd and 5th, G's 1st and 4th, O's 2nd and 3rd
            self.highlight_template([(1, 0), (2, 0),  # B's 2nd and 3rd
                                    (0, 1), (3, 1),  # I's 1st and 4th
                                    (1, 2), (4, 2),  # N's 2nd and 5th
                                    (0, 3), (3, 3),  # G's 1st and 4th
                                    (1, 4), (2, 4)])  # O's 2nd and 3rd

        elif mode == 'Postage Stamp':
            self.highlight_template([(0, 0), (0, 1), (1, 0), (1, 1),  # Top-left
                                    (3, 3), (3, 4), (4, 3), (4, 4)])  # Bottom-right

        elif mode == 'Block of 8':
            # I, N, G, O columns, 2nd and 3rd downs to create a block of 8
            self.highlight_template([(1, 1), (2, 1),  # I column
                                    (1, 2), (2, 2),  # N column
                                    (1, 3), (2, 3),  # G column
                                    (1, 4), (2, 4)])  # O column

        elif mode == 'Blackout':
            self.highlight_template([(i, j) for i in range(5) for j in range(5)])

    def toggle_template_cell(self, pos):
        cell = self.template_cells[pos]
        current_style = cell.styleSheet()
        if 'background-color: orange;' in current_style:
            cell.setStyleSheet(current_style.replace('background-color: orange;', '').replace('border-radius: 30px;', ''))
        else:
            cell.setStyleSheet(current_style + 'background-color: orange; border-radius: 30px;')

    def highlight_template(self, positions):
        for i, j in positions:
            self.toggle_template_cell((i, j))

class BingoApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.up_next_window = UpNextWindow()
        self.control_window = ControlWindow()
        self.display_window = DisplayWindow()
        self.ball_selector_window = BallSelectorWindow(self.up_next_window)

        self.control_window.number_selected.connect(self.display_window.update_display)
        self.control_window.number_selected.connect(self.ball_selector_window.handle_manual_selection)
        self.control_window.game_mode_selected.connect(self.display_window.update_game_mode)
        self.control_window.clear_selection.connect(self.display_window.clear_display)
        self.control_window.manual_mode_entered.connect(self.display_window.update_game_mode)
        self.control_window.draw_ball.connect(self.draw_ball)
        self.control_window.reset_ball_selector.connect(self.ball_selector_window.reset)

        self.control_window.show()
        self.display_window.show()
        self.ball_selector_window.show()
        self.up_next_window.show()

    def draw_ball(self):
        ball = self.ball_selector_window.draw_ball()
        if ball:
            self.display_window.update_display(ball)

if __name__ == '__main__':
    app = BingoApp(sys.argv)
    sys.exit(app.exec_())