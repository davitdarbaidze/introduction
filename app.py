import os
from moviepy.editor import VideoFileClip
import numpy as np

# Function to extract audio and convert it to binary representation
def extract_audio_and_convert_to_binary(input_folder, output_folder):
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all the MP4 files in the input folder
    mp4_files = [file for file in os.listdir(input_folder) if file.endswith('.mp4')]

    for mp4_file in mp4_files:
        input_path = os.path.join(input_folder, mp4_file)
        output_path = os.path.join(output_folder, f"{os.path.splitext(mp4_file)[0]}.bin")

        try:
            
            # Load the video clip and extract audio
            video_clip = VideoFileClip(input_path)
            audio = video_clip.audio

            # Convert the audio data to a binary representation
            audio_binary = np.array(audio.to_soundarray(), dtype=np.int16).tobytes()

            # Write the binary audio data to a file
            with open(output_path, 'wb') as binary_file:
                binary_file.write(audio_binary)
        except Exception as e:
            print(f"Error processing {mp4_file}: {e}")

if __name__ == "__main__":
    
    input_folder = "../videos"  # Replace with the path to your input folder containing MP4 files
    output_folder = "../outputvideos"  # Replace with the path where you want to save the binary files
    input_folder1 = "../videos"  # Replace with the path to your input folder containing MP4 files
    output_folder1 = "../outputvideos"  # Replace with the path where you want to save the binary files

    extract_audio_and_convert_to_binary(input_folder, output_folder)
