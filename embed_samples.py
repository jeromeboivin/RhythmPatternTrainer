#!/usr/bin/env python3
"""
Convert WAV samples to mono 22050Hz and embed them as base64 in HTML file.
This solves the CORS issue when opening HTML files locally.
"""

import os
import base64
import wave
import struct
from pathlib import Path

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("Warning: pydub not available. Install with: pip install pydub")
    print("Samples will be embedded as-is without conversion.")


def convert_to_mono_22khz(input_path):
    """Convert audio file to mono 22050Hz WAV format."""
    if not PYDUB_AVAILABLE:
        # Just read the file as-is
        with open(input_path, 'rb') as f:
            return f.read()
    
    try:
        # Load audio file
        audio = AudioSegment.from_wav(input_path)
        
        # Convert to mono
        if audio.channels > 1:
            audio = audio.set_channels(1)
        
        # Convert to 22050 Hz
        if audio.frame_rate != 22050:
            audio = audio.set_frame_rate(22050)
        
        # Export to bytes
        from io import BytesIO
        buffer = BytesIO()
        audio.export(buffer, format='wav')
        return buffer.getvalue()
    
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        # Fallback: read original file
        with open(input_path, 'rb') as f:
            return f.read()


def audio_to_base64(audio_data):
    """Convert audio bytes to base64 string."""
    return base64.b64encode(audio_data).decode('utf-8')


def process_samples(samples_dir):
    """Process all WAV samples in the directory."""
    samples = {}
    sample_files = {
        'tambourine_strong': 'tambourine_strong.wav',
        'tambourine_weak': 'tambourine_weak.wav',
        'kick': 'kick.wav',
        'hihat': 'hihat.wav',
        'rim': 'rim.wav',
        'bell': 'bell.wav'
    }
    
    for name, filename in sample_files.items():
        filepath = Path(samples_dir) / filename
        if filepath.exists():
            print(f"Processing {filename}...")
            audio_data = convert_to_mono_22khz(filepath)
            base64_data = audio_to_base64(audio_data)
            samples[name] = base64_data
            print(f"  ✓ {filename} -> {len(base64_data)} chars")
        else:
            print(f"  ✗ {filename} not found")
    
    return samples


def embed_samples_in_html(html_path, samples):
    """Embed base64-encoded samples into HTML file."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Create the embedded samples JavaScript object
    samples_js = "        const embeddedSamples = {\n"
    for name, data in samples.items():
        samples_js += f"            {name}: '{data}',\n"
    samples_js += "        };\n"
    
    # Find where to insert (after the samples declaration)
    marker = "        let samples = {"
    if marker in html_content:
        insert_pos = html_content.find(marker) + len(marker)
        # Find the closing brace and semicolon
        closing_pos = html_content.find("};", insert_pos) + 2
        
        # Insert embedded samples right after
        html_content = (
            html_content[:closing_pos] + "\n\n" +
            samples_js +
            html_content[closing_pos:]
        )
        
        # Now replace the loadSamples function
        load_samples_start = html_content.find("        async function loadSamples() {")
        if load_samples_start != -1:
            # Find the end of the function
            load_samples_end = html_content.find("        }", load_samples_start) + 9
            
            new_load_samples = """        async function loadSamples() {
            // Load from embedded base64 data if available, otherwise try to fetch
            const sampleFiles = {
                tambourine_strong: 'tambourine_strong.wav',
                tambourine_weak: 'tambourine_weak.wav',
                kick: 'kick.wav',
                hihat: 'hihat.wav'
            };

            for (const [name, file] of Object.entries(sampleFiles)) {
                try {
                    // Try embedded samples first
                    if (embeddedSamples[name]) {
                        const binaryString = atob(embeddedSamples[name]);
                        const bytes = new Uint8Array(binaryString.length);
                        for (let i = 0; i < binaryString.length; i++) {
                            bytes[i] = binaryString.charCodeAt(i);
                        }
                        samples[name] = await audioContext.decodeAudioData(bytes.buffer);
                        console.log(`✓ Loaded embedded sample: ${file}`);
                        continue;
                    }
                    
                    // Fallback: try to fetch
                    const response = await fetch(file);
                    if (response.ok) {
                        const arrayBuffer = await response.arrayBuffer();
                        samples[name] = await audioContext.decodeAudioData(arrayBuffer);
                        console.log(`✓ Loaded sample from file: ${file}`);
                    } else {
                        console.log(`✗ Sample ${file} not found (${response.status})`);
                    }
                } catch (e) {
                    console.log(`✗ Error loading ${file}:`, e.message);
                }
            }
        }"""
            
            html_content = html_content[:load_samples_start] + new_load_samples + html_content[load_samples_end:]
    
    # Write back
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✓ Updated {html_path}")


def main():
    script_dir = Path(__file__).parent
    html_path = script_dir / "index.html"
    
    if not html_path.exists():
        print(f"Error: {html_path} not found!")
        return
    
    print("=== Rhythm Pattern Trainer - Sample Embedder ===\n")
    
    # Process samples
    samples = process_samples(script_dir)
    
    if not samples:
        print("\nNo samples found! Please add WAV files:")
        print("  - tambourine_strong.wav")
        print("  - tambourine_weak.wav")
        print("  - kick.wav")
        print("  - hihat.wav")
        return
    
    # Embed into HTML
    print("\nEmbedding samples into HTML...")
    embed_samples_in_html(html_path, samples)
    
    print("\n✓ Done! Reload index.html in your browser.")


if __name__ == "__main__":
    main()
