# 🖼️ ComfyUI MetaImageViewer

https://youtu.be/xgDcXMIAMy8?si=5PFMGef_m37Iez9l

A fast and intuitive image viewer to explore image collections with embedded JSON metadata, specifically designed to visualize AI generation prompts and parameters (ComfyUI, Stable Diffusion, etc.).

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## ✨ Features

- **Fast navigation**: Browse images with arrow keys or mouse wheel
- **Thumbnail strip**: Visual preview of all images in the current folder
- **JSON metadata extraction**: Automatically displays prompts, checkpoints, seeds, and LoRAs from PNG metadata
- **Subfolder management**: Easily switch between main folder and subfolders
- **Resizable text area**: Adjust metadata area height via drag and drop
- **Context menu**: Open folder in file explorer or delete images directly
- **Dark mode interface**: Black/lime green design to reduce eye strain
- **Smart cache**: Thumbnails are generated once and saved in `.thumbnails` folder

## 📋 Requirements

```
Python 3.7+
tkinter (included with Python)
Pillow (PIL)
```

## 🚀 Installation
Portable binaries "EXE" download:
https://github.com/gio83dj/ComfyUI-MetaImageViewer/releases/download/v0.1/ComfyUI.MetaImageViewer.exe

or

1. Clone the repository:
```bash
git clone https://github.com/gio83dj/ComfyUI-MetaImageViewer.git
cd comfyui_metadata_viewer
```

2. Install dependencies:
```bash
pip install Pillow
```

3. Run the application:
```bash
python "ComfyUI MetaImageViewer.py"
```

## 🌍 Localization

The application supports multiple languages. Change the language by modifying the `LANG` variable at the top of the code:

```python
LANG = "en"  # English (default)
LANG = "it"  # Italian
```

Supported languages:
- 🇬🇧 English (en)
- 🇮🇹 Italian (it)

Want to add your language? Simply add a new entry to the `TRANSLATIONS` dictionary!

## 🎮 Usage

### Basic Controls

| Action | Control |
|--------|---------|
| Select folder | "Select Folder" button |
| Next image | `Right Arrow` or `Mouse Wheel Down` |
| Previous image | `Left Arrow` or `Mouse Wheel Up` |
| Go to specific image | Click on thumbnail |
| Resize text area | Drag green bar |
| Context menu | Right-click on image |

### Folder Structure

The app works best with this structure:
```
main_folder/
├── image1.png
├── image2.jpg
├── subfolder1/
│   ├── img_a.png
│   └── img_b.png
└── subfolder2/
    └── img_c.png
```

### Supported Metadata

The application automatically extracts from JSON metadata embedded in PNG images:
- **Checkpoint**: Models used (`ckpt_name`)
- **Prompt**: Generation texts (`text`)
- **Seed**: Random seeds (`seed`, `noise_seed`)
- **LoRA**: Applied LoRA models (`lora_name`)

## 🎨 Screenshots

The interface shows:
- Scrollable thumbnail strip at the top
- Main image in the center (automatically resized)
- Metadata area at the bottom (adjustable height)
- Combobox for subfolder selection

## ⚙️ Configuration

You can modify these variables at the beginning of the code:

```python
MIN_RIGHE_TEXT = 6          # Minimum metadata area height
MAX_RIGHE_TEXT = 30         # Maximum metadata area height
thumbnail_size = 80         # Thumbnail size (pixels)
```

## 🔧 Context Menu Features

Right-click on the image to:
- **Explore**: Opens the folder containing the image in File Explorer (Windows)
- **Delete**: Deletes the current image (with confirmation)

## 📝 Notes

- Thumbnails are saved in `.thumbnails` folders to speed up subsequent loading
- Deleting images automatically updates the thumbnail strip
- The `os.startfile()` function is Windows-specific

## 🐛 Known Issues

- The "Explore" function only works on Windows (uses `os.startfile`)
- Only supports PNG, JPG, JPEG formats

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests
- Improve documentation

## 📄 License

This project is released under the MIT License. See the `LICENSE` file for details.

## 👤 Author

Created to quickly manage and visualize AI-generated image collections.

## 🙏 Acknowledgments

- Built with Python and Tkinter
- Image handling with Pillow (PIL)
- Inspired by the needs of the AI image generation community

---

⭐ If you find this project useful, consider leaving a star on GitHub!
