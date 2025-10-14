import tkinter as tk
from tkinter import scrolledtext, filedialog, font, ttk, messagebox
from PIL import Image, ImageTk
import json
import os
import subprocess
import sys

## Made by gio83dj (GL) vith Heart!

# --- Language Configuration ---
LANG = "en"  # Change to "it" for Italian

TRANSLATIONS = {
    "en": {
        "title": "ComfyUI MetaImageViewer",
        "select_folder": "Select Folder",
        "select_main_folder": "Select main folder",
        "explore": "Explore",
        "delete": "Delete",
        "confirm": "Confirm",
        "delete_confirm": "Do you want to delete {}?",
        "checkpoint": "Checkpoint",
        "prompt": "Prompt",
        "seed": "Seed",
        "lora": "Lora"
    },
    "it": {
        "title": "ComfyUI MetaImageViewer",
        "select_folder": "Seleziona Cartella",
        "select_main_folder": "Seleziona cartella principale",
        "explore": "Esplora",
        "delete": "Cancella",
        "confirm": "Conferma",
        "delete_confirm": "Vuoi eliminare {}?",
        "checkpoint": "Checkpoint",
        "prompt": "Prompt",
        "seed": "Seed",
        "lora": "Lora"
    }
}

def t(key):
    """Get translation for current language"""
    return TRANSLATIONS[LANG].get(key, key)

# --- Global Variables ---
immagini_files = []
cartella_corrente = ""
idx = 0
img_originale = None
img_tk = None
MIN_RIGHE_TEXT = 10
MAX_RIGHE_TEXT = 30
text_height_lines = MIN_RIGHE_TEXT
drag_start_y = 0
text_start_height_lines = MIN_RIGHE_TEXT

# Thumbnails
thumbnail_size = 100
thumb_imgs = []
thumb_items = []

# --- Functions ---
def elimina_spazi(testo):
    return " ".join(testo.replace("\n", " ").split())

def scegli_cartella():
    global cartella_corrente
    cartella_corrente = filedialog.askdirectory(title=t("select_main_folder"))
    if not cartella_corrente:
        return
    carica_cartelle(cartella_corrente)

def apri_file_argomento():
    """Opens file passed as command line argument"""
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.isfile(file_path) and file_path.lower().endswith((".png", ".jpg", ".jpeg")):
            global cartella_corrente
            cartella_corrente = os.path.dirname(os.path.abspath(file_path))
            carica_cartelle(cartella_corrente)
            # Find the file index
            file_name = os.path.basename(file_path)
            if file_name in immagini_files:
                global idx
                idx = immagini_files.index(file_name)
                mostra_immagine(idx)
            return True
    return False

def carica_cartelle(path):
    global immagini_files, idx
    sottocartelle = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    combobox_values = ["root"] + sottocartelle
    sottocartella_menu['values'] = combobox_values
    sottocartella_menu.current(0)
    cambia_sottocartella(None)

def cambia_sottocartella(event):
    global cartella_corrente, immagini_files, idx
    scelta = sottocartella_var.get()
    if scelta == "root":
        percorso = cartella_corrente
    else:
        percorso = os.path.join(cartella_corrente, scelta)
    immagini_files = [f for f in os.listdir(percorso) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    idx = 0
    if immagini_files:
        mostra_immagine(idx)
    aggiorna_barra_thumb()

def estrai_info(image_path):
    img = Image.open(image_path)
    prompt = img.info.get("prompt", "{}")
    try:
        messaggioJson = json.loads(prompt)
    except:
        messaggioJson = {}

    contenuti_text = []
    contenuti_checkpoint = []
    contenuti_seed = []
    contenuti_lora = []

    for chiave, valore in messaggioJson.items():
        if isinstance(valore, dict) and "inputs" in valore:
            inputs = valore["inputs"]
            if "ckpt_name" in inputs:
                contenuti_checkpoint.append(inputs["ckpt_name"])
            if "text" in inputs:
                t_text = inputs["text"]
                if isinstance(t_text, list):
                    t_text = " ".join(str(x) for x in t_text)
                elif isinstance(t_text, (int, float)):
                    t_text = str(t_text)
                contenuti_text.append(elimina_spazi(t_text))
            if "noise_seed" in inputs:
                contenuti_seed.append(inputs["noise_seed"])
            if "seed" in inputs:
                contenuti_seed.append(inputs["seed"])
            if "lora_name" in inputs:
                contenuti_lora.append(inputs["lora_name"])

    testo_output = ""
    for i, c in enumerate(contenuti_checkpoint):
        testo_output += f"{t('checkpoint')} {i}: {c}\n"
    for i, txt in enumerate(contenuti_text):
        testo_output += f"{t('prompt')} {i}: {txt}\n"
    for i, s in enumerate(contenuti_seed):
        testo_output += f"{t('seed')} {i}: {s}\n"
    for i, l in enumerate(contenuti_lora):
        testo_output += f"{t('lora')} {i}: {l}\n"
    return testo_output

def aggiorna_textbox(text):
    text_box.config(state="normal")
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, text)
    text_box.config(state="disabled")

def ridimensiona_immagine():
    global img_tk, img_originale
    if img_originale is None:
        return
    root.update_idletasks()
    tk_font = font.Font(font=text_box['font'])
    text_height_px = tk_font.metrics("linespace") * text_height_lines + 4

    max_width = root.winfo_width() - 20
    max_height = root.winfo_height() - text_height_px - thumb_canvas.winfo_height() - 50

    img_resized = img_originale.copy()
    img_resized.thumbnail((max_width, max_height))
    img_tk = ImageTk.PhotoImage(img_resized)
    label_img.config(image=img_tk)
    label_img.image = img_tk

def mostra_immagine(i):
    global img_originale
    if not immagini_files:
        return
    scelta = sottocartella_var.get()
    if scelta == "root":
        path_base = cartella_corrente
    else:
        path_base = os.path.join(cartella_corrente, scelta)
    path = os.path.join(path_base, immagini_files[i])
    img_originale = Image.open(path)

    width, height = img_originale.size
    root.title(f"{t('title')} - {path} ({width}x{height})")

    testo = estrai_info(path)
    aggiorna_textbox(testo)
    ridimensiona_immagine()
    evidenzia_thumb(i)

def avanti(event=None):
    global idx
    if immagini_files:
        idx = (idx + 1) % len(immagini_files)
        mostra_immagine(idx)

def indietro(event=None):
    global idx
    if immagini_files:
        idx = (idx - 1) % len(immagini_files)
        mostra_immagine(idx)

# --- Drag TextBox top border ---
def start_drag(event):
    global drag_start_y, text_start_height_lines
    drag_start_y = event.y_root
    text_start_height_lines = text_height_lines

def drag_motion(event):
    global text_height_lines
    tk_font = font.Font(font=text_box['font'])
    line_height = tk_font.metrics("linespace")

    delta_y = drag_start_y - event.y_root
    new_height_lines = text_start_height_lines + round(delta_y / line_height)
    text_height_lines = max(MIN_RIGHE_TEXT, min(MAX_RIGHE_TEXT, new_height_lines))
    text_box.config(height=text_height_lines)
    ridimensiona_immagine()

# --- Context menu ---
def apri_cartella():
    if not immagini_files:
        return
    scelta = sottocartella_var.get()
    if scelta == "root":
        path_base = cartella_corrente
    else:
        path_base = os.path.join(cartella_corrente, scelta)
    path = os.path.join(path_base, immagini_files[idx])
    folder = os.path.dirname(os.path.abspath(path))
    os.startfile(folder)

def cancella_immagine():
    global idx
    if not immagini_files:
        return
    scelta = sottocartella_var.get()
    if scelta == "root":
        path_base = cartella_corrente
    else:
        path_base = os.path.join(cartella_corrente, scelta)
    path = os.path.join(path_base, immagini_files[idx])
    conferma = messagebox.askyesno(t("confirm"), t("delete_confirm").format(path))
    if conferma:
        os.remove(path)
        immagini_files.pop(idx)
        if idx >= len(immagini_files):
            idx = len(immagini_files) - 1
        if immagini_files:
            mostra_immagine(idx)
            aggiorna_barra_thumb()
        else:
            label_img.config(image='')
            text_box.config(state="normal")
            text_box.delete("1.0", tk.END)
            text_box.config(state="disabled")

def menu_contenuto(event):
    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label=t("explore"), command=apri_cartella)
    menu.add_command(label=t("delete"), command=cancella_immagine)
    menu.tk_popup(event.x_root, event.y_root)

def scroll_avanti_indietro(event):
    global idx
    if not immagini_files:
        return
    if event.delta > 0:
        idx = (idx - 1) % len(immagini_files)
    else:
        idx = (idx + 1) % len(immagini_files)
    mostra_immagine(idx)

# --- Thumbnails ---
def genera_thumbnails():
    global thumb_imgs
    thumb_imgs.clear()
    if not immagini_files:
        return
    # Determine correct path based on subfolder
    scelta = sottocartella_var.get()
    if scelta == "root":
        path_base = cartella_corrente
    else:
        path_base = os.path.join(cartella_corrente, scelta)
    
    thumb_folder = os.path.join(path_base, ".thumbnails")
    os.makedirs(thumb_folder, exist_ok=True)
    for f in immagini_files:
        path = os.path.join(path_base, f)
        thumb_path = os.path.join(thumb_folder, f)
        if not os.path.exists(thumb_path):
            try:
                img = Image.open(path)
                img.thumbnail((thumbnail_size, thumbnail_size))
                img.save(thumb_path)
            except:
                continue
        img = Image.open(thumb_path)
        thumb_imgs.append(ImageTk.PhotoImage(img))

# thumbnail: save tuple (rect_id, img_id)
thumb_items = []

def aggiorna_barra_thumb():
    thumb_canvas.delete("all")
    genera_thumbnails()
    x = 5
    thumb_items.clear()
    for i, img in enumerate(thumb_imgs):
        rect = thumb_canvas.create_rectangle(x-3, 0, x+thumbnail_size+3, thumbnail_size+10, outline="black", width=2)
        img_id = thumb_canvas.create_image(x, 5, anchor="nw", image=img)
        thumb_items.append((rect, img_id))
        x += thumbnail_size + 10
    thumb_canvas.config(scrollregion=(0, 0, x, thumbnail_size+10))
    evidenzia_thumb(idx)

def evidenzia_thumb(index):
    for i, (rect, _) in enumerate(thumb_items):
        if i == index:
            thumb_canvas.itemconfig(rect, outline="lime")
            thumb_canvas.xview_moveto(max(0, (i*(thumbnail_size+10)-100)/thumb_canvas.bbox("all")[2]))
        else:
            thumb_canvas.itemconfig(rect, outline="black")

def click_thumb(event):
    x = thumb_canvas.canvasx(event.x)
    i = int(x // (thumbnail_size + 10))
    if 0 <= i < len(immagini_files):
        global idx
        idx = i
        mostra_immagine(idx)
        evidenzia_thumb(idx)


def scroll_thumbs(event):
    thumb_canvas.xview_scroll(-1*(event.delta//120), "units")

# Funzione per ottenere il percorso corretto anche nel .exe
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):  # Quando è impacchettato nel .exe
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(relative_path)
# --- Main GUI ---

    
root = tk.Tk()
root.title(t("title"))
root.configure(bg="black")
root.geometry("1000x800")
# Carica icona compatibile con PyInstaller
try:
    icon_path = resource_path("icone/ComfyUIMetaImageViewer.ico")
    root.iconbitmap(icon_path)
except Exception as e:
    print("Icona non trovata:", e)
    
try:
    root.iconbitmap(os.path.join("icone", "ComfyUIMetaImageViewer.ico"))
except:
    pass  # Evita errore su Linux/Mac o se non trova l'icona

# Top frame: button + combobox
top_frame = tk.Frame(root, bg="black")
top_frame.pack(side="top", fill="x")
btn_cartella = tk.Button(top_frame, text=t("select_folder"), command=scegli_cartella, bg="black", fg="lime")
btn_cartella.pack(side="left", padx=5, pady=5)
sottocartella_var = tk.StringVar()
sottocartella_menu = ttk.Combobox(top_frame, textvariable=sottocartella_var, state="readonly")
sottocartella_menu.pack(side="left", padx=5)
sottocartella_menu.bind("<<ComboboxSelected>>", cambia_sottocartella)

# Canvas for thumbnails (fixed height)
thumb_frame = tk.Frame(root, height=thumbnail_size+10)
thumb_frame.pack(side="top", fill="x")
thumb_canvas = tk.Canvas(thumb_frame, height=thumbnail_size+10, bg="black")
thumb_scroll = tk.Scrollbar(thumb_frame, orient="horizontal", command=thumb_canvas.xview)
thumb_canvas.config(xscrollcommand=thumb_scroll.set)
thumb_canvas.pack(side="top", fill="x")
thumb_scroll.pack(side="bottom", fill="x")
thumb_canvas.bind("<Button-1>", click_thumb)
thumb_canvas.bind("<MouseWheel>", scroll_thumbs)

# Main frame containing image and TextBox
main_frame = tk.Frame(root, bg="black")
main_frame.pack(fill="both", expand=True)

# Image label
label_img = tk.Label(main_frame, bg="black")
label_img.pack(fill="both", expand=True)
label_img.bind("<Button-3>", menu_contenuto)

# TextBox frame at bottom
textbox_frame = tk.Frame(main_frame)
textbox_frame.pack(fill="x", side="bottom")
separator = tk.Frame(textbox_frame, height=5, bg="lime", cursor="sb_v_double_arrow")
separator.pack(fill="x", side="top")
separator.bind("<Button-1>", start_drag)
separator.bind("<B1-Motion>", drag_motion)
text_box = scrolledtext.ScrolledText(textbox_frame, width=80, height=MIN_RIGHE_TEXT, state="disabled", bg="black", fg="lime")
text_box.pack(fill="x", side="top")

# Bind arrows
root.bind("<Left>", indietro)
root.bind("<Right>", avanti)
root.bind("<Configure>", lambda e: ridimensiona_immagine())
root.bind("<MouseWheel>", scroll_avanti_indietro)

# Check if opened with a file argument
if not apri_file_argomento():
    # If no file argument, show file selection prompt
    pass

root.mainloop()