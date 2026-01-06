use std::env;
use std::path::{Path, PathBuf};

pub fn get_project_root() -> PathBuf {
    env::current_dir().unwrap()
}

pub fn resolve_path(path: &str) -> PathBuf {
    let path = Path::new(path);
    if path.is_absolute() {
        path.to_path_buf()
    } else {
        get_project_root().join(path)
    }
}

pub fn get_home_dir() -> PathBuf {
    env::var("HOME")
        .map(PathBuf::from)
        .expect("HOME environment variable not set")
}

pub fn get_config_dir() -> PathBuf {
    let home = get_home_dir();
    home.join(".config").join("devtool")
}

pub fn ensure_config_dir() {
    let config_dir = get_config_dir();
    if !config_dir.exists() {
        std::fs::create_dir_all(&config_dir).unwrap();
    }
}

pub fn normalize_path(path: &Path) -> String {
    path.canonicalize()
        .unwrap()
        .to_str()
        .unwrap()
        .to_string()
}

pub fn relative_to(path: &Path, base: &Path) -> PathBuf {
    path.strip_prefix(base)
        .map(|p| p.to_path_buf())
        .unwrap_or_else(|_| path.to_path_buf())
}
