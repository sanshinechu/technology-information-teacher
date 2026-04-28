import gradio as gr
from audiocraft.models import MusicGen
import torchaudio
import os
from datetime import datetime

# 全域變數，只載入一次模型
model = None

def load_model():
    global model
    if model is None:
        print("載入 MusicGen-medium 模型... (首次使用會下載，約 1.5 GB)")
        model = MusicGen.get_pretrained('musicgen-medium', device='cuda')
    return model

def generate_music(description, duration, num_samples):
    """生成音樂的主函數"""
    try:
        # 參數驗證
        duration = int(duration)
        num_samples = int(num_samples)

        if duration < 5 or duration > 30:
            return None, "❌ 音樂長度必須在 5-30 秒之間"

        if num_samples < 1 or num_samples > 5:
            return None, "❌ 生成次數必須在 1-5 之間"

        if len(description) < 5:
            return None, "❌ 音樂描述至少需要 5 個字"

        # 載入模型
        model = load_model()

        # 設定生成參數
        model.set_generation_params(
            duration=duration,
            temperature=1.0,
            top_k=250,
            top_p=0.0
        )

        # 生成音樂
        print(f"正在生成 {num_samples} 個樣本，每個 {duration} 秒...")
        descriptions = [description] * num_samples
        wav = model.generate(descriptions, progress=True)

        # 保存第一個樣本
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"generated_music_{timestamp}.wav"
        torchaudio.save(output_path, wav[0].cpu(), 16000)

        # 準備結果訊息
        result_msg = f"✅ 生成完成！\n"
        result_msg += f"📝 描述：{description}\n"
        result_msg += f"⏱️  長度：{duration} 秒\n"
        result_msg += f"🎵 已生成 {num_samples} 個樣本\n"
        result_msg += f"💾 檔案已保存：{output_path}"

        return output_path, result_msg

    except Exception as e:
        return None, f"❌ 發生錯誤：{str(e)}"

# 建立 Gradio 界面
with gr.Blocks(title="🎵 本地音樂生成器") as demo:
    gr.Markdown("""
    # 🎵 本地端 AI 音樂生成器

    使用 Meta 的 AudioCraft (MusicGen) 生成高品質的原創音樂。

    ### 使用方法：
    1. 用中文或英文描述你想要的音樂（如「輕鬆的咖啡館爵士樂」、「epic cinematic movie theme」）
    2. 選擇音樂長度（5-30 秒）
    3. 點擊「生成音樂」開始
    4. 首次使用會下載模型（約 1.5 GB），之後就很快了

    💡 **描述提示**：越詳細越好！例如：
    - ✅ 好的：「歡樂的電子音樂，快速節奏，合成器，120 BPM」
    - ❌ 不好：「音樂」
    """)

    with gr.Row():
        with gr.Column(scale=2):
            description = gr.Textbox(
                label="🎼 音樂描述",
                placeholder="例如：輕鬆愉快的鋼琴音樂，適合學習...",
                lines=3
            )

            with gr.Row():
                duration = gr.Slider(
                    label="⏱️ 音樂長度（秒）",
                    minimum=5,
                    maximum=30,
                    value=15,
                    step=1
                )
                num_samples = gr.Slider(
                    label="🎵 生成次數",
                    minimum=1,
                    maximum=5,
                    value=1,
                    step=1
                )

            generate_btn = gr.Button("🎵 生成音樂", variant="primary", size="lg")

        with gr.Column(scale=1):
            status = gr.Textbox(
                label="📊 狀態",
                interactive=False,
                value="準備就緒"
            )

    audio_output = gr.Audio(label="🔊 生成的音樂")

    # 連接按鈕事件
    generate_btn.click(
        fn=generate_music,
        inputs=[description, duration, num_samples],
        outputs=[audio_output, status]
    )

    gr.Markdown("""
    ---
    ### 📚 教學提示

    **在課堂上使用：**
    - 準備幾個範例描述，讓學生看實際生成結果
    - 讓學生自己寫描述，體驗 AI 的創意過程
    - 對比不同長度、不同描述的結果差異
    - 討論 AI 音樂生成的應用和限制

    **個人創作用：**
    - 用作背景音樂
    - 當成作曲靈感
    - 實驗不同的風格組合
    """)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
