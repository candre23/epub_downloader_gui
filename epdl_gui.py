import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import subprocess
import threading
import os
import shutil # Imported for moving the file

class DownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("Ebook Downloader GUI")
        master.geometry("700x500")

        # --- GUI Widgets ---
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat")

        main_frame = ttk.Frame(master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        url_label = ttk.Label(main_frame, text="Book URL:")
        url_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ttk.Entry(main_frame, width=60)
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        dir_label = ttk.Label(main_frame, text="Destination:")
        dir_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.dir_entry = ttk.Entry(main_frame)
        self.dir_entry.grid(row=1, column=1, padx=(5,0), pady=5, sticky="ew")
        self.browse_button = ttk.Button(main_frame, text="Browse...", command=self.browse_directory)
        self.browse_button.grid(row=1, column=2, padx=(5,0), pady=5)

        self.download_button = ttk.Button(main_frame, text="Download", command=self.start_download_thread)
        self.download_button.grid(row=2, column=1, pady=15, sticky="w")

        log_label = ttk.Label(main_frame, text="Log:")
        log_label.grid(row=3, column=0, sticky="w", padx=5)
        self.log_window = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=15, state='disabled')
        self.log_window.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def log(self, message):
        self.log_window.configure(state='normal')
        self.log_window.insert(tk.END, message)
        self.log_window.see(tk.END)
        self.log_window.configure(state='disabled')

    def start_download_thread(self):
        url = self.url_entry.get()
        directory = self.dir_entry.get()

        if not url or not directory:
            self.log("Error: URL and destination directory are required.\n")
            return
        
        self.download_button.config(state=tk.DISABLED)
        self.log_window.configure(state='normal')
        self.log_window.delete('1.0', tk.END)
        self.log_window.configure(state='disabled')

        thread = threading.Thread(target=self.run_downloader_process, args=(url, directory))
        thread.start()

    def run_downloader_process(self, url, directory):
        script_path = os.path.join(os.path.dirname(__file__), "epub_downloader.py")
        epub_filename = None

        try:
            command = ["python", "-u", script_path, url]
            
            startupinfo = None
            if os.name == 'nt':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                startupinfo=startupinfo,
                cwd=os.path.dirname(script_path) # Run script in its own directory
            )

            for line in iter(process.stdout.readline, ''):
                self.master.after(0, self.log, line)
                if "epub file created:" in line.lower():
                    try:
                        filename = line.split(':', 1)[1].strip()
                        epub_filename = os.path.basename(filename)
                    except IndexError:
                        self.log("Could not parse filename from output.\n")
            
            process.stdout.close()
            return_code = process.wait()

            if return_code == 0 and epub_filename:
                source_path = os.path.join(os.path.dirname(script_path), "downloaded_epubs", epub_filename)
                
                if os.path.exists(source_path):
                    self.master.after(0, self.log, f"\nDownload complete. Moving file...\n")
                    shutil.move(source_path, directory)
                    final_dest_path = os.path.join(directory, epub_filename)
                    self.master.after(0, self.log, f"Successfully moved ebook to: {final_dest_path}\n")
                else:
                    self.master.after(0, self.log, f"Error: Could not find downloaded file at '{source_path}' to move.\n")

            elif return_code != 0:
                self.master.after(0, self.log, f"\n--- Subprocess failed with return code {return_code} ---\n")

        except FileNotFoundError:
            self.master.after(0, self.log, f"Error: The script '{script_path}' was not found.\n")
        except Exception as e:
            self.master.after(0, self.log, f"An unexpected error occurred: {e}\n")
        finally:
            self.master.after(0, lambda: self.download_button.config(state=tk.NORMAL))

if __name__ == '__main__':
    root = tk.Tk()
    app = DownloaderGUI(root)
    root.mainloop()
