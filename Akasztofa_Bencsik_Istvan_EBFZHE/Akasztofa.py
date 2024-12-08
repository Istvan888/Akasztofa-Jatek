import tkinter as tk
from tkinter import messagebox
from random import choice

MAX_WRONG_GUESSES = 6


class HangmanGame:
    def __init__(self, root, word_list, label_word, label_status, buttons):
        self.root = root
        self.word_list = word_list
        self.label_word = label_word
        self.label_status = label_status
        self.buttons = buttons
        self.target_word = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.new_game()

    def new_game(self):
        """Új játék inicializálása."""
        self.target_word = choice(self.word_list).upper()
        self.guessed_letters = set()
        self.wrong_guesses = 0

        # Reset GUI
        for button in self.buttons.values():
            button.config(state=tk.NORMAL)
        self.update_display()

    def update_display(self):
        """Frissíti a játék állapotát a képernyőn."""
        displayed_word = " ".join(
            [letter if letter in self.guessed_letters else "_" for letter in self.target_word]
        )
        self.label_word.config(text=displayed_word)
        self.label_status.config(
            text=f"Hibás próbálkozások: {self.wrong_guesses}/{MAX_WRONG_GUESSES}"
        )

    def handle_guess(self, letter):
        """Kezeli a betűtippet."""
        if letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)
        self.buttons[letter].config(state=tk.DISABLED)

        if letter in self.target_word:
            if all(letter in self.guessed_letters for letter in self.target_word):
                self.end_game(won=True)
        else:
            self.wrong_guesses += 1
            if self.wrong_guesses >= MAX_WRONG_GUESSES:
                self.end_game(won=False)

        self.update_display()

    def end_game(self, won):
        """Játék vége: győzelem vagy vereség."""
        if won:
            messagebox.showinfo("Győzelem", f"Gratulálok! Nyertél!\nA szó: {self.target_word}")
        else:
            messagebox.showinfo("Vereség", f"Sajnos vesztettél!\nA helyes szó: {self.target_word}")

        self.new_game()


def load_words(file_path):
    """Betölti a szavakat a words.txt fájlból."""
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            words = [line.strip().upper() for line in file if line.strip()]
        return words
    except FileNotFoundError:
        messagebox.showerror("Hiba", "A words.txt fájl nem található!")
        return []


def create_gui(word_list):
    """Létrehozza a grafikus felületet."""
    root = tk.Tk()
    root.title("Akasztófa")

    # Játék címkéje
    label_word = tk.Label(root, text="", font=("Courier", 24), pady=20)
    label_word.pack()

    # Státusz címke
    label_status = tk.Label(root, text="", font=("Arial", 14), pady=10)
    label_status.pack()

    # Betűk gombjai
    button_frame = tk.Frame(root)
    button_frame.pack()
    buttons = {}
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        button = tk.Button(
            button_frame,
            text=letter,
            font=("Arial", 14),
            width=4,
            command=lambda l=letter: game.handle_guess(l),
        )
        button.grid(row=(ord(letter) - 65) // 9, column=(ord(letter) - 65) % 9)
        buttons[letter] = button

    # Új játék gomb
    new_game_button = tk.Button(
        root, text="Új játék", font=("Arial", 14), command=lambda: game.new_game()
    )
    new_game_button.pack(pady=10)

    # Játék inicializálása
    game = HangmanGame(root, word_list, label_word, label_status, buttons)
    root.mainloop()


if __name__ == "__main__":
    word_file = "words.txt"
    loaded_words = load_words(word_file) 
    if loaded_words:
        create_gui(loaded_words)
