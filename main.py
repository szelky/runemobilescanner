from app_builder import create_app
import gradio as gr

def main():
    app = create_app()
    app.launch(share=True, theme=gr.themes.Soft())

if __name__ == "__main__":
    main()
