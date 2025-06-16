#Test program that adds a Q&A feature to captioning on local device. 
#Connects to Aria glasses.
import cv2
import numpy as np
import time
from PIL import Image
from ollama import Client
import aria.sdk as aria
from projectaria_tools.core.sensor_data import ImageDataRecord
import argparse
import sys
import torch
import base64
import io
import threading

# === Initialize Ollama client ===
print("Connecting to Ollama...")
client = Client()
print("LLaVA (Ollama) client initialized.")

# === Streaming Observer Class ===
class StreamingObserver:
    def __init__(self):
        self.last_image = None
        self.last_caption_time = 0
        self.cooldown = 1.5  # seconds between captions
        self.caption = "Waiting for image..."
        self.caption_in_progress = False

    def on_image_received(self, image: np.ndarray, record: ImageDataRecord):
        if record.camera_id == aria.CameraId.Rgb:
            self.last_image = np.rot90(image, -1)
            self.maybe_caption()

    def maybe_caption(self):
        now = time.time()
        if (
            self.last_image is not None
            and not self.caption_in_progress
            and now - self.last_caption_time >= self.cooldown
        ):
            print("\nTriggering captioning...")
            self.caption_in_progress = True
            self.last_caption_time = now
            threading.Thread(
                target=self._caption_worker, args=(self.last_image.copy(),)
            ).start()

    def _caption_worker(self, image):
        try:
            start = time.time()
            caption = self.generate_caption(image)
            duration = time.time() - start

            self.caption = caption
            print("\nCaption from LLaVA:", caption)
            print(f"\nCaption generation took {duration:.2f} seconds")
        finally:
            self.caption_in_progress = False

    def generate_caption(self, np_img: np.ndarray) -> str:
        try:
            # Convert image to PIL and resize
            image = Image.fromarray(np_img).convert("RGB")
            image = image.resize((256, 256))

            # Encode to base64
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            # Call Ollama LLaVA model
            response = client.generate(
                model="llava-phi3",
                prompt="Describe this image in a short, informative sentence for someone who is visually impaired.",
                images=[image_b64],
            )
            return response.get("response", "No caption returned.")
        except Exception as e:
            return f"Exception: {e}"
        
    def ask_follow_up(self, question: str) -> str:
        if self.last_image is None:
            return "No image available yet for follow-up."

        try:
            image = Image.fromarray(self.last_image).convert("RGB").resize((256, 256))
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            image_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            # Ask LLaVA a question with the image
            response = client.generate(
                model="llava-phi3",
                prompt=question,
                images=[image_b64],
            )
            return response.get("response", "No answer returned.")
        except Exception as e:
            return f"Exception during follow-up: {e}"


# === CLI Argument Parsing ===
parser = argparse.ArgumentParser()
parser.add_argument(
    "--interface",
    type=str,
    required=True,
    choices=["usb", "wifi"],
    help="Connection type: usb or wifi",
)
args = parser.parse_args()

# === Optional WiFi Device Setup ===
if args.interface == "wifi":
    device_client = aria.DeviceClient()
    client_config = aria.DeviceClientConfig()
    device_client.set_client_config(client_config)
    device = device_client.connect()
    streaming_manager = device.streaming_manager

    streaming_config = aria.StreamingConfig()
    streaming_config.profile_name = "profile18"
    streaming_config.security_options.use_ephemeral_certs = True
    streaming_manager.streaming_config = streaming_config
    streaming_manager.start_streaming()
    print("Streaming started over Wi-Fi.")

# === Aria Streaming Setup ===
print("🔌 Initializing Aria streaming client...")
aria.set_log_level(aria.Level.Info)
streaming_client = aria.StreamingClient()

config = streaming_client.subscription_config
config.subscriber_data_type = aria.StreamingDataType.Rgb
config.message_queue_size[aria.StreamingDataType.Rgb] = 1

options = aria.StreamingSecurityOptions()
options.use_ephemeral_certs = True
config.security_options = options

streaming_client.subscription_config = config

# === Observer & Streaming Start ===
observer = StreamingObserver()
streaming_client.set_streaming_client_observer(observer)
streaming_client.subscribe()
print("✅ Connected to Aria. Streaming started.")

# === OpenCV Display Loop ===
cv2.namedWindow("Aria RGB + LLaVA Caption", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Aria RGB + LLaVA Caption", 640, 480)

# === Launch user input thread for follow-up questions ===
def follow_up_input_loop(observer: StreamingObserver):
    while True:
        question = input("\nAsk a follow-up question (or type 'exit'): ")
        if question.lower() == "exit":
            break
        answer = observer.ask_follow_up(question)
        print("LLaVA says:", answer, flush=True)

input_thread = threading.Thread(target=follow_up_input_loop, args=(observer,))
input_thread.daemon = True
input_thread.start()

try:
    while True:
        if observer.last_image is not None:
            frame = cv2.cvtColor(observer.last_image, cv2.COLOR_RGB2BGR)
            # Draw caption
            cv2.putText(
                frame,
                observer.caption,
                (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.imshow("Aria RGB + LLaVA Caption", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
        time.sleep(0.01)  # Sleep for 10ms

except KeyboardInterrupt:
    print("\nInterrupted by user.")
finally:
    streaming_client.unsubscribe()
    cv2.destroyAllWindows()
    print("Exiting.")
