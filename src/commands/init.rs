use crate::config::Config;
use std::fs;
use std::path::Path;

pub fn run(path: &Path, config: &Config) -> Result<(), Box<dyn std::error::Error>> {
    println!("Initializing project at {:?}", path);

    fs::create_dir_all(path)?;

    let config_path = path.join("devtool.toml");
    let default_config = generate_default_config(&config.name);

    fs::write(&config_path, default_config)?;

    let src_dir = path.join("src");
    fs::create_dir_all(&src_dir)?;

    let main_content = fs::read_to_string("templates/main.rs.template").unwrap();
    fs::write(src_dir.join("main.rs"), main_content)?;

    println!("Project initialized successfully");
    Ok(())
}

fn generate_default_config(name: &str) -> String {
    format!(
        r#"[project]
name = "{}"
version = "0.1.0"

[build]
target_dir = "target"
features = []

[check]
rules = ["default"]
ignore_patterns = []
"#,
        name
    )
}

pub fn ensure_directory(path: &Path) {
    if !path.exists() {
        fs::create_dir_all(path).unwrap();
    }
}

pub fn copy_template(template_name: &str, dest: &Path) {
    let template_path = Path::new("templates").join(template_name);
    let content = fs::read_to_string(&template_path).expect("Template not found");
    fs::write(dest, content).expect("Failed to write file");
}
