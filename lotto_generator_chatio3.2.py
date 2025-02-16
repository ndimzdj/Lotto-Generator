import csv
import random
from collections import Counter
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lottery Number Generator")
        self.root.geometry("900x700")
        self.root.tk.call('tk', 'scaling', 2.0)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Home Tab
        self.home_frame = tk.Frame(self.notebook)
        self.notebook.add(self.home_frame, text="Home")

        # Randomize Tab
        self.randomize_frame = tk.Frame(self.notebook)
        self.notebook.add(self.randomize_frame, text="Randomize")

        self.setup_home_tab()
        self.setup_randomize_tab()

    def setup_home_tab(self):
        # Add Dark/Light Mode Toggle
        self.current_theme = tk.StringVar(value="Light")
        self.theme_menu = ttk.Combobox(self.home_frame, textvariable=self.current_theme, values=["Light", "Dark"], state="readonly")
        self.theme_menu.bind("<<ComboboxSelected>>", self.toggle_theme)
        self.theme_menu.pack(pady=5)

        # Title Label
        self.title_label = tk.Label(self.home_frame, text="Lottery Number Generator", font=("Helvetica", 18))
        self.title_label.pack(pady=10)

        # Lotto Machine Canvas
        self.lotto_canvas = tk.Canvas(self.home_frame, width=700, height=500, bg="lightgray")
        self.lotto_canvas.pack(pady=10, expand=True, fill="both")

        # Browse Button
        self.browse_button = ttk.Button(self.home_frame, text="Browse Lottery Data File", command=self.browse_file)
        self.browse_button.pack(pady=10)

        # Result Label
        self.result_label = tk.Label(self.home_frame, text="", font=("Helvetica", 14), wraplength=700, justify="center")
        self.result_label.pack(pady=10)

        # Seed and Pattern Analysis Labels
        self.seed_frame = tk.Frame(self.home_frame)
        self.seed_frame.pack(pady=10)

        self.seed_label = tk.Label(self.seed_frame, text="", font=("Helvetica", 14), wraplength=700, justify="center", fg="blue")
        self.seed_label.pack(pady=5)

        self.bonus_label = tk.Label(self.seed_frame, text="", font=("Helvetica", 14), wraplength=700, justify="center", fg="green")
        self.bonus_label.pack(pady=5)

        # Placeholder for table of past results
        self.results_table = ttk.Treeview(self.home_frame, columns=("Draw", "Numbers", "Bonus"), show="headings")
        self.results_table.heading("Draw", text="Draw")
        self.results_table.heading("Numbers", text="Numbers")
        self.results_table.heading("Bonus", text="Bonus")
        self.results_table.pack(pady=10, fill="x")

    def setup_randomize_tab(self):
        self.randomize_canvas = tk.Canvas(self.randomize_frame, width=700, height=500, bg="lightgray")
        self.randomize_canvas.pack(pady=10, expand=True, fill="both")

        self.randomize_button = ttk.Button(self.randomize_frame, text="Generate Randomized Numbers", command=self.randomize_numbers)
        self.randomize_button.pack(pady=10)

        self.randomize_result_label = tk.Label(self.randomize_frame, text="", font=("Helvetica", 14), wraplength=700, justify="center")
        self.randomize_result_label.pack(pady=10)

    def toggle_theme(self, event):
        theme = self.current_theme.get()
        if theme == "Dark":
            self.root.configure(bg="black")
            self.title_label.configure(bg="black", fg="white")
            self.result_label.configure(bg="black", fg="white")
            self.seed_label.configure(bg="black", fg="cyan")
            self.bonus_label.configure(bg="black", fg="lime")
            self.lotto_canvas.configure(bg="darkgray")
            self.randomize_canvas.configure(bg="darkgray")
            self.randomize_result_label.configure(bg="black", fg="white")
        else:
            self.root.configure(bg="SystemButtonFace")
            self.title_label.configure(bg="SystemButtonFace", fg="black")
            self.result_label.configure(bg="SystemButtonFace", fg="black")
            self.seed_label.configure(bg="SystemButtonFace", fg="blue")
            self.bonus_label.configure(bg="SystemButtonFace", fg="green")
            self.lotto_canvas.configure(bg="lightgray")
            self.randomize_canvas.configure(bg="lightgray")
            self.randomize_result_label.configure(bg="SystemButtonFace", fg="black")

    def browse_file(self):
        file_path = filedialog.askopenfilename(title="Select Lottery Data File", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                main_numbers, bonus_numbers = self.load_lottery_data(file_path)
                frequencies = self.calculate_frequencies(main_numbers)
                lotto_numbers = self.generate_lotto_numbers(frequencies)
                main_most_common, bonus_most_common = self.analyze_seed_and_patterns(main_numbers, bonus_numbers)

                # Display results
                self.result_label.config(text=f"Generated Lottery Numbers: {', '.join(map(str, lotto_numbers))}\nPredicted Bonus Number: {bonus_most_common[0][0]} (Bonus)")
                self.seed_label.config(text=f"Most Common Numbers: {', '.join(f'{num} ({freq})' for num, freq in main_most_common)}")
                self.bonus_label.config(text=f"Most Common Bonus Number: {bonus_most_common[0][0]} ({bonus_most_common[0][1]})")

                # Update results table
                for i, row in enumerate(zip(main_numbers, bonus_numbers)):
                    self.results_table.insert("", "end", values=(i + 1, ', '.join(map(str, row[:-1])), row[-1]))

            except Exception as e:
                messagebox.showerror("Error", str(e))

    def randomize_numbers(self):
        try:
            # Simulate a randomized draw based on historical data
            randomized_numbers = random.sample(range(1, 50), 6)
            self.animate_randomize_lotto_machine(randomized_numbers)
            self.randomize_result_label.config(text=f"Randomized Numbers: {', '.join(map(str, randomized_numbers))}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def animate_randomize_lotto_machine(self, numbers):
        self.randomize_canvas.delete("all")
        ball_positions = [(100 + i * 80, 200) for i in range(len(numbers))]
        ball_colors = ["red", "blue", "green", "yellow", "purple", "orange"]

        balls = []
        for pos, color, number in zip(ball_positions, ball_colors, numbers):
            x, y = pos
            ball = self.randomize_canvas.create_oval(x, y, x + 50, y + 50, fill=color, outline="black")
            self.randomize_canvas.create_text(x + 25, y + 25, text=str(number), fill="white", font=("Helvetica", 14))
            balls.append(ball)

        for _ in range(20):
            for ball in balls:
                self.randomize_canvas.move(ball, 0, random.choice([-5, 5]))
            self.randomize_canvas.update()
            time.sleep(0.05)

    def load_lottery_data(self, file_path):
        """
        Load historical lottery data from a CSV file.
        The file should contain past winning numbers, one draw per row.
        """
        main_numbers = []
        bonus_numbers = []
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    *main, bonus = map(int, row)
                    main_numbers.append(main)
                    bonus_numbers.append(bonus)
                except ValueError:
                    raise ValueError(f"Invalid data in file: {row}")
        return main_numbers, bonus_numbers

    def calculate_frequencies(self, numbers):
        return Counter(num for row in numbers for num in row)

    def generate_lotto_numbers(self, frequencies, num_numbers=6, number_range=49):
        numbers, weights = zip(*[(num, frequencies.get(num, 0) + 1) for num in range(1, number_range + 1)])
        selected_numbers = set()
        while len(selected_numbers) < num_numbers:
            selected_numbers.add(random.choices(numbers, weights=weights, k=1)[0])
        return sorted(selected_numbers)

    def analyze_seed_and_patterns(self, main_numbers, bonus_numbers):
        main_freq = self.calculate_frequencies(main_numbers)
        bonus_freq = Counter(bonus_numbers)
        main_most_common = main_freq.most_common(5)
        bonus_most_common = bonus_freq.most_common(1)
        return main_most_common, bonus_most_common

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()
