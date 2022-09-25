import tkinter as tk
import customtkinter as ctk 

from PIL import ImageTk
#from authtoken import auth_token
import auth_token

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline 

# Create the app
app = tk.Tk()
app.geometry("532x632")
app.title("Goriber Midjourney AI") 
ctk.set_appearance_mode("dark") 



app.mainloop()