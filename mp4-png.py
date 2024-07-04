# Converts an MP4 file into a PNG sequence at full resolution using ffmpeg

import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import ffmpeg

class MP4toPNGApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MP4 to PNG Converter")
        self.geometry("600x500")
        self.configure(bg="#f0f0f0")  # Set background color
        self.create_widgets()
        self.layout_widgets()

    # Create all GUI widgets
    def create_widgets(self):
        
        self.input_label = tk.Label(self, text="Select MP4 File:", bg="#f0f0f0")
        self.input_entry = tk.Entry(self, width=50)
        self.input_button = tk.Button(self, text='Browse', bg="#4CAF50", fg="white", command=self.browse_input_file)

        self.output_label = tk.Label(self, text='Select Output Directory:', bg="#f0f0f0")
        self.output_entry = tk.Entry(self, width=50)
        self.output_button = tk.Button(self, text='Browse', bg="#4CAF50", fg="white", command=self.browse_output_dir)

        self.convert_button = tk.Button(self, text='Convert', bg="#008CBA", fg="white", command=self.convert_mp4)

        self.progress_log = scrolledtext.ScrolledText(self, width=70, height=15)
    
    # GUI widget layout using pack geometry manager
    def layout_widgets(self):
        
        widgets = [
            (self.input_label, 5), (self.input_entry, 5), (self.input_button, 5),
            (self.output_label, 5), (self.output_entry, 5), (self.output_button, 5),
            (self.convert_button, 20), (self.progress_log, 10)
        ]
        for widget, pady in widgets:
            widget.pack(pady=pady)
    
    # Open file dialog to select input MP4 file
    def browse_input_file(self):
        
        input_file = filedialog.askopenfilename(filetypes=[("MP4 Files", "*.mp4")])
        if input_file:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, input_file)

    # Open directory dialog to select output directory
    def browse_output_dir(self):
        
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_dir)
    
    # Convert MP4 to PNG sequence
    def convert_mp4(self):
        
        input_file = self.input_entry.get()
        output_dir = self.output_entry.get()

        if not input_file or not output_dir:
            messagebox.showerror("Error", "Please select an input file and output directory.")
            return

        # Clear progress log on start
        self.progress_log.delete(1.0, tk.END)
        
        self.progress_log.insert(tk.END, "Starting conversion...\n")
        self.progress_log.see(tk.END)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Run ffmpeg process to convert MP4 to PNG
        try:
            
            process = ffmpeg.input(input_file).output(os.path.join(output_dir, 'frame_%04d.png'), format='image2', vcodec='png')
            process = process.global_args('-progress', 'pipe:1')

            pipe = process.run_async(pipe_stderr=True)
            while pipe.poll() is None:
                line = pipe.stderr.readline().decode('utf8')
                if 'frame=' in line:
                    self.progress_log.insert(tk.END, line.strip() + '\n')
                    self.progress_log.see(tk.END)
                self.update_idletasks()

            pipe.wait()
            self.progress_log.insert(tk.END, "Conversion complete.\n")
        except Exception as e:
            self.progress_log.insert(tk.END, f"Error: {e}\n")

        self.progress_log.see(tk.END)

if __name__ == "__main__":
    app = MP4toPNGApp()
    app.mainloop()
