import functools
from tkVideoPlayer import TkinterVideo
import tkinter as tk
# Import tkinter library
import customtkinter
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
import os
import importlib


def play_next_video(event, videoplayer, playlist):
    next_video = next(playlist, None)
    print('Next is:', next_video)
    if not next_video:
        return

    # Play new video only after end of current
    videoplayer.load(next_video)
    videoplayer.play()

videos = []
def animate():
    from animation import array_module
    # this function will read the modified version of the pickle array
    importlib.reload(array_module)
    videos = array_module.my_array;
    module_dir = os.path.dirname(os.path.abspath(__file__))
    videos = [os.path.join(module_dir, video) for video in videos]
    root = tk.Toplevel()
    root.geometry('500x500+0+0')
    videoplayer = TkinterVideo(master=root, scaled=True, )

    # Use 'iter' to work with 'next' in callback
    playlist = iter(videos)

    # After end of video, use callback to run next video from playlist
    videoplayer.bind(
        "<<Ended>>",
        functools.partial(
            play_next_video,
            videoplayer=videoplayer,
            playlist=playlist,
        ),
    )

    # Play first video from playlist
    videoplayer.load(next(playlist))
    videoplayer.pack(expand=True, fill="both")
    videoplayer.play()
    root.mainloop()
