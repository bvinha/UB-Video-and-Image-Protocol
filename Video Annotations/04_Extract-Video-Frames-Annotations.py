"""
Run code to extract video frames based on the "label_name" column from BIIGLE annotations report
"""
#import libraries
import cv2
import pandas as pd
import os

#build 'extract_frames' function
def extract_frames(video_path, csv_path, output_folder, target_label):
    #read csv file
    df = pd.read_csv(csv_path, delimiter=';', decimal=',') #change according to your computer settings, e.g. delimiter= ',', decimal='.'

    #filter by "label_name" in BIIGLE annotation report
    filtered_df = df[df['label_name'] == target_label]

    #make sure output_folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    #open video
    cap = cv2.VideoCapture(video_path)

    #iterate each row in the filtered dataframe
    for index, row in filtered_df.iterrows():
        #get frame number from video
        frame_number = int(row['frames']) #change column name, if different
        print(f"Frame: {frame_number}")

        #calculate corresponding frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        #Read frame
        ret, frame = cap.read()

        #Save frame as PNG
        if ret:
            cv2.imwrite(os.path.join(output_folder, f'{row["video_filename"]}_frame{frame_number}.png'), frame) #change column name, if different
            print(f"Done: {frame_number}")

    #Release video
    cap.release()

#Function Use
#Extract all frames annotated with "Eunicella singularis", from a video file called "video.mp4", 
#based on an annotation report with file name "annotation_report.csv". 
#Frames will be saved to folder named "frames"
extract_frames('video.mp4', 'annotation_report.csv', 'frames', 'Eunicella singularis') #change according to your directory/filenames


