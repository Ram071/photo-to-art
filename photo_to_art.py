import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


class PhotoToArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo to Real Art")
        self.root.geometry("900x700")

        self.original = None
        self.result = None

        tk.Label(
            root,
            text="🎨 PHOTO TO REAL ART",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

        tk.Button(
            root,
            text="Choose Photo",
            command=self.choose_photo,
            font=("Arial", 14),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=8
        ).pack(pady=10)

        self.style_var = tk.StringVar(value="Pencil Sketch")

        styles = [
            "Pencil Sketch",
            "Cartoon",
            "Watercolor",
            "Pop Art",
            "Oil Painting"
        ]

        tk.Label(root, text="Choose Art Style:", font=("Arial", 13)).pack()

        tk.OptionMenu(
            root,
            self.style_var,
            *styles
        ).pack(pady=8)

        tk.Button(
            root,
            text="Transform into Art",
            command=self.transform,
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=8
        ).pack(pady=10)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=15)

        tk.Button(
            root,
            text="Save Artwork",
            command=self.save_art,
            font=("Arial", 12),
            bg="#FF9800",
            fg="white",
            padx=15,
            pady=6
        ).pack()

    def choose_photo(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png *.bmp")
            ]
        )

        if path:
            self.original = cv2.imread(path)

            if self.original is None:
                messagebox.showerror("Error", "Could not open image.")
                return

            self.show_image(self.original)

    def transform(self):
        if self.original is None:
            messagebox.showwarning(
                "No Photo",
                "Please choose a photo first."
            )
            return

        style = self.style_var.get()

        if style == "Pencil Sketch":
            self.result = self.pencil_sketch(self.original)

        elif style == "Cartoon":
            self.result = self.cartoon(self.original)

        elif style == "Watercolor":
            self.result = cv2.stylization(
                self.original,
                sigma_s=60,
                sigma_r=0.6
            )

        elif style == "Pop Art":
            self.result = self.pop_art(self.original)

        elif style == "Oil Painting":
            self.result = cv2.detailEnhance(
                self.original,
                sigma_s=10,
                sigma_r=0.15
            )

        self.show_image(self.result)

    def pencil_sketch(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        inverted = 255 - gray

        blurred = cv2.GaussianBlur(
            inverted,
            (21, 21),
            0
        )

        sketch = cv2.divide(
            gray,
            255 - blurred,
            scale=256
        )

        return cv2.cvtColor(
            sketch,
            cv2.COLOR_GRAY2BGR
        )

    def cartoon(self, image):
        # Smooth colors
        smooth = cv2.bilateralFilter(
            image,
            9,
            250,
            250
        )

        # Detect edges
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.medianBlur(gray, 7)

        edges = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            9,
            9
        )

        # Combine colors and edges
        cartoon = cv2.bitwise_and(
            smooth,
            smooth,
            mask=edges
        )

        return cartoon

    def pop_art(self, image):
        # Convert to HSV
        hsv = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2HSV
        )

        # Increase saturation
        hsv[:, :, 1] = cv2.add(
            hsv[:, :, 1],
            80
        )

        result = cv2.cvtColor(
            hsv,
            cv2.COLOR_HSV2BGR
        )

        # Posterize colors
        result = result // 64 * 64

        return result

    def show_image(self, image):
        display = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        pil_image = Image.fromarray(display)

        # Resize for display
        pil_image.thumbnail((750, 450))

        photo = ImageTk.PhotoImage(pil_image)

        self.image_label.configure(
            image=photo
        )

        self.image_label.image = photo

    def save_art(self):
        if self.result is None:
            messagebox.showwarning(
                "No Artwork",
                "Create an artwork first."
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[
                ("JPEG Image", "*.jpg"),
                ("PNG Image", "*.png")
            ]
        )

        if path:
            cv2.imwrite(path, self.result)

            messagebox.showinfo(
                "Saved",
                "Your artwork has been saved successfully!"
            )


root = tk.Tk()
app = PhotoToArtApp(root)
root.mainloop()
