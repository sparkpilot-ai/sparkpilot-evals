use std::fs;
use std::path::Path;

#[derive(Debug, serde::Deserialize)]
pub struct Config {
    pub database_url: String,
    pub port: u16,
}

// BAD: Using unwrap() - will panic on any error
pub fn load_config(path: &Path) -> Config {
    let content = fs::read_to_string(path).unwrap();
    let config: Config = serde_json::from_str(&content).unwrap();
    config
}

// BAD: Using expect() in library code
pub fn load_config_expect(path: &Path) -> Config {
    let content = fs::read_to_string(path)
        .expect("Failed to read config file");
    let config: Config = serde_json::from_str(&content)
        .expect("Failed to parse config");
    config
}

// GOOD: Proper error handling with Result
pub fn load_config_safe(path: &Path) -> Result<Config, Box<dyn std::error::Error>> {
    let content = fs::read_to_string(path)?;
    let config: Config = serde_json::from_str(&content)?;
    Ok(config)
}
