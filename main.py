import tkinter as tk # tkinter imports
import vlc # plays audio
import requests # necessary to get the metadata of radio stations
from time import sleep

class StreamingPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Bootleg Radio Station")
        self.root.geometry("600x300")

        # vlc player variables
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # split gui into 2 so that there can be a recently played and radio control section
        self.root.columnconfigure(0, weight=1)  # Left Side (Future Features)
        self.root.columnconfigure(1, weight=1)  # Right Side (Active GUI)
        self.root.rowconfigure(0, weight=1)

        # create left frame
        self.left_frame = tk.Frame(root, bg="lightgray", width=300, height=300)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        # recently played box label
        self.recently_label = tk.Label(self.left_frame, text="Recently Played Songs")
        self.recently_label.pack(anchor="w", pady=5)

        # recently played box
        self.recently_box = tk.Listbox(self.left_frame)
        self.recently_box.bind("<ButtonRelease-1>", self.on_select)
        self.recently_box.pack(fill="both", expand=True, padx=5, pady=5)
        
        # create right frame of gui
        self.right_frame = tk.Frame(root, width=300, height=300)
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.right_frame.columnconfigure(0, weight=1)

        # input for url of radio station to stream
        self.url_label = tk.Label(self.right_frame, text="Enter Stream URL:")
        self.url_label.pack(anchor="w", pady=5)

        self.url_entry = tk.Entry(self.right_frame, width=40)
        self.url_entry.pack(pady=5)

        # frame and functionality for play/stop buttons
        button_frame = tk.Frame(self.right_frame)
        button_frame.pack(pady=5)

        self.play_button = tk.Button(button_frame, text="Play", command=self.play_audio)
        self.play_button.pack(side="left", padx=5)

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_audio, state=tk.DISABLED)
        self.stop_button.pack(side="left", padx=5)

        # volume slider label
        self.volume_label = tk.Label(self.right_frame, text="Volume:")
        self.volume_label.pack(anchor="w", pady=5)

        # volume slider so user can change volume of audio
        self.volume_slider = tk.Scale(self.right_frame, from_=0, to=500, orient="horizontal")
        self.volume_slider.set(100)  #  default at 100% volume
        self.volume_slider.pack(fill="x", padx=5)

        # only update volume when slider is released to eliminate issues with lagg 
        self.volume_slider.bind("<ButtonRelease-1>", lambda event: self.set_volume(self.volume_slider.get()))  

        self.meta_label = tk.Label(self.right_frame, text="", justify="left", wraplength=250)
        self.meta_label.pack(pady=5)

    def play_audio(self): # plays audio from url specified
        url = self.url_entry.get().strip()
        if not url: # error validation if there is no url
            tk.messagebox.showerror("Error", "Please enter a valid URL!")
            return

        all_items = self.recently_box.get(0, tk.END)

        if url not in all_items: # add url to recently played IF not already there
            self.recently_box.insert(0, url)

        # play audio through vlc
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()

        self.set_volume(self.volume_slider.get())

        # update metadata for the new radio station playing
        self.fetch_metadata(url)

        self.play_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def stop_audio(self): # stop the currently playing radio station
        self.player.stop()
        self.play_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def set_volume(self, volume): # set volume based on slider value
        self.player.audio_set_volume(volume)

    def on_select(self, e): # function to be called on selection of an item from the recently played box
        selection = self.recently_box.curselection() # get value thats actually selected
        if selection:
            selection = self.recently_box.get(selection[0])
            self.stop_audio()
            # update url entry
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, selection)

    def fetch_metadata(self, url): # fetch and update metadata of current radio station
        headers = {"Icy-MetaData": "1"}
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=5)
            if response.status_code == 200:
                icy_headers = response.headers
                metadata = {
                    "Name": icy_headers.get("icy-name", "N/A" ),
                    "Description": icy_headers.get("icy-description", "N/A"),
                    "Genre": icy_headers.get("icy-genre", "N/A"),
                    "URL": icy_headers.get("icy-url", "N/A"),
                }
                meta_text = "\n".join([f"{key}: {value}" for key, value in metadata.items()])
                self.meta_label.config(text=meta_text)
            else:
                self.meta_label.config(text="Failed to fetch metadata.")
        except requests.exceptions.RequestException as e:
            self.meta_label.config(text=f"Error: {e}")

root = tk.Tk()
app = StreamingPlayer(root)
root.mainloop()
