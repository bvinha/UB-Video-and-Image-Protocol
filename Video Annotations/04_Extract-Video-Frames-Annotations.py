#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Run code to extract video frames based on the "label_name" column from BIIGLE annotations report
"""

#import libraries
import pandas as pd
import cv2
import os

#build 'extract_frames' function
def extract_frames(csv_path, video_folder, output_folder, species_name):
    #load the BIIGLE annotations CSV
    annotations = pd.read_csv(csv_path)
    
    #filter annotations for the target species
    species_annotations = annotations[annotations['label_name'] == species_name]
    
    #create output folder to save extracted frames, if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    #process each video file
    for video_name in species_annotations['video_filename'].unique():
        video_path = os.path.join(video_folder, video_name)
        
        #check if video exists
        if not os.path.exists(video_path):
            print(f"Warning: Video {video_name} not found in {video_folder}")
            continue
        
        #open  video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Cannot open video {video_name}")
            continue
        
        #get video frames per seconds (FPS)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            print(f"Error: Cannot determine FPS for {video_name}")
            cap.release()
            continue
        
        #extract frames based on the "frames" column in the annotation file
        video_annotations = species_annotations[species_annotations['video_filename'] == video_name]
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        for _, row in video_annotations.iterrows():
            #convert seconds to frame number
            frame_time = row['frames']
            if pd.isna(frame_time):
                continue
            frame_number = int(float(frame_time) * fps)
            if frame_number >= total_frames:
                print(f"Warning: Frame {frame_number} exceeds total frames in {video_name}")
                continue
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            if ret:
                #add label to frame, with information, on species, video filename and frame number
                label = f"{species_name} | {video_name} | Frame: {frame_number}"
                text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                text_x = 10
                text_y = frame.shape[0] - 10
                cv2.putText(frame, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                #save frame as image
                frame_filename = f"{species_name.replace(' ', '_')}_{video_name}_frame{frame_number}.png"
                frame_path = os.path.join(output_folder, frame_filename)
                cv2.imwrite(frame_path, frame)
                print(f"Saved: {frame_path}")
            else:
                print(f"Warning: Could not read frame {frame_number} from {video_name}")
        
        cap.release()
    print("Frame extraction complete.")

#ADAPT THIS PART OF THE CODE BASED ON YOUR DIRECTORY/FILE NAMES
csv_path = '/Users/beatriz/Desktop/frames_size/annotation_report.csv' #BIIGLE annotation report
video_folder = '/Users/beatriz/Desktop/frames_size/videos' #Folder containing all the videos to extract frames
output_folder = '/Users/beatriz/Desktop/frames_size/frames' #Output folder to save frames
species_name = 'Eunicella singularis' #Target species

extract_frames(csv_path, video_folder, output_folder, species_name)
