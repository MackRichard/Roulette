import secrets
import tkinter as tk


WHEEL = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
COLORS = {"red": "#c74b4b", "black": "#202522", "green": "#287a56"}


class RouletteGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Roulette")
        self.root.geometry("1040x720")
        self.root.minsize(900, 650)
        self.root.configure(bg="#111815")

        self.balance = 100
        self.bet_mode = None
        self.selected_numbers = set()
        self.number_buttons = {}
        self.history = []
        self.spinning = False
        self.palette = {
            "background": "#111815",
            "panel": "#1b2620",
            "felt": "#15523d",
            "felt_dark": "#103d2e",
            "gold": "#d8b66a",
            "text": "#f2eee3",
            "muted": "#9ba79c",
            "red": COLORS["red"],
            "black": COLORS["black"],
            "green": COLORS["green"],
        }

        self.build_ui()
        self.refresh_controls()

    def build_ui(self):
        header = tk.Frame(self.root, bg=self.palette["background"])
        header.pack(fill="x", padx=32, pady=(24, 16))

        title_block = tk.Frame(header, bg=self.palette["background"])
        title_block.pack(side="left")
        tk.Label(
            title_block,
            text="EUROPEAN TABLE",
            font=("Segoe UI", 10, "bold"),
            fg=self.palette["gold"],
            bg=self.palette["background"],
        ).pack(anchor="w")
        tk.Label(
            title_block,
            text="Roulette",
            font=("Georgia", 28, "bold"),
            fg=self.palette["text"],
            bg=self.palette["background"],
        ).pack(anchor="w", pady=(2, 0))

        balance_box = tk.Frame(header, bg=self.palette["panel"], padx=18, pady=10)
        balance_box.pack(side="right")
        tk.Label(
            balance_box,
            text="GUTHABEN",
            font=("Segoe UI", 9, "bold"),
            fg=self.palette["muted"],
            bg=self.palette["panel"],
        ).pack(anchor="e")
        self.balance_label = tk.Label(
            balance_box,
            text="100 $",
            font=("Georgia", 20, "bold"),
            fg=self.palette["gold"],
            bg=self.palette["panel"],
        )
        self.balance_label.pack(anchor="e")

        self.result_panel = tk.Frame(self.root, bg=self.palette["felt_dark"], height=150)
        self.result_panel.pack(fill="x", padx=32)
        self.result_panel.pack_propagate(False)
        result_content = tk.Frame(self.result_panel, bg=self.palette["felt_dark"])
        result_content.pack(expand=True)
        tk.Label(
            result_content,
            text="LETZTES ERGEBNIS",
            font=("Segoe UI", 9, "bold"),
            fg="#b8c5bb",
            bg=self.palette["felt_dark"],
        ).pack(pady=(13, 4))
        self.result_number = tk.Label(
            result_content,
            text="?",
            font=("Georgia", 34, "bold"),
            fg=self.palette["text"],
            bg=self.palette["green"],
            width=3,
            height=1,
        )
        self.result_number.pack()
        self.status_label = tk.Label(
            result_content,
            text="Wähle eine Farbe oder eine Zahl.",
            font=("Segoe UI", 10),
            fg=self.palette["text"],
            bg=self.palette["felt_dark"],
        )
        self.status_label.pack(pady=(6, 0))

        content = tk.Frame(self.root, bg=self.palette["background"])
        content.pack(fill="both", expand=True, padx=32, pady=20)
        board_area = tk.Frame(content, bg=self.palette["background"])
        board_area.pack(side="left", fill="both", expand=True)
        side_panel = tk.Frame(content, bg=self.palette["background"], width=245)
        side_panel.pack(side="right", fill="y", padx=(24, 0))
        side_panel.pack_propagate(False)

        tk.Label(
            board_area,
            text="TISCH",
            font=("Segoe UI", 9, "bold"),
            fg=self.palette["muted"],
            bg=self.palette["background"],
        ).pack(anchor="w", pady=(0, 9))
        board = tk.Frame(board_area, bg=self.palette["felt"], padx=10, pady=10)
        board.pack(fill="both", expand=True)
        zero = self.make_number_button(board, 0)
        zero.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=(0, 7), pady=2)
        for column in range(12):
            for row in range(3):
                number = column * 3 + (3 - row)
                button = self.make_number_button(board, number)
                button.grid(row=row, column=column + 1, sticky="nsew", padx=2, pady=2)
        for column in range(13):
            board.columnconfigure(column, weight=1, uniform="board")
        for row in range(3):
            board.rowconfigure(row, weight=1, uniform="board")

        self.history_label = tk.Label(
            board_area,
            text="KEINE VORHERIGEN ERGEBNISSE",
            font=("Segoe UI", 9),
            fg=self.palette["muted"],
            bg=self.palette["background"],
            anchor="w",
        )
        self.history_label.pack(fill="x", pady=(12, 0))

        tk.Label(
            side_panel,
            text="EINSATZ",
            font=("Segoe UI", 9, "bold"),
            fg=self.palette["muted"],
            bg=self.palette["background"],
        ).pack(anchor="w", pady=(0, 8))
        self.bet_entry = tk.Spinbox(
            side_panel,
            from_=1,
            to=self.balance,
            width=12,
            font=("Segoe UI", 14),
            bg=self.palette["panel"],
            fg=self.palette["text"],
            buttonbackground=self.palette["panel"],
            insertbackground=self.palette["text"],
            relief="flat",
            justify="center",
        )
        self.bet_entry.pack(fill="x", ipady=7)

        tk.Label(
            side_panel,
            text="FARBE",
            font=("Segoe UI", 9, "bold"),
            fg=self.palette["muted"],
            bg=self.palette["background"],
        ).pack(anchor="w", pady=(20, 8))
        color_row = tk.Frame(side_panel, bg=self.palette["background"])
        color_row.pack(fill="x")
        self.color_buttons = {}
        for label, mode, color in (
            ("Rot", "red", self.palette["red"]),
            ("Schwarz", "black", self.palette["black"]),
            ("Grün", "green", self.palette["green"]),
        ):
            button = tk.Button(
                color_row,
                text=label,
                command=lambda selected=mode: self.select_color(selected),
                font=("Segoe UI", 9, "bold"),
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                relief="flat",
                padx=7,
                pady=9,
                cursor="hand2",
            )
            button.pack(side="left", expand=True, fill="x", padx=(0, 4))
            self.color_buttons[mode] = button

        self.bet_summary = tk.Label(
            side_panel,
            text="Kein Einsatz gewählt",
            font=("Segoe UI", 10),
            fg=self.palette["text"],
            bg=self.palette["background"],
            justify="left",
            wraplength=230,
            anchor="w",
        )
        self.bet_summary.pack(fill="x", pady=(18, 12))

        self.spin_button = tk.Button(
            side_panel,
            text="DREHEN",
            command=self.start_spin,
            font=("Segoe UI", 11, "bold"),
            bg=self.palette["gold"],
            fg="#182019",
            activebackground="#e8cb87",
            activeforeground="#182019",
            disabledforeground="#7f887f",
            relief="flat",
            pady=13,
            cursor="hand2",
        )
        self.spin_button.pack(fill="x")
        tk.Button(
            side_panel,
            text="Auswahl löschen",
            command=self.clear_selection,
            font=("Segoe UI", 9),
            bg=self.palette["background"],
            fg=self.palette["muted"],
            activebackground=self.palette["background"],
            activeforeground=self.palette["text"],
            relief="flat",
            cursor="hand2",
        ).pack(fill="x", pady=(8, 0))
        tk.Button(
            side_panel,
            text="Neues Spiel",
            command=self.new_game,
            font=("Segoe UI", 9),
            bg=self.palette["background"],
            fg=self.palette["muted"],
            activebackground=self.palette["background"],
            activeforeground=self.palette["text"],
            relief="flat",
            cursor="hand2",
        ).pack(fill="x", pady=(3, 0))

    def make_number_button(self, parent, number):
        color = self.number_color(number)
        button = tk.Button(
            parent,
            text=str(number),
            command=lambda value=number: self.toggle_number(value),
            font=("Segoe UI", 10, "bold"),
            bg=color,
            fg="white",
            activebackground=color,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
        )
        self.number_buttons[number] = button
        return button

    @staticmethod
    def number_color(number):
        if number == 0:
            return COLORS["green"]
        return COLORS["red"] if number in RED_NUMBERS else COLORS["black"]

    def select_color(self, color):
        if self.spinning:
            return
        self.bet_mode = color
        self.selected_numbers.clear()
        self.refresh_controls()

    def toggle_number(self, number):
        if self.spinning:
            return
        if self.bet_mode != "numbers":
            self.bet_mode = "numbers"
            self.selected_numbers.clear()
        if number in self.selected_numbers:
            self.selected_numbers.remove(number)
        else:
            self.selected_numbers.add(number)
        if not self.selected_numbers:
            self.bet_mode = None
        self.refresh_controls()

    def clear_selection(self):
        if self.spinning:
            return
        self.bet_mode = None
        self.selected_numbers.clear()
        self.refresh_controls()
        self.status_label.config(text="Wähle eine Farbe oder eine Zahl.", fg=self.palette["text"])

    def refresh_controls(self):
        self.balance_label.config(text=f"{self.balance} $")
        self.bet_entry.config(to=max(self.balance, 1))
        for mode, button in self.color_buttons.items():
            button.config(relief="sunken" if self.bet_mode == mode else "flat", bd=2 if self.bet_mode == mode else 0)
        for number, button in self.number_buttons.items():
            button.config(relief="sunken" if number in self.selected_numbers else "flat", bd=2 if number in self.selected_numbers else 0)

        if self.bet_mode == "numbers":
            numbers = ", ".join(str(number) for number in sorted(self.selected_numbers))
            self.bet_summary.config(text=f"Zahlen: {numbers}" if numbers else "Zahlen auswählen")
        elif self.bet_mode:
            labels = {"red": "Rot", "black": "Schwarz", "green": "Grün"}
            self.bet_summary.config(text=f"Farbe: {labels[self.bet_mode]}")
        else:
            self.bet_summary.config(text="Kein Einsatz gewählt")

        self.spin_button.config(state="normal" if self.bet_mode and self.balance > 0 and not self.spinning else "disabled")

    def start_spin(self):
        if self.spinning or not self.bet_mode:
            return
        try:
            stake = int(self.bet_entry.get())
        except ValueError:
            self.status_label.config(text="Bitte einen gültigen Einsatz eingeben.", fg="#ef8880")
            return
        if stake <= 0 or stake > self.balance:
            self.status_label.config(text=f"Der Einsatz muss zwischen 1 und {self.balance} $ liegen.", fg="#ef8880")
            return

        self.balance -= stake
        self.spinning = True
        self.pending_stake = stake
        self.winning_number = secrets.choice(WHEEL)
        self.spin_frame = 0
        self.refresh_controls()
        self.status_label.config(text="Die Kugel rollt ...", fg=self.palette["text"])
        self.animate_spin()

    def animate_spin(self):
        if self.spin_frame < 34:
            number = secrets.choice(WHEEL)
            self.result_number.config(text=str(number), bg=self.number_color(number))
            delay = 35 + self.spin_frame * 4
            self.spin_frame += 1
            self.root.after(delay, self.animate_spin)
            return
        self.finish_spin()

    def finish_spin(self):
        number = self.winning_number
        color = self.number_color(number)
        self.result_number.config(text=str(number), bg=color)
        won = (self.bet_mode == "red" and color == COLORS["red"]) or (self.bet_mode == "black" and color == COLORS["black"]) or (self.bet_mode == "green" and number == 0)
        if self.bet_mode == "numbers" and number in self.selected_numbers:
            payout = round(self.pending_stake * 36 / len(self.selected_numbers))
        elif won:
            payout = self.pending_stake * (36 if number == 0 else 2)
        else:
            payout = 0
        self.balance += payout
        self.history.insert(0, number)
        self.history = self.history[:8]
        self.history_label.config(text="LETZTE ERGEBNISSE   " + "   ".join(str(item) for item in self.history))

        if payout:
            profit = payout - self.pending_stake
            self.status_label.config(text=f"Gewonnen: +{profit} $   ·   Auszahlung {payout} $", fg="#9cdbad")
        elif self.balance == 0:
            self.status_label.config(text="Kein Guthaben mehr. Starte ein neues Spiel.", fg="#ef8880")
        else:
            self.status_label.config(text=f"Leider verloren. Einsatz: {self.pending_stake} $", fg="#efb0a9")

        self.spinning = False
        self.refresh_controls()

    def new_game(self):
        if self.spinning:
            return
        self.balance = 100
        self.history.clear()
        self.history_label.config(text="KEINE VORHERIGEN ERGEBNISSE")
        self.result_number.config(text="?", bg=self.palette["green"])
        self.status_label.config(text="Neues Spiel gestartet. Wähle deinen Einsatz.", fg=self.palette["text"])
        self.bet_entry.delete(0, "end")
        self.bet_entry.insert(0, "1")
        self.bet_mode = None
        self.selected_numbers.clear()
        self.refresh_controls()


if __name__ == "__main__":
    window = tk.Tk()
    game = RouletteGame(window)
    window.mainloop()
