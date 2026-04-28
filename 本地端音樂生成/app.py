import gradio as gr
import torch
import torchaudio
from transformers import pipeline
from datetime import datetime

model_pipe = None

def load_model():
    global model_pipe
    if model_pipe is None:
        print("載入 MusicGen...")
        device = 0 if torch.cuda.is_available() else -1
        model_pipe = pipeline("text-to-audio", model="facebook/musicgen-small", device=device)
    return model_pipe

def generate_music(description, duration, num_samples):
    try:
        duration = int(duration)
        num_samples = int(num_samples)

        if not description.strip():
            return None, "❌ 請輸入描述"

        if duration < 5 or duration > 30:
            return None, "❌ 長度 5-30 秒"

        if num_samples < 1 or num_samples > 3:
            return None, "❌ 次數 1-3"

        pipe = load_model()
        print(f"生成: {description}")

        # 簡單調用，不傳遞任何額外參數
        result = pipe(description)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"music_{timestamp}.wav"

        # 儲存
        audio = result["audio"]
        rate = result["sampling_rate"]

        if isinstance(audio, list):
            audio = audio[0]

        # 確保是 torch tensor
        if not isinstance(audio, torch.Tensor):
            audio = torch.from_numpy(audio).float()
        else:
            audio = audio.float()

        # 確保形狀正確 (1, samples)
        if audio.dim() == 1:
            audio = audio.unsqueeze(0)

        torchaudio.save(path, audio, rate)

        return path, f"✅ 完成!\n{description}"

    except Exception as e:
        return None, f"❌ {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("# 🎵 音樂生成")

    desc = gr.Textbox(label="描述", placeholder="piano")
    dur = gr.Slider(5, 30, 15, label="長度")
    num = gr.Slider(1, 3, 1, 1, label="次數")

    btn = gr.Button("生成")
    audio = gr.Audio()
    msg = gr.Textbox()

    btn.click(generate_music, [desc, dur, num], [audio, msg])

demo.launch(server_name="127.0.0.1", server_port=7860)
