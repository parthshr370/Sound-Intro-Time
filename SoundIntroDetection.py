import numpy as np
import librosa
import matplotlib.pyplot as plt

def load_audio(audio_path, duration=60):
    try:
        y, sr = librosa.load(audio_path, sr=None, duration=duration)
        return y, sr
    except FileNotFoundError:
        print("Audio file not found. Please check the path.")
        exit()
    except Exception as e:
        print(f"Error loading audio file: {e}")
        exit()

def compute_stft(y, sr, n_fft=2048, hop_length=512, freq_cutoff=1000):
    D = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    magnitude = np.abs(D)
    freq_bins = np.fft.rfftfreq(n_fft, 1/sr)
    max_freq_index = np.where(freq_bins <= freq_cutoff)[0][-1]
    magnitude = magnitude[:max_freq_index + 1, :]
    return magnitude

def compute_flux(magnitude):
    num_frames = magnitude.shape[1]
    flux = np.zeros(num_frames)
    for i in range(1, num_frames):
        diff = magnitude[:, i] - magnitude[:, i-1]
        flux[i] = np.sum(np.abs(diff))
    return flux

def apply_sliding_window(flux, window_size=5):
    num_frames = len(flux)
    flux_sliding = np.zeros_like(flux)
    for i in range(num_frames):
        start = max(0, i - window_size + 1)
        flux_sliding[i] = np.mean(flux[start : i+1])
    return flux_sliding

def find_sudden_change_time(flux_sliding, hop_length, sr, alpha=2.0):
    mean_val = np.mean(flux_sliding)
    std_val = np.std(flux_sliding)
    threshold = mean_val + alpha * std_val
    for i, value in enumerate(flux_sliding):
        if value > threshold:
            return i * (hop_length / sr)
    return None

def plot_flux(flux):
    plt.figure(figsize=(10, 4))
    plt.plot(flux, label='Spectral Flux')
    plt.title('Spectral Flux Over Time')
    plt.xlabel('Time Frame')
    plt.ylabel('Flux')
    plt.legend()
    plt.show()

def main():
    audio_path = input("Enter the path to the audio file: ")
    window_size = int(input("Enter window size for the sliding window (default is 5): ") or "5")
    n_fft = int(input("Enter FFT window size (default is 2048): ") or "2048")
    hop_length = int(input("Enter hop length for STFT (default is 512): ") or "512")
    freq_cutoff = int(input("Enter frequency cutoff for noise reduction (default is 1000 Hz): ") or "1000")
    alpha = float(input("Enter alpha value for threshold calculation (default is 2.0): ") or "2.0")
    visualize = input("Do you want to visualize the spectral flux? (yes/no): ").lower() == 'yes'

    print(f"Attempting to load audio from: {audio_path}")
    y, sr = load_audio(audio_path)
    magnitude = compute_stft(y, sr, n_fft, hop_length, freq_cutoff)
    flux = compute_flux(magnitude)
    flux_sliding = apply_sliding_window(flux, window_size)

    print("Smoothed Flux Values:", flux_sliding)  # Print the smoothed spectral flux values

    change_time = find_sudden_change_time(flux_sliding, hop_length, sr, alpha)
    if change_time is not None:
        print(f"Sudden change detected at ~{change_time:.2f} seconds.")
    else:
        print("No sudden change found above the threshold.")

    if visualize:
        plot_flux(flux_sliding)

if __name__ == "__main__":
    main()
