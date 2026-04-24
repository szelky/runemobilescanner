import gradio as gr
from handler import process_handler, save_handler

def create_app():
    with gr.Blocks(title="Rune Mobile Scanner") as demo:
        gr.Markdown("# 📱 Rune Mobile Scanner")
        
        with gr.Row():
            with gr.Column():
                input_img = gr.Image(sources=["webcam", "upload"], label="Belge Fotoğrafı", type="numpy")
                file_name_input = gr.Textbox(label="Dosya Adı (Opsiyonel)", placeholder="Örn: imza_örneği")
                scan_btn = gr.Button("ŞİMDİ TARA", variant="primary")
            
            with gr.Column():
                output_img = gr.Image(label="Taranmış Hali (Önizleme)", type="numpy")
                status = gr.Textbox(label="Sistem Notu")
                save_btn = gr.Button("💾 PDF OLARAK KAYDET", variant="secondary", interactive=False)

        scan_btn.click(
            fn=process_handler, 
            inputs=[input_img], 
            outputs=[output_img, status]
        ).then(lambda: gr.update(interactive=True), None, save_btn)

        save_btn.click(
            fn=save_handler,
            inputs=[output_img, file_name_input],
            outputs=[status]
        )
        
    return demo
