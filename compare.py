import os
import torchaudio
import torch
import torch.nn.functional as F
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO

# Ensure CUDA (GPU support) is available
if not torch.cuda.is_available():
    raise Exception("CUDA (GPU support) is not available.")

# Set the device to GPU
device = torch.device("cuda")

def check_file_exists(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

def convert_binary_to_tensor(binary_file_path, sample_rate=44100):
    # Check if the file exists
    check_file_exists(binary_file_path)

    # Load the binary data
    binary_data = open(binary_file_path, 'rb').read()
    
    # Convert the binary data to a PyTorch tensor
    audio_tensor, sample_rate = torchaudio.load(io.BytesIO(binary_data), sample_rate=sample_rate)
    
    return audio_tensor

def trim_audio(audio_tensor, duration_in_seconds=300):
    # Calculate the number of frames to keep for the specified duration
    num_frames = int(duration_in_seconds * audio_tensor.shape[1] / audio_tensor.shape[0])
    
    # Trim the audio tensor
    trimmed_audio = audio_tensor[:, :num_frames]
    
    return trimmed_audio

def find_similar_segments(audio1_path, audio2_path, threshold=0.95, duration_to_trim_seconds=300):
    # Check if the files exist
    check_file_exists(audio1_path)
    check_file_exists(audio2_path)

    # Convert binary files to PyTorch tensors
    audio1_tensor = convert_binary_to_tensor(audio1_path)
    audio2_tensor = convert_binary_to_tensor(audio2_path)

    # Trim the input tensors to the specified duration
    audio1_trimmed = trim_audio(audio1_tensor, duration_to_trim_seconds)
    audio2_trimmed = trim_audio(audio2_tensor, duration_to_trim_seconds)

    # Transfer tensors to GPU
    audio1_trimmed = audio1_trimmed.to(device)
    audio2_trimmed = audio2_trimmed.to(device)

    # Calculate the cross-correlation between the two audio signals
    cross_corr = F.conv1d(audio1_trimmed, audio2_trimmed.flip(2))

    # Normalize cross-correlation values to the range [0, 1]
    normalized_corr = (cross_corr - torch.min(cross_corr)) / (torch.max(cross_corr) - torch.min(cross_corr))

    # Find indices where the correlation exceeds the threshold
    similar_indices = torch.where(normalized_corr >= threshold)

    # Print the time positions of similar segments
    if len(similar_indices[0]) > 0:
        logging.info("Similar segments found:")
        for idx in range(len(similar_indices[0])):
            time_seconds = similar_indices[2][idx] / audio1_trimmed.shape[2]
            logging.info(f"At {time_seconds:.2f} seconds")
    else:
        logging.info("No similar segments found.")

if __name__ == "__main__":
    audio1_path = "../outputvideos/The Office S02E01 The Dundies.bin"  # Replace with the path to your first binary audio file
    audio2_path = "../outputvideos/The Office S02E03 Office Olympics.bin"  # Replace with the path to your second binary audio file

    logging.info("Comparing audio files...")
    find_similar_segments(audio1_path, audio2_path)
    logging.info("Comparison completed.")
