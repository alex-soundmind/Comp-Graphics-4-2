import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Лабораторная работа №4")
        self.pack()
        self.create_widgets()
        self.transformations = []

    def create_widgets(self):
        button_width = 30 

        self.open_button = tk.Button(self, width=button_width)
        self.open_button["text"] = "Открыть изображение"
        self.open_button["command"] = self.open_image
        self.open_button.pack(side="top")

        self.affine_button = tk.Button(self, width=button_width)
        self.affine_button["text"] = "Афинные преобразования"
        self.affine_button["command"] = self.affine_transform
        self.affine_button.pack(side="top")

        self.nonlinear_button = tk.Button(self, width=button_width)
        self.nonlinear_button["text"] = "Нелинейные преобразования"
        self.nonlinear_button["command"] = self.nonlinear_transform
        self.nonlinear_button.pack(side="top")

        self.save_button = tk.Button(self, width=button_width)
        self.save_button["text"] = "Сохранить результат"
        self.save_button["command"] = self.save_result
        self.save_button.pack(side="top")

        self.restore_button = tk.Button(self, width=button_width)
        self.restore_button["text"] = "Восстановить исходное изображение"
        self.restore_button["command"] = self.restore_original
        self.restore_button.pack(side="top")

        self.image_label = tk.Label(self)
        self.image_label.pack(side="bottom")

        self.original_image = None
        self.transformed_image = None

    def open_image(self):
        path = filedialog.askopenfilename()
        self.original_image = Image.open(path)
        self.transformed_image = self.original_image.copy()
        self.image = ImageTk.PhotoImage(self.transformed_image)
        self.image_label.config(image=self.image)
        self.transformations = []
    
    def affine_transform(self):
        if self.transformed_image:
            self.transformed_image = self.transformed_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.transformed_image = self.transformed_image.resize((self.transformed_image.width*2, self.transformed_image.height))
            self.image = ImageTk.PhotoImage(self.transformed_image)
            self.image_label.config(image=self.image)
            self.transformations.append(("affine", self.transformed_image.size))
    
    def nonlinear_transform(self):
        if self.transformed_image:
            array = np.array(self.transformed_image)
            width, height = array.shape[1], array.shape[0]
            transformed_array = np.zeros_like(array)
            coordinates = [] 
            for i in range(height):
                for j in range(width):
                    if i == 0:
                        x_prime = 0
                    else:
                        x_prime = np.log(i)
                    y_prime = j
                    i_prime = int(np.exp(x_prime))
                    j_prime = int(y_prime)
                    if 0 <= i_prime < height and 0 <= j_prime < width:
                        transformed_array[i, j] = array[i_prime, j_prime]
                        coordinates.append((i_prime, j_prime)) 
            self.transformed_image = Image.fromarray(transformed_array)
            self.image = ImageTk.PhotoImage(self.transformed_image)
            self.image_label.config(image=self.image)
            self.transformations.append(("nonlinear", coordinates))

    def save_result(self):
        if self.transformed_image:
            filename, file_extension = os.path.splitext(self.original_image.filename)
            output_filename = f"{filename}_output.jpg"
            self.transformed_image.save(output_filename)

    def restore_original(self):
        if self.transformations:
            for transformation in reversed(self.transformations):
                if transformation[0] == "affine":
                    width, height = transformation[1]
                    self.transformed_image = self.transformed_image.resize((width//2, height))
                    self.transformed_image = self.transformed_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.image = ImageTk.PhotoImage(self.transformed_image)
            self.image_label.config(image=self.image)
            self.transformations = []

root = tk.Tk()
app = Application(master=root)
app.mainloop()
