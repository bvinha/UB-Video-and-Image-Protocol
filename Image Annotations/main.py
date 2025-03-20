import cv2
import pandas as pd
import os

def extract_frames(video_path, csv_path, output_folder):
    # Leer el archivo CSV
    df = pd.read_csv(csv_path, delimiter=';', decimal=',')

    # Asegurarse de que la carpeta de salida existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Abrir el video
    cap = cv2.VideoCapture(video_path)

    # Iterar sobre cada fila del DataFrame
    for index, row in df.iterrows():
        # Obtener el segundo del video
        second = row['Frame']
        print(f"second: {second}")
    


        # Calcular el frame correspondiente
        cap.set(cv2.CAP_PROP_POS_MSEC, second*1000)

        # Leer el frame
        ret, frame = cap.read()

        # Si el frame se leyó correctamente, guardarlo como imagen PNG
        if ret:
            cv2.imwrite(os.path.join(output_folder, f'{second}.png'), frame)
            print(f"Done: {second}")

    # Liberar el video
    cap.release()

# Uso de la función
#extract_frames('video.mp4', 'data.csv', 'frames')
extract_frames('/Volumes/LaCie/OASIS_ROV_VIDEOS/Dive15a.avi', 'oasis15_selected.csv', '/Users/arianmartinez/Desktop/oasis15')




