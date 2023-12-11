#!/usr/bin/env python3

import argparse
import librosa
import numpy as np
from PIL import Image

def downsample_audio(file_path, target_sr=4000):
    # Load audio file
    print("Loading and downsamping audio...")
    y, sr = librosa.load(file_path, sr=target_sr)
    return y, sr

def create_barcode(audio_data, output_image):
    # Normalize audio data
    print("Normalising audio...")
    normalized_audio = (audio_data - np.min(audio_data)) / (np.max(audio_data) - np.min(audio_data))

    print("Creating barcode image...")
    # Convert audio waveform to flat pixel list (left-to-right repeating)
    one_horizontal_line = (normalized_audio * 255).astype(np.uint8)

    # Create barcode image
    width = len(one_horizontal_line)
    height = int(width/4)

    barcode = Image.new("L", (width, height))
    pixels = np.tile(one_horizontal_line, height)
    barcode.putdata(pixels)
    barcode.save(output_image)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert audio file to barcode image")
    parser.add_argument("input_audio", help="Path to input audio file (.wav)")
    parser.add_argument("output_image", help="Path to output barcode image (.png)")
    args = parser.parse_args()

    input_file = args.input_audio
    output_image = args.output_image

    audio_data, sample_rate = downsample_audio(input_file)
    create_barcode(audio_data, output_image)
