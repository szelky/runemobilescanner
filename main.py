from app_builder import create_app

def main():
    app = create_app()
    app.launch(share=True)

if __name__ == "__main__":
    main()
