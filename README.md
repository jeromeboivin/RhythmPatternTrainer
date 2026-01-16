# Rhythm Pattern Trainer

A web-based rhythm training tool for practicing eighth and sixteenth note patterns with audio playback.

## Features

### Rhythm Patterns
- 14 different patterns: eighth notes, sixteenth notes, dotted rhythms
- Visual notation display with Unicode musical symbols
- Multiple font options (default, serif, music, monospace)
- Selectable pattern library with quick enable/disable

### Playback Controls
- Adjustable tempo (40-200 BPM)
- Play modes: loop, one-time, or random shuffle
- Swing control (0-100%) for groove feel
- Lookahead (1-8 bars) to see upcoming patterns

### Sound Options
- Three sound sources: Basic beep, Tambourine, or Drum kit
- Metronome modes: Beats only, 8th subdivisions, or silent
- Optional bell accent on first beat
- High-quality embedded audio samples

### Visual Settings
- Light and dark theme support
- Customizable note font display
- Real-time pattern highlighting during playback
- Beat separator visualization

### Technical
- Works completely offline (all audio embedded as base64)
- No installation required - pure HTML/CSS/JavaScript
- Responsive design for different screen sizes

## Usage

Simply open `index.html` in your web browser. No installation or server required.

## Development

The `embed_samples.py` script converts and embeds audio samples as base64 data into the HTML file for offline use.
