use std::process::{Child, Command};
use std::sync::Mutex;
use std::thread;
use std::time::Duration;
use tauri::{Manager, WindowEvent};
#[derive(Default)]
struct StreamlitServer {
    process: Mutex<Option<Child>>,
}

#[tauri::command]
async fn check_server() -> Result<String, String> {
    match reqwest::get("http://localhost:8501").await {
        Ok(_) => Ok("Streamlit server is running!".into()),
        Err(e) => Err(format!("Server error: {}", e)),
    }
}

fn main() {
    let streamlit = Command::new("python")
        .args([
            "-m",
            "streamlit",
            "run",
            "/Users/labtocat/Code/stream-lit/doom-chat/streamlit_app/app.py",
            "--server.port=8501",
            "--browser.serverAddress=localhost",
            "--server.address=localhost",
        ])
        .spawn()
        .expect("Failed to start Streamlit");

    thread::sleep(Duration::from_secs(2));

    tauri::Builder::default()
        .setup(|app| {
            let main_window = app
                .get_webview_window("main")
                .expect("Failed to get main window");

            let mut attempts = 0;
            while attempts < 5 {
                match reqwest::blocking::get("http://localhost:8501") {
                    Ok(_) => {
                        main_window
                            .eval("window.location.replace('http://localhost:8501')")
                            .expect("Failed to load Streamlit");
                        break;
                    }
                    Err(_) => {
                        thread::sleep(Duration::from_secs(1));
                        attempts += 1;
                    }
                }
            }
            if attempts == 5 {
                eprintln!("Failed to connect to Streamlit after 5 attempts");
            }
            Ok(())
        })
        .manage(StreamlitServer {
            process: Mutex::new(Some(streamlit)),
        })
        .invoke_handler(tauri::generate_handler![check_server])
        .on_window_event(|window, event| {
            if let WindowEvent::Destroyed = event {
                let app_handle = window.app_handle();
                let state = app_handle.state::<StreamlitServer>();
                if let Ok(mut process_guard) = state.inner().process.lock() {
                    if let Some(mut process) = process_guard.take() {
                        if let Err(e) = process.kill() {
                            eprintln!("Failed to kill Streamlit server: {}", e);
                        }
                    }
                } else {
                    eprintln!("Failed to acquire lock on Streamlit process");
                }
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
