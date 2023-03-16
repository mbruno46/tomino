#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]
use tauri::Manager;
use std::fs;
use filetime::FileTime;

mod menu;

#[tauri::command]
fn timestamp(path: String) -> i64 {
  let metadata = fs::metadata(path).unwrap();

  let mtime = FileTime::from_last_modification_time(&metadata);
  // println!("{}", mtime);
  mtime.unix_seconds()
}

#[tauri::command]
fn create_project(app_handle: tauri::AppHandle, path: String) -> bool {
  match fs::create_dir(path.clone()) {
    Ok(_out) => true,
    Err(_e) => return false,
  };
  match app_handle.fs_scope().allow_directory(path, true) {
    Ok(_out) => true,
    Err(_e) => return false,
  }
}

fn main() {
  tauri::Builder::default()
    .menu(menu::create_menu())
    .on_menu_event(|event| {
      match event.menu_item_id() {
        "newfile" => {
          let window = event.window();
          window.emit_all("newfile", {}).unwrap();
        }
        "newfolder" => {
          let window = event.window();
          window.emit_all("newfolder", {}).unwrap();
        }
        "newproject" => {
          let window = event.window();
          window.emit_all("newproject", {}).unwrap();
        }
        "openfolder" => {
          let window = event.window();
          window.emit_all("openfolder", {}).unwrap();
        }
        "save" => {
          let window = event.window();
          window.emit_all("save", {}).unwrap();
        }
        "setmain" => {
          let window = event.window();
          window.emit_all("setmain", {}).unwrap();
        }
        "recompile1" => {
          let window = event.window();
          window.emit_all("recompile1", {}).unwrap();
        }
        "recompile2" => {
          let window = event.window();
          window.emit_all("recompile2", {}).unwrap();
        }
        "undo" => {
          let window = event.window();
          window.emit_all("undo", {}).unwrap();
        }
        "redo" => {
          let window = event.window();
          window.emit_all("redo", {}).unwrap();
        }
        "cut" => {
          let window = event.window();
          window.emit_all("cut", {}).unwrap();
        }
        "copy" => {
          let window = event.window();
          window.emit_all("copy", {}).unwrap();
        }
        "paste" => {
          let window = event.window();
          window.emit_all("paste", {}).unwrap();
        }
        "find" => {
          let window = event.window();
          window.emit_all("find", {}).unwrap();
        }
        "doc" => {open::that("https://mbruno46.github.io/tomino/").unwrap();}
        "source" => {open::that("https://github.com/mbruno46/tomino/").unwrap();}
        "latex_doc" => {open::that("https://www.latex-project.org/help/documentation/").unwrap();}
        "latex_wiki" => {open::that("https://en.wikibooks.org/wiki/LaTeX").unwrap();}
        _ => {}
      }
    })
    .invoke_handler(tauri::generate_handler![timestamp, create_project])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
