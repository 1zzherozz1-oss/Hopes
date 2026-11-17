"""Reflex Clicker: simple Tkinter game for Windows.

Click the moving button as many times as possible before the timer runs out.
"""

import random
import time
import tkinter as tk


class ReflexGame:
    """A tiny reflex-training game implemented with Tkinter."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Reflex Clicker")
        self.root.geometry("640x480")
        self.root.resizable(False, False)

        self.game_duration = 30
        self.end_time: float | None = None
        self.score = 0
        self.running = False
        self.move_job: str | None = None
        self.timer_job: str | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        header = tk.Frame(self.root, pady=10)
        header.pack(fill=tk.X)

        tk.Label(header, text="Reflex Clicker", font=("Segoe UI", 18, "bold")).pack()
        tk.Label(
            header,
            text="Klik target secepat mungkin selama 30 detik.",
            font=("Segoe UI", 11),
        ).pack()

        stats = tk.Frame(self.root, pady=5)
        stats.pack(fill=tk.X)

        self.score_label = tk.Label(stats, text="Skor: 0", font=("Segoe UI", 12, "bold"))
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.timer_label = tk.Label(stats, text="Waktu: 30", font=("Segoe UI", 12))
        self.timer_label.pack(side=tk.RIGHT, padx=10)

        controls = tk.Frame(self.root, pady=10)
        controls.pack(fill=tk.X)

        self.start_button = tk.Button(
            controls,
            text="Mulai",
            font=("Segoe UI", 11),
            command=self.start_game,
            width=10,
        )
        self.start_button.pack()

        self.arena = tk.Frame(self.root, bg="#f2f2f2", width=620, height=360)
        self.arena.pack(padx=10, pady=10)
        self.arena.pack_propagate(False)

        self.target = tk.Button(
            self.arena,
            text="Klik!",
            font=("Segoe UI", 10, "bold"),
            bg="#f7c948",
            activebackground="#f1b24a",
            width=8,
            height=2,
            command=self.on_target_click,
            state=tk.DISABLED,
        )
        self.target.place(x=280, y=150)

        self.status_label = tk.Label(
            self.root,
            text="Tekan 'Mulai' untuk bermain.",
            font=("Segoe UI", 10),
            pady=10,
        )
        self.status_label.pack()

    def start_game(self) -> None:
        if self.running:
            return

        self.score = 0
        self.update_score()
        self.end_time = time.time() + self.game_duration
        self.running = True
        self.status_label.config(text="Klik target secepat mungkin!")
        self.start_button.config(text="Sedang bermain...", state=tk.DISABLED)
        self.target.config(state=tk.NORMAL)

        self._schedule_move()
        self._update_timer()

    def _update_timer(self) -> None:
        if not self.running or self.end_time is None:
            return

        remaining = max(0, int(round(self.end_time - time.time())))
        self.timer_label.config(text=f"Waktu: {remaining}")

        if remaining <= 0:
            self.end_game()
            return

        self.timer_job = self.root.after(200, self._update_timer)

    def on_target_click(self) -> None:
        if not self.running:
            return

        self.score += 1
        self.update_score()
        self._schedule_move(immediate=True)

    def update_score(self) -> None:
        self.score_label.config(text=f"Skor: {self.score}")

    def _schedule_move(self, immediate: bool = False) -> None:
        if not self.running:
            return

        self._cancel_job(self.move_job)
        delay = 100 if immediate else 700
        self.move_job = self.root.after(delay, self._move_target)

    def _move_target(self) -> None:
        if not self.running:
            return

        self.root.update_idletasks()
        arena_width = self.arena.winfo_width()
        arena_height = self.arena.winfo_height()

        button_width = self.target.winfo_reqwidth()
        button_height = self.target.winfo_reqheight()

        max_x = max(10, arena_width - button_width - 10)
        max_y = max(10, arena_height - button_height - 10)

        new_x = random.randint(10, max_x)
        new_y = random.randint(10, max_y)
        self.target.place(x=new_x, y=new_y)

        self._schedule_move()

    def _cancel_job(self, job_id: str | None) -> None:
        if job_id is not None:
            self.root.after_cancel(job_id)

    def end_game(self) -> None:
        if not self.running:
            return

        self.running = False
        self._cancel_job(self.move_job)
        self._cancel_job(self.timer_job)

        self.start_button.config(text="Mulai", state=tk.NORMAL)
        self.target.config(state=tk.DISABLED)
        self.status_label.config(text=f"Waktu habis! Skor akhir: {self.score}")

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    ReflexGame().run()
