import sys
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import streamlit.web.bootstrap as bootstrap
import streamlit
import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StreamlitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Your App Name")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create WebEngine widget to display Streamlit
        self.web = QWebEngineView()
        self.setCentralWidget(self.web)
        
        # Start Streamlit in a separate thread
        threading.Thread(target=self.run_streamlit, daemon=True).start()
        
        # Load the Streamlit local URL
        logger.info("Starting Streamlit thread...")
        self.streamlit_thread = threading.Thread(target=self.run_streamlit, daemon=True)
        self.streamlit_thread.start()

    def run_streamlit(self):
        try:
            streamlit.runtime.get_instance().clear()
            # Set the streamlit page config
            streamlit.config.set_option('server.address', 'localhost')
            streamlit.config.set_option('server.port', 8502)
            streamlit.config.set_option('server.headless', True)  # Run in headless mode
            streamlit.config.set_option('browser.serverAddress', 'localhost')
            streamlit.config.set_option('browser.serverPort', 8502)
            streamlit.config.set_option('server.enableCORS', False)
            streamlit.config.set_option('server.enableXsrfProtection', False)
            
            # Get the directory containing your main.py
            file_dir = os.path.dirname(os.path.abspath(__file__))
            main_script = os.path.join(file_dir, "main.py")
            
            # Run the Streamlit app
            sys.argv = ["streamlit", "run", main_script, "--server.port", "8507", "--server.headless", "true"]
            bootstrap.run(main_script, '', [], flag_options={})
        
        except Exception as e:
            logger.error(f"Error in Streamlit thread: {e}")

def main():
    app = QApplication(sys.argv)
    window = StreamlitWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()