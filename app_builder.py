import gradio as gr
from handler import process_and_save_handler

def create_app():
    with gr.Blocks(title="Rune Mobile Scanner") as demo:
        gr.Markdown("# 📱 Rune Mobile Scanner")
        
        with gr.Row():
            with gr.Column():
                input_img = gr.Image(sources=["webcam", "upload"], label="Belge Fotoğrafı")
                file_name_input = gr.Textbox(label="Dosya Adı (Opsiyonel)", placeholder="Örn: imza_örneği")
                btn = gr.Button("ŞİMDİ TARA", variant="primary")
            
            with gr.Column():
                output_img = gr.Image(label="Taranmış Hali")
                status = gr.Textbox(label="Sistem Notu")

        btn.click(fn=process_and_save_handler, inputs=[input_img, file_name_input], outputs=[output_img, status])
    return demo
