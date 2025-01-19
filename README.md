# Detecting Intro time in Songs

## 1. Introduction

### Goal

Most songs are structured into Intro, Main, and Outro sections. The intro is a critical part of a song; knowing its length helps determine how much time there is to set up the hook. While one way to find the length of an intro is to listen to it, this approach is not practical for analyzing thousands of songs manually.

To overcome this, I developed a Python script that automatically identifies where the intro ends and the main section begins. The primary objective of this project is to detect the transition from the intro to the main part of a song. This transition is found by spotting a significant change in the audio signal—an "inflection point"—through analysis of the spectral flux.

### Key Concept: Spectral Flux

Spectral flux measures how the power spectrum of an audio signal changes from one frame to the next. Large shifts in spectral flux often indicate important moments in a song, such as the start of a new instrument or vocals.

![sound](https://github.com/parthshr370/Sound-Intro-Time/blob/main/sound.png)


### High-Level Process

1. **Load** the audio file, either fully or partially.
2. **Compute** the Short-Time Fourier Transform (STFT) to derive time-based magnitude spectra.
3. **Calculate** the spectral flux by examining changes between consecutive frames.
4. **Smooth** the spectral flux using a sliding window to reduce noise.
5. **Detect** the point where the smoothed spectral flux surpasses a specific threshold.
6. **Report** the detected point as the time of the intro transition.

---
## 2. How to Run the Code

1. **Install Dependencies:**
    
    ```bash
    pip install librosa numpy matplotlib
    ```
    
2. **Save the Code:**
    
    - File name: `SoundToIntroFile.py`.
3. **Execute the Script:**
    
    ```bash
    python SoundToIntroFile.py
    ```
    
4. **Provide Inputs:**
    
    - Audio file path, FFT size, hop length, window size for smoothing, frequency cutoff, and decision on plotting.


## 3. Code Implementation

### 3.1 Function: `load_audio`

```python
def load_audio(audio_path, duration=60):
    ...
```

- **Purpose:** Loads an audio file for analysis.
- **Parameters:** `audio_path` (path to the file), `duration` (length in seconds to load, default is 60 seconds).
- **Returns:** Audio data and sampling rate.
- **Errors:** Handles file not found or loading errors gracefully.

### 3.2 Function: `compute_stft`

```python
def compute_stft(y, sr, n_fft=2048, hop_length=512, freq_cutoff=1000):
    ...
```

- **Purpose:** Computes the Short-Time Fourier Transform of the audio data.
- **Parameters:** Raw audio data `y`, sampling rate `sr`, FFT window size `n_fft`, frame hop length `hop_length`, frequency cutoff `freq_cutoff`.
- **Returns:** Magnitude spectra truncated to `freq_cutoff`.

### 3.3 Function: `compute_flux`

```python
def compute_flux(magnitude):
    ...
```

- **Purpose:** Calculates the spectral flux from the magnitude spectra.
- **Returns:** Flux values indicating spectral changes.

### 3.4 Function: `apply_sliding_window`

```python
def apply_sliding_window(flux, window_size=5):
    ...
```

- **Purpose:** Smooths the spectral flux to reduce variability and noise.
- **Parameters:** Flux data `flux`, size of the window `window_size`.
- **Returns:** Smoothed flux data.

### 3.5 Function: `find_sudden_change_time`

```python
def find_sudden_change_time(flux_sliding, hop_length, sr, alpha=2.0):
    ...
```

- **Purpose:** Identifies the first significant change in the smoothed flux that exceeds the threshold.
- **Parameters:** Smoothed flux `flux_sliding`, hop length `hop_length`, sampling rate `sr`, sensitivity `alpha`.
- **Returns:** Time of the detected change in seconds, or `None` if no change exceeds the threshold.

### 3.6 Function: `plot_flux`

```python
def plot_flux(flux):
    ...
```

- **Purpose:** Visualizes the spectral flux over time for analysis.
- **Parameters:** Flux data `flux`.
- **Visualization:** Line plot of flux values.

### 3.7 Function: `main`

```python
def main():
    ...
```

- **Purpose:** Orchestrates the entire analysis process from loading the audio to detecting the intro transition.
- **User Interaction:** Prompts for file paths and analysis parameters, and optionally displays the flux visualization.

---
### Handling Edge Cases

- **Gradual Intros:** Modify detection algorithms to better capture slow-fading intros.
- **Multiple Peaks:** Establish criteria to determine the most significant peak when multiple candidates are present.


For any suggestions 
Reach me out at [X](https://x.com/parthshr370) or [Linkdin](https://www.linkedin.com/in/parthshr370/)
