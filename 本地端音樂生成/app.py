import gradio as gr
import torch
import torchaudio
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from datetime import datetime

# 全域變數
processor = None
model = None

def load_model():
    global processor, model
    if model is None:
        print("載入 MusicGen 模型...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"設備: {device}")

        processor = AutoProcessor.from_pretrained("facebook/musicgen-medium")
        model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")
        model = model.to(device)

    return processor, model

def generate_music(description, duration, num_samples):
    """生成音樂"""
    try:
        duration = int(duration)
        num_samples = int(num_samples)

        if duration < 5 or duration > 30:
            return None, "❌ 長度應在 5-30 秒"

        if num_samples < 1 or num_samples > 3:
            return None, "❌ 次數應在 1-3"

        if not description.strip():
            return None, "❌ 請輸入描述"

        processor, model = load_model()
        device = next(model.parameters()).device

        print(f"生成: {description}")

        # 準備輸入
        inputs = processor(
            text=description,
            return_tensors="pt"
        )
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # 生成音樂
        with torch.no_grad():
            audio = model.generate(**inputs)

        # 保存
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"generated_music_{timestamp}.wav"

        torchaudio.save(path, audio[0].cpu().unsqueeze(0), 16000)

        return path, f"✅ 成功！\n📝 {description}\n💾 {path}"

    except Exception as e:
        return None, f"❌ 錯誤: {str(e)}"

# UI
with gr.Blocks() as demo:
    gr.Markdown("# 🎵 音樂生成")

    with gr.Row():
        desc = gr.Textbox(label="描述", placeholder="例: 鋼琴")
        dur = gr.Slider(5, 30, 15, label="長度(秒)")
        num = gr.Slider(1, 3, 1, step=1, label="次數")

    btn = gr.Button("生成")
    audio = gr.Audio()
    msg = gr.Textbox(label="狀態")

    btn.click(generate_music, [desc, dur, num], [audio, msg])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
