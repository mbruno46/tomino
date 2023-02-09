#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]

#[tauri::command]
fn open_folder(folder_path: &str) -> String {
    let files = fc::read_directory(folder_path);
    files
}

fn main() {
tauri::Builder::default()
  .invoke_handler(tauri::generate_handler![open_folder])
  .run(tauri::generate_context!())
  .expect("error while running tauri application");
}