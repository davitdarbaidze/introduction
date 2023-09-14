import os
from pydub import AudioSegment
import librosa
import numpy as np

import logging
logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO

def convert_binary_to_wav(binary_file_path, wav_file_path, sample_width=2, frame_rate=44100):
    # Load the binary data
    binary_data = open(binary_file_path, 'rb').read()

    # Create an AudioSegment from the binary data
    audio = AudioSegment(
        data=binary_data,
        sample_width=sample_width,
        frame_rate=frame_rate,
        channels=1  # Mono audio
    )

    # Export the AudioSegment as a WAV file
    audio.export(wav_file_path, format="wav")

def trim_audio(file_path, output_path, duration_in_seconds=300):
    # Convert the binary file to WAV format
    temp_wav_file = "temp_audio.wav"
    convert_binary_to_wav(file_path, temp_wav_file)

    # Load the audio using pydub
    audio = AudioSegment.from_file(temp_wav_file)

    # Trim the audio to the specified duration (in milliseconds)
    trimmed_audio = audio[:duration_in_seconds * 1000]

    # Export the trimmed audio as a WAV file
    trimmed_audio.export(output_path, format="wav")

    # Clean up temporary WAV file
    os.remove(temp_wav_file)

def find_similar_segments(file1_path, file2_path, threshold=0.95, duration_to_trim_seconds=300):
    # Trim the input files to the specified duration
    trimmed_file1_path = "trimmed_file1.wav"
    trimmed_file2_path = "trimmed_file2.wav"
    trim_audio(file1_path, trimmed_file1_path, duration_to_trim_seconds)
    trim_audio(file2_path, trimmed_file2_path, duration_to_trim_seconds)

    # Load audio from trimmed WAV files using pydub
    audio1 = AudioSegment.from_file(trimmed_file1_path)
    audio2 = AudioSegment.from_file(trimmed_file2_path)

    # Calculate the cross-correlation between the two audio signals
    cross_corr = np.correlate(audio1.get_array_of_samples(), audio2.get_array_of_samples(), mode='full')

    # Normalize cross-correlation values to the range [0, 1]
    normalized_corr = (cross_corr - np.min(cross_corr)) / (np.max(cross_corr) - np.min(cross_corr))

    # Find indices where the correlation exceeds the threshold
    similar_indices = np.where(normalized_corr >= threshold)[0]

    # Print the time positions of similar segments
    if len(similar_indices) > 0:
        logging.info("Similar segments found:")
        for index in similar_indices:
            time_seconds = index / audio1.frame_rate
            logging.info(f"At {time_seconds:.2f} seconds")
    else:
        logging.info("No similar segments found.")

    # Clean up temporary WAV files
    os.remove(trimmed_file1_path)
    os.remove(trimmed_file2_path)

if __name__ == "__main__":
    file1_path = "../outputvideos/The Office S02E01 The Dundies.bin"  # Replace with the path to your first binary file
    file2_path = "../outputvideos/The Office S02E03 Office Olympics.bin"  # Replace with the path to your second binary file

    logging.info("Comparing audio files...")
    find_similar_segments(file1_path, file2_path)
    logging.info("Comparison completed.")