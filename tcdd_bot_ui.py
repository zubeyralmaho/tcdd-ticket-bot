import tkinter as tk
from tkinter import ttk, messagebox
from tcddbot import AppointmentBot
import threading
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TCDDBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TCDD Ticket Bot")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")
        
        # Style configuration
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#2196F3")
        style.configure("TLabel", padding=6, background="#f0f0f0")
        style.configure("TEntry", padding=6)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="TCDD Ticket Bot", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)
        
        # Journey Details Frame
        journey_frame = ttk.LabelFrame(main_frame, text="Journey Details", padding="10")
        journey_frame.pack(fill=tk.X, pady=10)
        
        # From
        ttk.Label(journey_frame, text="From:").pack(anchor=tk.W)
        self.from_entry = ttk.Entry(journey_frame)
        self.from_entry.pack(fill=tk.X, pady=5)
        self.from_entry.insert(0, os.getenv("DEFAULT_FROM", "Ankara"))
        
        # To
        ttk.Label(journey_frame, text="To:").pack(anchor=tk.W)
        self.to_entry = ttk.Entry(journey_frame)
        self.to_entry.pack(fill=tk.X, pady=5)
        self.to_entry.insert(0, os.getenv("DEFAULT_TO", "Kars"))
        
        # Email Configuration Frame
        email_frame = ttk.LabelFrame(main_frame, text="Email Configuration", padding="10")
        email_frame.pack(fill=tk.X, pady=10)
        
        # Sender Email
        ttk.Label(email_frame, text="Sender Email:").pack(anchor=tk.W)
        self.sender_email_entry = ttk.Entry(email_frame)
        self.sender_email_entry.pack(fill=tk.X, pady=5)
        self.sender_email_entry.insert(0, os.getenv("SENDER_EMAIL", ""))
        
        # Sender Password
        ttk.Label(email_frame, text="App Password:").pack(anchor=tk.W)
        self.sender_password_entry = ttk.Entry(email_frame, show="*")
        self.sender_password_entry.pack(fill=tk.X, pady=5)
        self.sender_password_entry.insert(0, os.getenv("SENDER_PASSWORD", ""))
        
        # Receiver Emails
        ttk.Label(email_frame, text="Receiver Emails (comma-separated):").pack(anchor=tk.W)
        self.receiver_emails_entry = ttk.Entry(email_frame)
        self.receiver_emails_entry.pack(fill=tk.X, pady=5)
        self.receiver_emails_entry.insert(0, os.getenv("RECEIVER_EMAILS", ""))
        
        # Status Frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_text = tk.Text(status_frame, height=10, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Control Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        self.start_button = ttk.Button(button_frame, text="Start Bot", command=self.start_bot)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop Bot", command=self.stop_bot, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.bot_thread = None
        self.is_running = False
        
    def update_status(self, message):
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        
    def start_bot(self):
        if not self.validate_inputs():
            return
            
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Get values from entries
        from_city = self.from_entry.get()
        to_city = self.to_entry.get()
        sender_email = self.sender_email_entry.get()
        sender_password = self.sender_password_entry.get()
        receiver_emails = [email.strip() for email in self.receiver_emails_entry.get().split(",")]
        
        # Create and start bot in a separate thread
        self.bot_thread = threading.Thread(target=self.run_bot, args=(
            from_city, to_city, sender_email, sender_password, receiver_emails
        ))
        self.bot_thread.start()
        
    def stop_bot(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.update_status("Bot stopped by user")
        
    def run_bot(self, from_city, to_city, sender_email, sender_password, receiver_emails):
        try:
            bot = AppointmentBot(
                kalkıs=from_city,
                varıs=to_city,
                sender_email=sender_email,
                sender_password=sender_password,
                receiver_emails=receiver_emails,
                message_subject="Boş Kuşetli Yatak Mevcut! ÇABUUKK!!!",
                message_body=f"https://bilet.tcdd.gov.tr/ adresinde {from_city}-{to_city} Doğu Ekspresi için"
            )
            
            self.update_status("Bot started successfully")
            bot.run()
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
        finally:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
    def validate_inputs(self):
        if not self.from_entry.get() or not self.to_entry.get():
            messagebox.showerror("Error", "Please enter both departure and arrival cities")
            return False
            
        if not self.sender_email_entry.get() or not self.sender_password_entry.get():
            messagebox.showerror("Error", "Please enter sender email and password")
            return False
            
        if not self.receiver_emails_entry.get():
            messagebox.showerror("Error", "Please enter at least one receiver email")
            return False
            
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = TCDDBotUI(root)
    root.mainloop() 