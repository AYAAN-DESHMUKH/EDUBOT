# edubot.py - EduBot: Personalized AI Tutor (No PDF, No Animation, Just Honest Offline Learning)
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import requests
import threading
import json
import time
import subprocess
import os

# Set appearance
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

class EduBot:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🎓 EduBot – Learn in Your World")
        self.window.geometry("900x700")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # State
        self.server_running = False
        self.interests = {}
        self.chat_history = []
        self.current_streaming_label = None
        self.current_streaming_content = ""
        self.message_widgets = []
        self.is_dark_mode = False

        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)

        # --- Header ---
        self.header = ctk.CTkLabel(
            self.window,
            text="🎓 EduBot",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1e88e5"
        )
        self.header.grid(row=0, column=0, padx=20, pady=20)

        # --- Top Bar: Dark Mode Toggle ---
        self.top_frame = ctk.CTkFrame(self.window, height=40)
        self.top_frame.grid(row=0, column=0, sticky="ne", padx=20, pady=20)
        self.top_frame.grid_propagate(False)

        self.dark_mode_btn = ctk.CTkButton(
            self.top_frame,
            text="🌙 Dark Mode",
            width=100,
            height=30,
            font=ctk.CTkFont(size=12),
            command=self.toggle_dark_mode
        )
        self.dark_mode_btn.pack()

        # --- Main Frame ---
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Start with homepage
        self.show_homepage()

    # === UI MODE TOGGLE ===
    def toggle_dark_mode(self):
        if self.is_dark_mode:
            ctk.set_appearance_mode("Light")
            self.dark_mode_btn.configure(text="🌙 Dark Mode")
            self.is_dark_mode = False
        else:
            ctk.set_appearance_mode("Dark")
            self.dark_mode_btn.configure(text="☀️ Light Mode")
            self.is_dark_mode = True

    # === SCREENS ===
    def show_homepage(self):
        self.clear_frame()

        welcome = ctk.CTkLabel(
            self.main_frame,
            text="Welcome to EduBot!\nA learning experience designed around your interests.",
            font=ctk.CTkFont(size=16),
            wraplength=600,
            justify="center"
        )
        welcome.pack(pady=40)

        # Server control
        self.server_status = ctk.CTkLabel(
            self.main_frame,
            text="🔴 Llama Server: Not Running",
            text_color="red",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.server_status.pack(pady=10)

        self.start_server_btn = ctk.CTkButton(
            self.main_frame,
            text="🔁 Start Llama Server",
            command=self.start_server,
            fg_color="#6d4c41"
        )
        self.start_server_btn.pack(pady=10)

        self.start_learning_btn = ctk.CTkButton(
            self.main_frame,
            text="🚀 Start Learning",
            command=self.show_interest_form,
            state="disabled",
            fg_color="#1b5e20"
        )
        self.start_learning_btn.pack(pady=20)

        # Test connection in background
        self.window.after(2000, self.check_server_status)

    def check_server_status(self):
        def test():
            try:
                r = requests.get("http://localhost:8080/v1/models", timeout=5)
                if r.status_code == 200:
                    self.server_running = True
                    self.window.after(0, self.update_server_ui)
            except:
                pass
        threading.Thread(target=test, daemon=True).start()

    def update_server_ui(self):
        if self.server_running:
            self.server_status.configure(text="🟢 Llama Server: Ready", text_color="green")
            self.start_server_btn.configure(state="disabled", text="✅ Server Running")
            self.start_learning_btn.configure(state="normal")

    def start_server(self):
        self.start_server_btn.configure(state="disabled", text="Starting...")
        self.server_status.configure(text="🟡 Starting server...", text_color="orange")

        def run():
            try:
                result = subprocess.run([
                    "docker", "run", "-d", "--name", "llamafile-server",
                    "--restart", "unless-stopped",
                    "-p", "8080:8080",
                    "-v", f"{os.getcwd()}/model:/usr/src/app/model",
                    "llamafile_image",
                    "--server", "--host", "0.0.0.0", "-m", "/usr/src/app/model/*.gguf"
                ], capture_output=True, text=True)
                if result.returncode == 0:
                    self.server_running = True
                    self.window.after(0, self.update_server_ui)
                    time.sleep(3)
                    self.window.after(1000, self.check_server_status)
                else:
                    raise Exception(result.stderr)
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror(
                    "Server Error",
                    f"Failed to start server. Make sure:\n"
                    "1. Docker is running\n"
                    "2. You built the image with build_file.sh\n"
                    "3. No other service uses port 8080\n\n"
                    f"Error: {str(e)}"
                ))
                self.window.after(0, lambda: self.start_server_btn.configure(state="normal", text="Retry"))

        threading.Thread(target=run, daemon=True).start()

    def show_interest_form(self):
        if not self.server_running:
            messagebox.showwarning("Wait", "Please wait for the server to start.")
            return

        self.clear_frame()
        self.main_frame.grid_rowconfigure((0,1,2,3,4,5), weight=0)

        ctk.CTkLabel(self.main_frame, text="Let's get to know you!", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        self.hero_var = ctk.StringVar()
        self.movie_var = ctk.StringVar()
        self.genre_var = ctk.StringVar()
        self.subject_var = ctk.StringVar()

        # Form fields
        ctk.CTkLabel(self.main_frame, text="🦸 Favorite Superhero?").pack(pady=5)
        ctk.CTkEntry(self.main_frame, textvariable=self.hero_var, width=300, placeholder_text="e.g. Iron Man").pack()

        ctk.CTkLabel(self.main_frame, text="🎬 Favorite Movie or Series?").pack(pady=5)
        ctk.CTkEntry(self.main_frame, textvariable=self.movie_var, width=300, placeholder_text="e.g. Avengers").pack()

        ctk.CTkLabel(self.main_frame, text="🎨 Favorite Genre?").pack(pady=5)
        ctk.CTkEntry(self.main_frame, textvariable=self.genre_var, width=300, placeholder_text="e.g. sci-fi, fantasy").pack()

        ctk.CTkLabel(self.main_frame, text="📚 Subject You Want to Learn?").pack(pady=5)
        ctk.CTkEntry(self.main_frame, textvariable=self.subject_var, width=300, placeholder_text="e.g. Physics, Math, History").pack()

        ctk.CTkButton(
            self.main_frame,
            text="💬 Start Learning",
            command=self.start_chat,
            fg_color="#1565c0"
        ).pack(pady=30)

    def start_chat(self):
        hero = self.hero_var.get().strip()
        movie = self.movie_var.get().strip()
        genre = self.genre_var.get().strip()
        subject = self.subject_var.get().strip()

        if not all([hero, movie, genre, subject]):
            messagebox.showwarning("Missing Info", "Please fill all fields.")
            return

        self.interests = {"hero": hero, "movie": movie, "genre": genre, "subject": subject}

        # Set system prompt
        self.chat_history = [
            {"role": "system", "content": f"""
            You are a friendly, encouraging tutor.
            The student loves {hero}, {movie}, and the {genre} genre.
            They want to learn {subject}.
            When explaining, use vivid analogies from their favorite world to make concepts relatable.
            Keep explanations accurate, engaging, and not too long.
            Start by welcoming them and asking what they'd like to learn first.
            """}
        ]

        self.show_chat_interface()

    def show_chat_interface(self):
        self.clear_frame()
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)

        # Chat frame
        self.chat_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.chat_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew", columnspan=2)
        self.message_widgets = []

        # Initial message
        intro = (
            f"Hi! I'm your personal tutor for {self.interests['subject']}.\n"
            f"Since you love {self.interests['movie']} and {self.interests['hero']}, "
            f"I'll explain things using those worlds to make them fun and easy.\n"
            f"What would you like to learn first?"
        )
        self.add_message("assistant", intro)

        # ⚠️ Offline Notice: Honest & Friendly
        offline_notice = (
            "💡 Heads up: I'm running offline on your device — not a cloud wizard, just a smart local model!\n"
            "So I might take a few seconds to think. But I promise, my answers are worth the wait. 😊"
        )
        self.add_message("assistant", offline_notice)

        # Input
        self.entry = ctk.CTkEntry(self.main_frame, placeholder_text="Ask anything...")
        self.entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = ctk.CTkButton(self.main_frame, text="Send", width=80, command=self.send_message)
        self.send_btn.grid(row=1, column=1, padx=10, pady=10)

        self.entry.focus()

    def add_message(self, role, content):
        align = "w" if role == "assistant" else "e"
        bg_color = "#2d4059" if role == "assistant" and self.is_dark_mode else "#f0f4f8"
        user_color = "#118ab2" if self.is_dark_mode else "#c8e6c9"
        fg_color = "#ffffff" if role == "assistant" and self.is_dark_mode else "#000000"

        color = bg_color if role == "assistant" else user_color

        label = ctk.CTkLabel(
            self.chat_frame,
            text=f"{'You' if role == 'user' else 'EduBot'}: {content}",
            fg_color=color,
            text_color=fg_color,
            corner_radius=15,
            padx=12,
            pady=8,
            justify="left",
            wraplength=650,
            font=ctk.CTkFont(size=13)
        )
        label.pack(anchor=align, pady=4, padx=10)
        self.message_widgets.append(label)
        self.chat_frame._parent_canvas.yview_moveto(1.0)

        if role == "assistant":
            self.current_streaming_label = label
            self.current_streaming_content = content

    def send_message(self):
        query = self.entry.get().strip()
        if not query:
            return

        self.entry.delete(0, "end")
        self.add_message("user", query)
        self.chat_history.append({"role": "user", "content": query})

        # Disable input
        self.entry.configure(state="disabled")
        self.send_btn.configure(state="disabled")

        threading.Thread(target=self.get_response, daemon=True).start()

    def get_response(self):
        try:
            payload = {
                "model": "llamafile",
                "messages": self.chat_history,
                "stream": True,
                "temperature": 0.7
            }
            response = requests.post(
                "http://localhost:8080/v1/chat/completions",
                json=payload,
                stream=True,
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(f"Server error: {response.status_code}")

            self.window.after(0, lambda: self.add_message("assistant", ""))
            ttft = None
            start = time.time()

            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    decoded = line.decode("utf-8").strip()
                    if decoded.startswith("data: "):
                        data_str = decoded[6:].strip()
                        if data_str == "[DONE]":
                            break
                        data = json.loads(data_str)
                        delta = data["choices"][0]["delta"].get("content", "")
                        if delta:
                            if ttft is None:
                                ttft = time.time() - start
                                print(f"⏱️ TTFT: {ttft:.2f}s")
                            self.window.after(0, lambda d=delta: self.update_stream(d))
                except:
                    continue

            self.window.after(0, self.finalize_stream)
        except Exception as e:
            self.window.after(0, lambda: self.add_message("assistant", f"❌ {str(e)}"))
            self.window.after(0, self.finalize_stream)

    def update_stream(self, delta):
        self.current_streaming_content += delta
        if self.current_streaming_label:
            self.current_streaming_label.configure(text=f"EduBot: {self.current_streaming_content}")
            self.chat_frame._parent_canvas.yview_moveto(1.0)

    def finalize_stream(self):
        self.chat_history.append({"role": "assistant", "content": self.current_streaming_content})
        self.current_streaming_label = None
        self.current_streaming_content = ""
        self.entry.configure(state="normal")
        self.send_btn.configure(state="normal")
        self.entry.focus()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Close EduBot?"):
            try:
                subprocess.run(["docker", "stop", "llamafile-server"], capture_output=True)
                subprocess.run(["docker", "rm", "llamafile-server"], capture_output=True)
            except:
                pass
            self.window.destroy()


if __name__ == "__main__":
    app = EduBot()
    app.window.mainloop()