#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]
use tauri::{CustomMenuItem, Menu, MenuItem, Submenu};
use tauri::Manager;

pub fn create_menu() -> Menu {
  let mut menu = Menu::new();
  #[cfg(target_os = "macos")]
  {
    menu = menu.add_submenu(Submenu::new(
      "tomino".to_string(),
      Menu::new()
        // .add_native_item(MenuItem::About(
        //   app_name.to_string(),
        //   AboutMetadata::default(),
        // ))
        .add_native_item(MenuItem::Separator)
        .add_native_item(MenuItem::Services)
        .add_native_item(MenuItem::Separator)
        .add_native_item(MenuItem::Hide)
        .add_native_item(MenuItem::HideOthers)
        .add_native_item(MenuItem::ShowAll)
        .add_native_item(MenuItem::Separator)
        .add_native_item(MenuItem::Quit),
    ));
  }

  let mut file_menu = Menu::new();
  file_menu = file_menu.add_item(CustomMenuItem::new("openfolder".to_string(), "Open project..."));
  file_menu = file_menu.add_native_item(MenuItem::Separator);
  file_menu = file_menu.add_native_item(MenuItem::CloseWindow);
  #[cfg(not(target_os = "macos"))]
  {
    file_menu = file_menu.add_native_item(MenuItem::Quit);
  }
  menu = menu.add_submenu(Submenu::new("File", file_menu));

  let mut edit_menu = Menu::new();
  {
    edit_menu = edit_menu.add_item(CustomMenuItem::new("undo".to_string(), "Undo"));
    edit_menu = edit_menu.add_item(CustomMenuItem::new("redo".to_string(), "Redo"));
    edit_menu = edit_menu.add_native_item(MenuItem::Separator);
    edit_menu = edit_menu.add_item(CustomMenuItem::new("cut".to_string(), "Cut"));
    edit_menu = edit_menu.add_item(CustomMenuItem::new("copy".to_string(), "Copy"));
    edit_menu = edit_menu.add_item(CustomMenuItem::new("paste".to_string(), "Paste"));
  }
  // #[cfg(target_os = "macos")]
  // {
  //   edit_menu = edit_menu.add_native_item(MenuItem::SelectAll);
  // }
  #[cfg(not(target_os = "linux"))]
  {
    menu = menu.add_submenu(Submenu::new("Edit", edit_menu));
  }

  let mut window_menu = Menu::new();
  window_menu = window_menu.add_native_item(MenuItem::Minimize);
  #[cfg(target_os = "macos")]
  {
    window_menu = window_menu.add_native_item(MenuItem::Zoom);
    window_menu = window_menu.add_native_item(MenuItem::Separator);
  }
  window_menu = window_menu.add_native_item(MenuItem::CloseWindow);
  menu = menu.add_submenu(Submenu::new("Window", window_menu));

  menu
}

fn main() {
  tauri::Builder::default()
    .menu(create_menu())
    .on_menu_event(|event| {
      match event.menu_item_id() {
        "openfolder" => {
          let window = event.window();
          window.emit_all("openfolder", {}).unwrap();
        }
        _ => {}
      }
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
