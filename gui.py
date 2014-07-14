#!/usr/bin/env python
import Tkinter
import tkFileDialog

import PIL.Image
import PIL.ImageTk
import numpy as np

import poissonblending
from image_managers import SourceImageManager


class PoissonBlendingApp(Tkinter.Tk):
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.src_img_manager = SourceImageManager()

        self.parent = parent
        self.entry = None
        self.label_text = None
        self.entry_text = None

        self.image_dst = None
        self.image_result = None

        self.initialize()

    def initialize(self):
        self.create_menu()
        self.create_widgets()

        self.src_img_manager.set_path('./testimages/test1_src.png')
        self.src_img_manager.load()

        self.dst_path = './testimages/test1_target.png'
        # self.load_src()
        self.load_dst()

    def create_widgets(self):
        self.grid()

        # Source and Destination images
        self.label_dst = Tkinter.Label(self)
        self.label_dst.grid(row=0, column=0)

        Tkinter.Label(self, text="+").grid(row=0, column=1)

        label_src = Tkinter.Label(self)
        label_src.grid(row=0, column=2)
        self.src_img_manager.set_tk_label(label_src)

        # Draw/Erase/Move buttons
        self.edit_options_frame = Tkinter.Frame(self)
        self.edit_options_frame.grid(row=1, column=2)
        edit_mode = Tkinter.StringVar()
        edit_mode.set('draw')
        edit_options = (
            ('Draw', 'draw'),
            ('Erase', 'erase'),
            ('Move', 'move'),
        )
        for text, mode in edit_options:
            b = Tkinter.Radiobutton(self.edit_options_frame, text=text,
                                    variable=edit_mode, value=mode,
                                    indicatoron=0)
            b.pack(side=Tkinter.LEFT)
        self.src_img_manager.set_edit_mode_str(edit_mode)

        # Blend button
        Tkinter \
            .Button(self, text=u'Blend', command=self.blend) \
            .grid(row=2, column=0, columnspan=3)

    def create_menu(self):
        menu_bar = Tkinter.Menu(self)

        file_menu = Tkinter.Menu(menu_bar)
        file_menu.add_command(label='Open Source Image',
                              command=self.src_img_manager.open)
        file_menu.add_command(label='Open Destination Image',
                              command=self.open_dst_file)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.config(menu=menu_bar)

    def load_dst(self):
        self.image_dst = PIL.Image.open(self.dst_path).convert("RGB")
        self.image_tk_dst = PIL.ImageTk.PhotoImage(self.image_dst)
        self.label_dst.configure(image=self.image_tk_dst)

    def blend(self):
        src = np.asarray(self.src_img_manager.image_src)
        src.flags.writeable = True
        dst = np.asarray(self.image_dst)
        dst.flags.writeable = True
        mask = np.asarray(self.src_img_manager.image_mask)
        mask.flags.writeable = True

        blended_image = poissonblending.blend(dst, src, mask, offset=(40, -30))
        self.image_result = PIL.Image.fromarray(np.uint8(blended_image))
        self.image_tk_result = PIL.ImageTk.PhotoImage(self.image_result)

        result_window = Tkinter.Toplevel()
        label = Tkinter.Label(result_window, image=self.image_tk_result)
        label.pack()
        result_window.title("Blended Result")

    def open_dst_file(self):
        self.dst_path = tkFileDialog.askopenfilename()
        self.load_dst()


if __name__ == "__main__":
    app = PoissonBlendingApp(None)
    app.title('Poisson Blending')
    app.mainloop()
