import pandas as pd
import os
from tkinter import Tk, Label, Button, messagebox
from playsound import playsound

if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as file:
        file.write("0")


data = pd.read_csv('List of most-followed Instagram accounts.csv')

def get_random_influencer(data):
    return data.sample(n=1).iloc[0]

class HigherOrLowerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Higher or Lower")
        self.score = 0
        self.current_influencer = get_random_influencer(data)
        self.next_influencer = get_random_influencer(data)
        
        self.label_info = Label(root, text="", width=50, height=7, font=("Arial", 14), justify="left")
        self.label_info.pack(pady=20)

        self.new_label_info = Label(root, text="", width=50, height=5, font=("Arial", 14), justify="left")
        self.new_label_info.pack(pady=20)

        self.score_label = Label(root, text="", font=("Arial", 20), justify="left")
        self.score_label.pack(pady=20)
        
        self.button_higher = Button(root, text="Higher", command=lambda: self.check_guess("higher"), font=("Arial", 12), bg="green", fg="white")
        self.button_higher.pack(side="left", padx=20, pady=10)
        
        self.button_lower = Button(root, text="Lower", command=lambda: self.check_guess("lower"), font=("Arial", 12), bg="red", fg="white")
        self.button_lower.pack(side="right", padx=20, pady=10)
        
        self.update_ui()

    def update_ui(self):
        influencer_info = (
            f"Instagram username: {self.current_influencer['Username']}\n"
            f"Owner: {self.current_influencer['Owner']}\n"
            f"Domain of activity: {self.current_influencer['Profession/Activity']}\n"
            f"Country: {self.current_influencer['Country/Continent']}\n"
            f"Followers: {self.current_influencer['Followers(millions)']} Millions\n"
        )
        self.label_info.config(text=influencer_info)

        next_influencer_info = (
            f"\n"
            f"Instagram username: {self.next_influencer['Username']}\n"
            f"Owner: {self.next_influencer['Owner']}\n"
            f"Domain of activity: {self.next_influencer['Profession/Activity']}\n"
            f"Country: {self.next_influencer['Country/Continent']}\n"
        )
        self.new_label_info.config(text=next_influencer_info)

        self.score_label.config(text=f"\nScore: {self.score}\n")

    def check_guess(self, guess):
        while self.next_influencer['Username'] == self.current_influencer['Username']:
            self.next_influencer = get_random_influencer(data)
        
        correct_guess = (
            (guess == "higher" and float(self.next_influencer['Followers(millions)']) > float(self.current_influencer['Followers(millions)'])) or
            (guess == "lower" and float(self.next_influencer['Followers(millions)']) < float(self.current_influencer['Followers(millions)']))
        )

        if correct_guess:
            self.score += 1
            playsound('correct.wav')
            self.current_influencer = self.next_influencer
            self.next_influencer = get_random_influencer(data)
            self.update_ui()
        else:
            playsound('wrong.wav')
            final_score = self.score
            with open("highscore.txt", "r") as file:
                highscore = int(file.read())
            if final_score > highscore:
                with open("highscore.txt", "w") as file:
                    file.write(str(final_score))
                highscore = final_score

            messagebox.showinfo("Game Over", f"Game over! Your final score is {final_score}.\nHighscore: {highscore}")
            self.root.destroy()


root = Tk()
game = HigherOrLowerGame(root)
root.geometry("600x600")
root.configure(bg="lightblue")
root.mainloop()
