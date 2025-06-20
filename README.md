# Aria Gen1 Assistive AI
Prototype build 1 (DEMO)
A real-time captioning and assistive system for Meta Project Aria glasses, using AI to generate descriptive captions and answer follow-up questions about your environment. Combines computer vision, natural language processing, and text-to-speech.

## Features
- Real-time video streaming from Aria glasses
- AI-powered image captioning using LLaVA-phi3 (via Ollama)
- Wake word support ("Hey Aria")
- Follow-up Q&A (text or speech)
- Text-to-speech output
- Low-latency processing

## Vision Language Model (VLM)
- **Model:** LLaVA-phi3 (served locally via [Ollama](https://ollama.com/))
- **Prompt:** "Describe this image in a short, informative sentence for someone who is visually impaired."
- **Capabilities:**
  - Real-time image understanding
  - Scene description
  - Follow-up Q&A

## Performance
- **Average Latency:**
  - Image Processing: ~0.2s
  - Model Inference: ~2.5s
  - Total Q&A Latency: ~4.8s
- **Frame Rate:** 10 FPS target
- **Caption Cooldown:** 10 seconds

### Example Output
```
Question: What's in front of me?
Q&A latency: 4.78 seconds
LLaVA says: 1. A man wearing a black shirt sitting at a desk with his hands folded on it next to a whiteboard. He has black hair.
2. The chairs around him are empty.
3. There is also an object that looks like an iPad near the man.
```

## Setup
### Prerequisites
- Python 3.8+
- Meta Project Aria Client SDK (see Meta documentation)
- [Ollama](https://ollama.com/) (for LLaVA)
- OpenCV, Flask, Whisper, etc. (see requirements.txt)
- System: macOS or Linux recommended

### Installation
1. Clone the repository:
```bash
git clone https://github.com/SirAlchemist1/Aria-gen1-assistive-ai.git
cd Aria-gen1-assistive-ai/aria_ai_caption
```
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```
3. Install Ollama and LLaVA-phi3 model:
```bash
curl https://ollama.ai/install.sh | sh
ollama pull llava-phi3
```
4. Install Meta Project Aria SDK (see Meta's official instructions)

### Running the System
1. Start the caption server:
```bash
python caption_server.py
```
2. In a new terminal, start the Aria server:
```bash
python aria_server_caption.py --interface usb
```

## Usage
- Say "Hey Aria" to start captioning
- Type 't' for text follow-up, 's' for speech
- Press 'q' to quit

## Troubleshooting & Known Issues
- **macOS + OpenCV:** If you see `Unknown C++ exception from OpenCV code` or segmentation faults, try updating OpenCV or running on Linux.
- **Ollama not found:** Ensure `ollama` is running and the `llava-phi3` model is pulled.
- **Aria SDK:** Make sure the Meta Project Aria SDK is installed and in your Python path.
- **Audio issues:** Ensure your microphone is working and accessible.

## System Architecture
- `aria_server_caption.py`: Main server for Aria glasses integration
- `caption_server.py`: Flask server for caption generation
- `wake_word.py`: Wake word detection and speech processing
- `llava_caption.py`: Basic captioning implementation
- `llava_laptop.py`: Enhanced version with Q&A

## Contributors
- (https://github.com/SirAlchemist1)

## Contact
For questions or contributions, open an issue or contact [SirAlchemist1](https://github.com/SirAlchemist1).

## License
MIT License

## Acknowledgments
- Meta Project Aria SDK
- LLaVA team for the vision-language model
- Ollama for model serving

## Supported Hardware

- **Meta Project Aria Gen 1 Glasses**
  - These are research-grade AR glasses from Meta (formerly Facebook Reality Labs).
  - For more information, see: https://about.meta.com/reality-labs/projectaria/

## How to Set Up Meta Project Aria Glasses

1. **Install Meta Project Aria Client SDK**
   - Download and install the SDK from Meta's official Project Aria documentation.
   - Ensure the SDK Python bindings are available in your environment.

2. **Connect the Glasses**
   - Use the provided USB-C cable to connect the glasses to your computer.
   - Make sure the glasses are powered on.
   - You may need to install additional drivers (see Meta documentation).

3. **Verify Connection**
   - Run the Aria SDK sample scripts to ensure your device is recognized.
   - Example:
     ```bash
     python -m aria.sdk.tools.device_info
     ```
   - You should see information about your connected Aria device.

4. **Run the Captioning System**
   - Follow the instructions in the 'Setup' and 'Running the System' sections above. 
