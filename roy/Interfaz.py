import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from ROI import procesar_imagen, procesar_imagen_sin_mascara

###############################################################################
#                 VARIABLES GLOBALES Y CONFIG
###############################################################################
ruta_imagen_actual = None
ruta_mascara_actual = None
current_oval_id = None
circles_ids = []  # guardamos los ids de los óvalos
MAX_CIRCULOS = 2  # Solo se permiten 2 círculos en modo sin máscara

###############################################################################
#                          FUNCIÓN on_select_option
###############################################################################
def on_select_option():
    """Habilitar/Deshabilitar botón 'Cargar Mascara' según radiobutton."""
    if mask_option.get() == 1:
        btn_cargar_mascara.config(state=tk.NORMAL)
    else:
        btn_cargar_mascara.config(state=tk.DISABLED)

###############################################################################
#                          FUNCIÓN cargar_imagen
###############################################################################
def cargar_imagen():
    global ruta_imagen_actual
    file_path = filedialog.askopenfilename(
        title="Seleccionar Imagen",
        filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")]
    )
    if file_path:
        ruta_imagen_actual = file_path
        # Mostramos una vista previa en 'label_imagen_original'
        img_pil = Image.open(ruta_imagen_actual)
        img_pil.thumbnail((250, 250))
        tk_img = ImageTk.PhotoImage(img_pil)
        label_imagen_original.config(image=tk_img, text="")
        label_imagen_original.image = tk_img

###############################################################################
#                          FUNCIÓN cargar_mascara
###############################################################################
def cargar_mascara():
    global ruta_mascara_actual
    file_path = filedialog.askopenfilename(
        title="Seleccionar Mascara",
        filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")]
    )
    if file_path:
        ruta_mascara_actual = file_path


###############################################################################
#            FUNCIONES DE DIBUJO EN MODO SIN MÁSCARA
###############################################################################
drawing = False
start_x, start_y = 0, 0


def on_mouse_down(event):
    global drawing, start_x, start_y, current_oval_id
    # Verificar si ya hay 2 círculos
    if len(circles_ids) >= MAX_CIRCULOS:
        print("Ya hay 2 círculos. No se pueden dibujar más.")
        return

    drawing = True
    start_x, start_y = event.x, event.y
    current_oval_id = canvas_roi.create_oval(start_x, start_y, start_x, start_y,
                                             outline="red", width=2)

def on_mouse_move(event):
    if drawing and current_oval_id is not None:
        canvas_roi.coords(current_oval_id, start_x, start_y, event.x, event.y)

def on_mouse_up(event):
    global drawing, current_oval_id
    drawing = False
    if current_oval_id is not None:
        circles_ids.append(current_oval_id)
    current_oval_id = None

def borrar_circulos():
    """ Elimina los círculos dibujados en el Canvas. """
    for cid in circles_ids:
        canvas_roi.delete(cid)
    circles_ids.clear()

def area_circulo(x1, y1, x2, y2):
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    r = (w + h)/4
    return 3.14159 * (r**2)

def calcular_cdr_manual():
    """ Requiere exactamente 2 círculos: disco y copa. """
    if len(circles_ids) < 2:
        print("Se necesitan 2 círculos para calcular CDR.")
        return

    # Primer óvalo => disco
    x1d,y1d,x2d,y2d = canvas_roi.coords(circles_ids[0])
    area_disco = area_circulo(x1d,y1d,x2d,y2d)

    # Segundo óvalo => copa
    x1c,y1c,x2c,y2c = canvas_roi.coords(circles_ids[1])
    area_copa = area_circulo(x1c,y1c,x2c,y2c)

    if area_disco>0:
        cdr = area_copa / area_disco
        label_ratio_manual.config(text=f"C/D manual = {cdr:.2f}")
    else:
        label_ratio_manual.config(text="C/D manual = Error (disco=0)")


###############################################################################
#            LIMPIAR (RESET) LA INTERFAZ
###############################################################################
def limpiar_interfaz():
    global ruta_imagen_actual, ruta_mascara_actual
    ruta_imagen_actual = None
    ruta_mascara_actual = None

    # Borrar label imagen original
    label_imagen_original.config(image="", text="Imagen Original")
    label_imagen_original.image = None

    # Borrar las 3 labels (org, mask, cup)
    label_resultado_org.config(image="", text="")
    label_resultado_org.image = None

    label_resultado_disc.config(image="", text="")
    label_resultado_disc.image = None

    label_resultado_cup.config(image="", text="")
    label_resultado_cup.image = None

    # Ratios
    label_ratio_a.config(text="C/D ratio a = --")
    label_ratio_vert.config(text="C/D ratio vert = --")
    label_ratio_manual.config(text="C/D manual = --")

    # Canvas
    borrar_circulos()
    canvas_roi.delete("all")

###############################################################################
def ejecutar_proceso():
    if not ruta_imagen_actual:
        print("No se ha cargado ninguna imagen.")
        return

    # 1) Ocultar Canvas y Botón Manual, para modo con máscara
    canvas_roi.pack_forget()
    btn_calcular_manual.pack_forget()
    btn_borrar_circ.pack_forget()
    label_ratio_manual.config(text="C/D manual = --")

    # 2) Limpiar labels
    label_resultado_org.config(image="", text="")
    label_resultado_org.image = None
    label_resultado_disc.config(image="", text="")
    label_resultado_disc.image = None
    label_resultado_cup.config(image="", text="")
    label_resultado_cup.image = None

    # 3) Elegir modo
    if mask_option.get() == 1:
        # ---------------------- CON MASCARA ----------------------
        res = procesar_imagen(
            ruta_imagen_actual,
            ruta_mascara_actual,
            DiscSeg_model_path='Model_DiscSeg_pretrain.h5',
            DiscROI_size=700,
            DiscSeg_size=640
        )
        if not res:
            print("Error con mascara.")
            return
        (org_pil, org_mask_pil, cup_pil, cdr_a, cdr_vert) = res

        # Muestra 3 imágenes horizontales (izq a der):
        if org_pil:
            org_pil.thumbnail((300, 300))
            tk_org = ImageTk.PhotoImage(org_pil)
            label_resultado_org.config(image=tk_org, text="")
            label_resultado_org.image = tk_org

        if org_mask_pil:
            org_mask_pil.thumbnail((180, 180))
            tk_disc = ImageTk.PhotoImage(org_mask_pil)
            label_resultado_disc.config(image=tk_disc, text="")
            label_resultado_disc.image = tk_disc

        if cup_pil:
            cup_pil.thumbnail((300, 300))
            tk_cup = ImageTk.PhotoImage(cup_pil)
            label_resultado_cup.config(image=tk_cup, text="")
            label_resultado_cup.image = tk_cup

        # Ratios
        label_ratio_a.config(text=f"C/D ratio a = {cdr_a:.2f}")
        label_ratio_vert.config(text=f"C/D ratio vert = {cdr_vert:.2f}")

    else:
        # ---------------------- SIN MASCARA ----------------------
        res_sin = procesar_imagen_sin_mascara(
            ruta_imagen_actual,
            DiscSeg_model_path='Model_DiscSeg_pretrain.h5',
            DiscROI_size=700,
            DiscSeg_size=640
        )
        if not res_sin:
            print("Error sin mascara.")
            return
        (roi_pil, cx, cy, org_dif) = res_sin


        # Muestra el ROI recortado en label_resultado_org
        if roi_pil:
            roi_pil.thumbnail((300, 300))
            tk_roi_sin = ImageTk.PhotoImage(roi_pil)
            label_resultado_org.config(image=tk_roi_sin, text="")
            label_resultado_org.image = tk_roi_sin

        if org_dif:
            org_dif.thumbnail((300, 300))
            tk_roi_dif = ImageTk.PhotoImage(org_dif)
            label_resultado_org.config(image=tk_roi_dif, text="")
            label_resultado_org.image = tk_roi_dif

        # Sin ratio a/vert
        label_ratio_a.config(text="C/D ratio a = --")
        label_ratio_vert.config(text="C/D ratio vert = --")

        # Adicionalmente, queremos poner ese ROI en el canvas para dibujar
        canvas_roi.delete("all")
        borrar_circulos()

        # Convertimos la roi
        global tk_roi
        tk_roi = tk_roi_sin  # referenciamos
        w, h = roi_pil.width, roi_pil.height
        canvas_roi.config(width=w, height=h)
        canvas_roi.create_image(0, 0, anchor=tk.NW, image=tk_roi)
        canvas_roi.image = tk_roi

        # Mostramos Canvas y Botones de manual
        canvas_roi.pack(side=tk.LEFT, padx=10, pady=10)
        btn_calcular_manual.pack(side=tk.LEFT, padx=10)
        btn_borrar_circ.pack(side=tk.LEFT, padx=10)


###############################################################################
#                CREAR LA VENTANA
###############################################################################
ventana = tk.Tk()
ventana.title("Detección de Glaucoma")
ventana.configure(bg="#b9d7f6")
ventana.geometry("1300x900")

# FRAME TOP => Radiobuttons y Botones
frame_top = tk.Frame(ventana, bg="#b0bac3")
frame_top.pack(side=tk.TOP, fill=tk.X, pady=5)

mask_option = tk.IntVar(value=1)
radio_con_mask = tk.Radiobutton(frame_top, text="Con Máscara",
                                variable=mask_option, value=1, command=on_select_option, bg="#b0bac3")
radio_con_mask.pack(side=tk.LEFT, padx=5)

radio_sin_mask = tk.Radiobutton(frame_top, text="Sin Máscara",
                                variable=mask_option, value=0, command=on_select_option, bg="#b0bac3")
radio_sin_mask.pack(side=tk.LEFT, padx=5)

btn_cargar_imagen = tk.Button(frame_top, text="Cargar Imagen", command=cargar_imagen)
btn_cargar_imagen.pack(side=tk.LEFT, padx=5)

btn_cargar_mascara = tk.Button(frame_top, text="Cargar Mascara", command=cargar_mascara)
btn_cargar_mascara.pack(side=tk.LEFT, padx=5)

btn_procesar = tk.Button(frame_top, text="Procesar", command=ejecutar_proceso)
btn_procesar.pack(side=tk.LEFT, padx=5)

btn_limpiar = tk.Button(frame_top, text="Limpiar", command=limpiar_interfaz)
btn_limpiar.pack(side=tk.LEFT, padx=5)

# FRAME para la imagen original
frame_left = tk.Frame(ventana, bg="#b9d7f6")
frame_left.pack(side=tk.LEFT, padx=10, pady=10)

# Ubicacion imagen original y las otras 3 imagenes
label_imagen_original = tk.Label(frame_left, text="Imagen Original", bg="gray")
label_imagen_original.grid(row=0, column=0, padx=10)
label_resultado_org = tk.Label(frame_left, bg="white")
label_resultado_org.grid(row=0, column=2, padx=10)
label_resultado_disc = tk.Label(frame_left, bg="white")
label_resultado_disc.grid(row=0, column=3, padx=10)
label_resultado_cup = tk.Label(frame_left, bg="white")
label_resultado_cup.grid(row=0, column=4, padx=10)

# FRAME BOTTOM: RATIOS
frame_bottom = tk.Frame(ventana, bg="#b9d7f6")
frame_bottom.pack(side=tk.RIGHT, fill=tk.X, pady=50)

label_ratio_a = tk.Label(frame_top, text="C/D ratio a = --", font=("Arial", 12), bg="#b9d7f6")
label_ratio_a.pack(side=tk.RIGHT, padx=50)

label_ratio_vert = tk.Label(frame_top, text="C/D ratio vert = --", font=("Arial", 12), bg="#b9d7f6")
label_ratio_vert.pack(side=tk.RIGHT, padx=50)

# Canvas para modo sin máscara (inicialmente invisible)
canvas_roi = tk.Canvas(ventana, bg="#b9d7f6", width=300, height=300)
canvas_roi.bind("<Button-1>", on_mouse_down)
canvas_roi.bind("<B1-Motion>", on_mouse_move)
canvas_roi.bind("<ButtonRelease-1>", on_mouse_up)

# Botones y label para CDR Manual
btn_calcular_manual = tk.Button(ventana, text="Calcular CDR Manual", command=calcular_cdr_manual)
btn_borrar_circ = tk.Button(ventana, text="Borrar Círculos", command=borrar_circulos)

label_ratio_manual = tk.Label(frame_top, text="C/D manual = --", font=("Arial", 12))
label_ratio_manual.pack(side=tk.RIGHT, pady=20)

ventana.mainloop()
