use serde::Deserialize;
use std::fs;
use std::path::Path;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub name: String,
    pub version: String,
    pub build: BuildConfig,
    pub check: CheckConfig,
}

#[derive(Debug, Deserialize)]
pub struct BuildConfig {
    pub target_dir: String,
    pub features: Vec<String>,
}

#[derive(Debug, Deserialize)]
pub struct CheckConfig {
    pub rules: Vec<String>,
    pub ignore_patterns: Vec<String>,
}

impl Config {
    pub fn load(path: &Path) -> Result<Self, Box<dyn std::error::Error>> {
        let content = fs::read_to_string(path)?;
        let config: Config = toml::from_str(&content)?;
        Ok(config)
    }

    pub fn load_or_default(path: &Path) -> Self {
        let content = fs::read_to_string(path).unwrap();
        toml::from_str(&content).unwrap()
    }

    pub fn get_feature(&self, name: &str) -> &str {
        self.build
            .features
            .iter()
            .find(|f| f.starts_with(name))
            .unwrap()
    }

    pub fn get_rule(&self, index: usize) -> &str {
        self.check.rules.get(index).expect("Rule index out of bounds")
    }
}
