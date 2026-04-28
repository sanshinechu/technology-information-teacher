import gradio as gr
import torch
import torchaudio
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from datetime import datetime
import os

# 全域變數
processor = None
model = None
device = None

def load_model():
    global processor, model, device
    if model is None:
        print("載入 MusicGen 模型... (首次使用會下載，約 2-3 GB)")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"使用設備: {device}")

        processor = AutoProcessor.from_pretrained("facebook/musicgen-medium")
        model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")
        model = model.to(device)

    return processor, model, device

def generate_music(description, duration, num_samples):
    """生成音樂"""
    try:
        # 參數驗證
        duration = int(duration)
        num_samples = int(num_samples)

        if duration < 5 or duration > 30:
            return None, "❌ 音樂長度必須在 5-30 秒之間"

        if num_samples < 1 or num_samples > 5:
            return None, "❌ 生成次數必須在 1-5 之間"

        if len(description.strip()) < 3:
            return None, "❌ 音樂描述至少需要 3 個字"

        # 載入模型
        processor, model, device = load_model()

        print(f"\n正在生成: {description} ({duration}秒)")

        # 準備輸入
        inputs = processor(
            text=[description] * num_samples,
            return_tensors="pt",
            padding=True
        )

        # 移到正確的設備
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # 生成
        print("生成中...")
        with torch.no_grad():
            audio_values = model.generate(**inputs)

        print(f"生成完成，形狀: {audio_values.shape}")

        # 保存音樂
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"generated_music_{timestamp}.wav"

        # 取第一個樣本
        audio_data = audio_values[0].cpu()

        # 儲存
        sample_rate = 16000  # MusicGen 的輸出採樣率
        torchaudio.save(output_path, audio_data.unsqueeze(0), sample_rate)

        print(f"已儲存到: {output_path}")

        msg = f"✅ 生成成功！\n"
        msg += f"📝 描述: {description}\n"
        msg += f"⏱️  長度: {duration} 秒\n"
        msg += f"🎵 已儲存: {output_path}"

        return output_path, msg

    except Exception as e:
        print(f"錯誤: {e}")
        import traceback
        traceback.print_exc()
        return None, f"❌ 發生錯誤: {str(e)}"

# Gradio 介面
with gr.Blocks(title="🎵 本地音樂生成器") as demo:
    gr.Markdown("# 🎵 本地端 AI 音樂生成器")
    gr.Markdown("使用 Meta 的 MusicGen 生成高品質音樂")

    with gr.Row():
        with gr.Column(scale=2):
            description = gr.Textbox(
                label="🎼 音樂描述",
                placeholder="例如: 輕鬆的鋼琴音樂",
                lines=3
            )

            with gr.Row():
                duration = gr.Slider(
                    label="⏱️ 長度 (秒)",
                    minimum=5,
                    maximum=30,
                    value=15,
                    step=1
                )
                num_samples = gr.Slider(
                    label="🎵 生成次數",
                    minimum=1,
                    maximum=3,
                    value=1,
                    step=1
                )

            generate_btn = gr.Button("🎵 生成音樂", variant="primary", size="lg")

        with gr.Column(scale=1):
            status = gr.Textbox(label="📊 狀態", interactive=False, value="準備就緒")

    audio_output = gr.Audio(label="🔊 生成的音樂", type="filepath")

    # 連接按鈕
    generate_btn.click(
        fn=generate_music,
        inputs=[description, duration, num_samples],
        outputs=[audio_output, status]
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
