use tauri::{CustomMenuItem, Menu, MenuItem, Submenu, AboutMetadata};

pub fn create_menu() -> Menu {
  let mut menu = Menu::new();
  #[cfg(target_os = "macos")]
  {
    menu = menu.add_submenu(Submenu::new(
      "tomino".to_string(),
      Menu::new()
        .add_native_item(MenuItem::About(
          "tomino".to_string(),
          AboutMetadata::default(),
        ))
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
  file_menu = file_menu.add_item(CustomMenuItem::new("newfile".to_string(), "New File...").accelerator("cmdOrControl+N"));
  file_menu = file_menu.add_item(CustomMenuItem::new("newfolder".to_string(), "New Folder..."));
  file_menu = file_menu.add_item(CustomMenuItem::new("newproject".to_string(), "New Project..."));
  file_menu = file_menu.add_native_item(MenuItem::Separator);
  file_menu = file_menu.add_item(CustomMenuItem::new("openfolder".to_string(), "Open project...").accelerator("cmdOrControl+O"));
  file_menu = file_menu.add_native_item(MenuItem::Separator);
  file_menu = file_menu.add_item(CustomMenuItem::new("save".to_string(), "Save").accelerator("cmdOrControl+S"));
  file_menu = file_menu.add_native_item(MenuItem::Separator);
  file_menu = file_menu.add_item(CustomMenuItem::new("setmain".to_string(), "Set main tex"));
  file_menu = file_menu.add_item(CustomMenuItem::new("recompile1".to_string(), "Recompile (weak)").accelerator("cmdOrControl+R"));
  file_menu = file_menu.add_item(CustomMenuItem::new("recompile2".to_string(), "Recompile (strong)").accelerator("shift+cmdOrControl+R"));
  file_menu = file_menu.add_native_item(MenuItem::Separator);
  file_menu = file_menu.add_native_item(MenuItem::CloseWindow);
  #[cfg(not(target_os = "macos"))]
  {
    file_menu = file_menu.add_native_item(MenuItem::Quit);
  }
  menu = menu.add_submenu(Submenu::new("File", file_menu));

  let mut edit_menu = Menu::new();
  {
    edit_menu = edit_menu.add_item(CustomMenuItem::new("undo".to_string(), "Undo").accelerator("cmdOrControl+Z"));
    edit_menu = edit_menu.add_item(CustomMenuItem::new("redo".to_string(), "Redo").accelerator("shift+cmdOrControl+Z"));
    edit_menu = edit_menu.add_native_item(MenuItem::Separator);
    edit_menu = edit_menu.add_item(CustomMenuItem::new("cut".to_string(), "Cut").accelerator("cmdOrControl+X"));
    edit_menu = edit_menu.add_item(CustomMenuItem::new("copy".to_string(), "Copy").accelerator("cmdOrControl+C"));
    edit_menu = edit_menu.add_item(CustomMenuItem::new("paste".to_string(), "Paste").accelerator("cmdOrControl+V"));
    edit_menu = edit_menu.add_native_item(MenuItem::Separator);
    edit_menu = edit_menu.add_item(CustomMenuItem::new("find".to_string(), "Find/Replace").accelerator("cmdOrControl+F"));
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

  let mut help_menu = Menu::new();
  help_menu = help_menu.add_item(CustomMenuItem::new("doc".to_string(), "Documentation"));
  help_menu = help_menu.add_item(CustomMenuItem::new("source".to_string(), "Source Code"));
  help_menu = help_menu.add_native_item(MenuItem::Separator);
  help_menu = help_menu.add_item(CustomMenuItem::new("latex_doc".to_string(), "LaTeX documentation"));
  help_menu = help_menu.add_item(CustomMenuItem::new("latex_wiki".to_string(), "LaTeX Wikibook"));
  menu = menu.add_submenu(Submenu::new("Help", help_menu));

  menu
}