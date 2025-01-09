import random
from itertools import permutations
import tkinter as tk
from tkinter import messagebox

def calculate_hit_and_blow(answer, guess):
    # ヒットとブローを計算
    hit = sum(a == g for a, g in zip(answer, guess))
    blow = sum(g in answer for g in guess) - hit
    return hit, blow

def ai_guess(possible_answers):
    # AIが次に推測する答えを選ぶ
    return random.choice(possible_answers)

class HitAndBlowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ヒット＆ブロー")

        # プレイヤーのUI
        self.label_player = tk.Label(root, text="プレイヤーの推測 (4桁の数字):")
        self.label_player.pack()

        self.entry_player = tk.Entry(root)
        self.entry_player.pack()

        self.submit_button = tk.Button(root, text="送信", command=self.player_turn)
        self.submit_button.pack()

        # AIのUI
        self.label_ai = tk.Label(root, text="AIがあなたの答えを推測します。4桁の答えを設定してください。")
        self.label_ai.pack()

        self.entry_ai = tk.Entry(root)
        self.entry_ai.pack()

        self.set_button = tk.Button(root, text="設定", command=self.set_player_answer)
        self.set_button.pack()

        # 出力表示
        self.output = tk.Text(root, height=20, width=60, state=tk.DISABLED)
        self.output.pack()

        # ゲーム状態
        self.player_answer = None
        self.ai_answer = None
        self.player_attempts = 0
        self.ai_attempts = 0
        self.ai_possible_answers = list(permutations(range(10), 4))

        # リスタートボタン
        self.restart_button = tk.Button(root, text="リスタート", command=self.restart, state=tk.DISABLED)
        self.restart_button.pack()

    def set_player_answer(self):
        user_answer = self.entry_ai.get()
        if len(user_answer) == 4 and user_answer.isdigit() and len(set(user_answer)) == 4:
            self.player_answer = list(map(int, user_answer))
            self.entry_ai.delete(0, tk.END)
            self.entry_ai.config(state=tk.DISABLED)
            self.set_button.config(state=tk.DISABLED)
            self.output.config(state=tk.NORMAL)
            self.output.insert(tk.END, "答えが設定されました。プレイヤーとAIの対決を始めます！\n")
            self.output.config(state=tk.DISABLED)
        else:
            messagebox.showerror("エラー", "無効な入力です。4桁の重複しない数字を入力してください。")

    def player_turn(self):
        if not self.player_answer:
            messagebox.showerror("エラー", "まずAIの答えを設定してください。")
            return

        player_guess = self.entry_player.get()
        if len(player_guess) != 4 or not player_guess.isdigit() or len(set(player_guess)) != 4:
            messagebox.showerror("エラー", "無効な入力です。4桁の重複しない数字を入力してください。")
            return

        player_guess = list(map(int, player_guess))
        self.player_attempts += 1

        hit, blow = calculate_hit_and_blow(self.player_answer, player_guess)

        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, f"プレイヤーの推測: {''.join(map(str, player_guess))}\n")
        self.output.insert(tk.END, f"ヒット: {hit}, ブロー: {blow}\n\n")
        self.output.config(state=tk.DISABLED)

        if hit == 4:
            self.output.config(state=tk.NORMAL)
            self.output.insert(tk.END, f"プレイヤーが勝利しました！試行回数: {self.player_attempts}\n")
            self.output.config(state=tk.DISABLED)
            self.end_game()
        else:
            self.ai_turn()

    def ai_turn(self):
        if not self.ai_answer:
            self.ai_answer = random.sample(range(10), 4)

        guess = ai_guess(self.ai_possible_answers)
        self.ai_attempts += 1

        hit, blow = calculate_hit_and_blow(self.ai_answer, guess)

        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, f"AIの推測: {''.join(map(str, guess))}\n")
        self.output.insert(tk.END, f"ヒット: {hit}, ブロー: {blow}\n\n")
        self.output.config(state=tk.DISABLED)

        if hit == 4:
            self.output.config(state=tk.NORMAL)
            self.output.insert(tk.END, f"AIが勝利しました！試行回数: {self.ai_attempts}\n")
            self.output.config(state=tk.DISABLED)
            self.end_game()
        else:
            self.ai_possible_answers = [p for p in self.ai_possible_answers if calculate_hit_and_blow(p, guess) == (hit, blow)]

    def end_game(self):
        self.submit_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.NORMAL)

    def restart(self):
        self.player_answer = None
        self.ai_answer = None
        self.player_attempts = 0
        self.ai_attempts = 0
        self.ai_possible_answers = list(permutations(range(10), 4))

        self.entry_player.config(state=tk.NORMAL)
        self.entry_ai.config(state=tk.NORMAL)
        self.set_button.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.DISABLED)

        self.output.config(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)
        self.output.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = HitAndBlowApp(root)
    root.mainloop()
