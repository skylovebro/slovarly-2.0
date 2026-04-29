import os
import sys

# Фикс ошибки TclError (прописываем пути вручную)
tcl_path = r'C:\Users\Student\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
tk_path = r'C:\Users\Student\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

if os.path.exists(tcl_path):
    os.environ['TCL_LIBRARY'] = tcl_path
    os.environ['TK_LIBRARY'] = tk_path

import customtkinter as ctk
import random as rnd
from datetime import datetime, timedelta

ctk.set_appearance_mode("dark")

slovar = []
file_path = 'slovarly.txt'
stats_path = 'stats.txt'


def load_data():
    global slovar
    if not os.path.exists(file_path):
        open(file_path, 'w', encoding='utf-8').close()
    with open(file_path, 'r', encoding='utf-8') as f:
        slovar = [line.strip() for line in f if line.strip()]


def get_days_streak():
    if not os.path.exists(stats_path):
        return 0, ""
    with open(stats_path, 'r') as f:
        content = f.read().strip()
        if '|' in content:
            data = content.split('|')
            return int(data[0]), data[1]
    return 0, ""


def update_days_streak():
    streak, last_date = get_days_streak()
    today = datetime.now().date()
    if last_date == str(today): return streak

    yesterday = today - timedelta(days=1)
    new_streak = streak + 1 if last_date == str(yesterday) else 1

    with open(stats_path, 'w') as f:
        f.write(f"{new_streak}|{today}")
    return new_streak


load_data()


def parse(line):
    if " - " in line:
        parts = line.split(" - ", 1)
        return parts[0].strip(), parts[1].strip()
    return line.strip(), ""


def add_window():
    win = ctk.CTkToplevel(app)
    win.geometry("400x250")
    win.attributes("-topmost", True)

    w_in = ctk.CTkEntry(win, placeholder_text="Слово", width=200)
    w_in.pack(pady=10)
    d_in = ctk.CTkEntry(win, placeholder_text="Перевод", width=200)
    d_in.pack(pady=10)

    def save():
        if w_in.get() and d_in.get():
            entry = f"{w_in.get()} - {d_in.get()}"
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(entry + "\n")
            slovar.append(entry)
            win.destroy()

    ctk.CTkButton(win, text="Сохранить", command=save).pack(pady=20)


def start_quiz():
    if not slovar: return

    q_win = ctk.CTkToplevel(app)
    q_win.geometry("400x350")
    q_win.attributes("-topmost", True)

    state = {"w": "", "t": "", "streak": 0}

    def next_word():
        line = rnd.choice(slovar)
        state["w"], state["t"] = parse(line)
        label_q.configure(text=state["t"])
        ans_in.delete(0, 'end')
        label_score.configure(text=f"🔥 ВЕРНО ПОДРЯД: {state['streak']}")

    def check():
        if ans_in.get().strip().lower() == state["w"].lower():
            state["streak"] += 1
            update_days_streak()
            label_res.configure(text="ПРАВИЛЬНО!", text_color="green")
            q_win.after(1000, next_word)
        else:
            state["streak"] = 0
            label_res.configure(text=f"ОШИБКА! Это: {state['w']}", text_color="red")
            label_score.configure(text=f"🔥 ВЕРНО ПОДРЯД: {state['streak']}")

    label_q = ctk.CTkLabel(q_win, text="", font=("Arial", 18))
    label_q.pack(pady=20)

    ans_in = ctk.CTkEntry(q_win, width=200)
    ans_in.pack(pady=10)

    label_score = ctk.CTkLabel(q_win, text="🔥 ВЕРНО ПОДРЯД: 0", font=("Arial", 14, "bold"), text_color="orange")
    label_score.pack(pady=5)

    label_res = ctk.CTkLabel(q_win, text="")
    label_res.pack(pady=5)

    ctk.CTkButton(q_win, text="Проверить", command=check).pack(pady=10)
    next_word()


app = ctk.CTk()
app.title("Slovarly 2.0")
app.geometry("400x400")

d_streak, _ = get_days_streak()
ctk.CTkLabel(app, text=f"ДНЕЙ В ПРОГРАММЕ: {d_streak}", font=("Arial", 14), text_color="gray").pack(pady=10)
ctk.CTkLabel(app, text="SLOVARLY 2.0", font=("Arial", 28, "bold")).pack(pady=20)

ctk.CTkButton(app, text="Добавить слово", width=220, height=45, command=add_window).pack(pady=10)
ctk.CTkButton(app, text="Начать тест", width=220, height=45, command=start_quiz).pack(pady=10)
app.mainloop()