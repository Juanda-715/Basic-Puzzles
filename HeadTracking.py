"""
    Este Codigo permite seleccionar un archivo STL y mediante la libreria
    OpenCV se hace el trackeo de la cabeza de una persona cambiando la perspectiva
    del modelo STL en función de la posición y orientación de la cabeza 

    Presentado por: 
        Laura Maria Vargas
        David Santaigo Arevalo
        Juan David Montaña

"""

import cv2
import numpy as np
import open3d as o3d
from tkinter import Tk, filedialog



# Función para seleccionar el archivo CAD
def select_cad_file():
    Tk().withdraw()
    file_path = filedialog.askopenfilename(title="Selecciona un modelo CAD", filetypes=[("Archivos CAD", "*.stl *.ply *.obj")])
    return file_path

# Cargar modelo CAD
cad_model_path = select_cad_file()
if not cad_model_path:
    print("No se seleccionó ningún modelo CAD. Cerrando programa.")
    exit()

mesh = o3d.io.read_triangle_mesh(cad_model_path)
mesh.compute_vertex_normals()

# Crear una copia del modelo original
original_mesh = o3d.geometry.TriangleMesh(
    vertices=mesh.vertices,
    triangles=mesh.triangles,
)
original_mesh.compute_vertex_normals()

# Inicializar captura de video
cap = cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Ventana de Open3D
vis = o3d.visualization.Visualizer()
vis.create_window()
vis.add_geometry(mesh)

# Variables para suavizar el movimiento y aumentar el rango de rotación
alpha = 0.2  # Factor de suavizado
prev_angle_x = 0
prev_angle_y = 0
max_rotation = np.pi / 3  # Rango máximo de rotación

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) > 0:
        x, y, w, h = faces[0]  # Tomar solo la primera cara detectada
        cx, cy = x + w // 2, y + h // 2

        # Detectar rostros en la imagen
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Dibujar rectángulos alrededor de los rostros detectados
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Normalizar coordenadas
        angle_x = (cx - frame.shape[1] // 2) / frame.shape[1] * max_rotation
        angle_y = (cy - frame.shape[0] // 2) / frame.shape[0] * max_rotation
        
        # Suavizado
        angle_x = alpha * angle_x + (1 - alpha) * prev_angle_x
        angle_y = alpha * angle_y + (1 - alpha) * prev_angle_y
        prev_angle_x, prev_angle_y = angle_x, angle_y

        # Restaurar modelo a su estado original antes de aplicar nueva rotación
        mesh.vertices = o3d.utility.Vector3dVector(np.asarray(original_mesh.vertices))
        mesh.triangles = o3d.utility.Vector3iVector(np.asarray(original_mesh.triangles))
        mesh.compute_vertex_normals()

        # Aplicar rotación absoluta (en lugar de acumulativa)
        R = mesh.get_rotation_matrix_from_xyz((angle_y, angle_x, 0))
        mesh.rotate(R, center=(0, 0, 0))

        vis.update_geometry(mesh)
    
    vis.poll_events()
    vis.update_renderer()
    
    frame_resized = cv2.resize(frame, (500, 350))
    cv2.imshow("Head Tracking", frame_resized)
    

cap.release()
cv2.destroyAllWindows()
vis.destroy_window()