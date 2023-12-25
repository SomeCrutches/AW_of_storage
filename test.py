import tkinter as tk
from tkinter import filedialog


class ColorGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Grid")

        # Параметры по умолчанию
        self.rows = 15
        self.cols = 15
        self.cell_size = 30
        self.selected_color = 3  # Исходный цвет - красный
        self.white_color = 2  # Белый цвет

        self.colors = {
            1: "black",
            2: "white",
            3: "red",
            4: "green"
        }

        self.color_sequence = ""

        self.create_widgets()

    def create_widgets(self):
        # Создание холста
        self.canvas = tk.Canvas(self.root, width=self.cols * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()

        # Создание кнопок для выбора цвета
        color_buttons = []
        for color_code, color_name in self.colors.items():
            button = tk.Button(self.root, text=color_name, command=lambda c=color_code: self.set_color(c))
            color_buttons.append(button)
            button.pack(side=tk.LEFT, padx=5)

        # Создание текстовых полей для ввода размеров сетки
        tk.Label(self.root, text="Rows:").pack(side=tk.LEFT)
        self.rows_entry = tk.Entry(self.root)
        self.rows_entry.insert(0, str(self.rows))
        self.rows_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.root, text="Cols:").pack(side=tk.LEFT)
        self.cols_entry = tk.Entry(self.root)
        self.cols_entry.insert(0, str(self.cols))
        self.cols_entry.pack(side=tk.LEFT, padx=5)

        # Кнопка для обновления сетки
        update_button = tk.Button(self.root, text="Update Grid", command=self.update_grid)
        update_button.pack(side=tk.LEFT, padx=5)

        # Текстовое поле для импорта цветов
        tk.Label(self.root, text="Color Sequence:").pack(side=tk.LEFT)
        self.color_sequence_entry = tk.Entry(self.root)
        self.color_sequence_entry.pack(side=tk.LEFT, padx=5)

        # Кнопка для применения цветовой последовательности
        apply_color_sequence_button = tk.Button(self.root, text="Apply Sequence", command=self.apply_color_sequence)
        apply_color_sequence_button.pack(side=tk.LEFT, padx=5)

        # Кнопка для экспорта цветовой последовательности
        export_button = tk.Button(self.root, text="Export Sequence", command=self.export_color_sequence)
        export_button.pack(side=tk.LEFT, padx=5)

        # Кнопка для импорта цветовой последовательности из файла
        import_button = tk.Button(self.root, text="Import Sequence", command=self.import_color_sequence)
        import_button.pack(side=tk.LEFT, padx=5)

        # Инициализация сетки
        self.grid = [[2 for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()

        # Обработка событий для ручного окрашивания клеток
        self.canvas.bind("<B1-Motion>", lambda event: self.paint_cell(event, self.selected_color))
        self.canvas.bind("<B3-Motion>", lambda event: self.paint_cell(event, self.white_color))

    def set_color(self, color_code):
        self.selected_color = color_code

    def draw_grid(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = self.colors[self.grid[row][col]]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        # Обновление текстового поля с цветовой последовательностью
        self.color_sequence_entry.delete(0, tk.END)
        self.color_sequence_entry.insert(0, self.get_color_sequence())

    def update_grid(self):
        try:
            self.rows = int(self.rows_entry.get())
            self.cols = int(self.cols_entry.get())
        except ValueError:
            return

        self.grid = [[2 for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_grid()

    def apply_color_sequence(self):
        self.color_sequence = self.color_sequence_entry.get()
        self.update_color_sequence()

    def update_color_sequence(self):
        row = 0
        col = 0
        for color_code in self.color_sequence:
            color_code = int(color_code)
            if col >= self.cols:
                col = 0
                row += 1
            if row >= self.rows:
                break
            self.grid[row][col] = color_code
            col += 1
        self.draw_grid()

    def paint_cell(self, event, color):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = color
            self.draw_grid()

    def get_color_sequence(self):
        return "".join(str(self.grid[row][col]) for row in range(self.rows) for col in range(self.cols))

    def export_color_sequence(self):
        exported_sequence = self.get_color_sequence()

        # Спросим у пользователя о месте сохранения файла
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        # Если пользователь выбрал место сохранения, сохраняем последовательность в файл
        if file_path:
            with open(file_path, "w") as file:
                file.write(exported_sequence)
            print(f"Exported Sequence saved to {file_path}")

    def import_color_sequence(self):
        # Спросим у пользователя о месте выбора файла
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        # Если пользователь выбрал файл, читаем последовательность из файла и обновляем сетку
        if file_path:
            with open(file_path, "r") as file:
                imported_sequence = file.read()
                self.color_sequence_entry.delete(0, tk.END)
                self.color_sequence_entry.insert(0, imported_sequence)
                self.color_sequence = imported_sequence
                self.update_color_sequence()


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorGridApp(root)
    root.mainloop()
