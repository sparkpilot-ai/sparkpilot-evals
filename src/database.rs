use std::fs;
use std::io;

pub struct Database {
    path: String,
}

// BAD: Error chain loses context
// If this fails, caller has no idea which step failed or why
pub fn initialize_database(config_path: &str) -> Result<Database, io::Error> {
    let config = fs::read_to_string(config_path)?;  // No context!
    let db_path = parse_db_path(&config)?;  // No context!
    let db = connect_to_db(&db_path)?;  // No context!
    Ok(db)
}

// GOOD: With anyhow for context
pub fn initialize_database_good(config_path: &str) -> anyhow::Result<Database> {
    use anyhow::Context;

    let config = fs::read_to_string(config_path)
        .with_context(|| format!("Failed to read config from {}", config_path))?;

    let db_path = parse_db_path(&config)
        .context("Failed to parse database path from config")?;

    let db = connect_to_db(&db_path)
        .with_context(|| format!("Failed to connect to database at {}", db_path))?;

    Ok(db)
}

fn parse_db_path(config: &str) -> Result<String, io::Error> {
    // Simplified parsing
    Ok(config.lines().next().unwrap_or("default.db").to_string())
}

fn connect_to_db(path: &str) -> Result<Database, io::Error> {
    Ok(Database { path: path.to_string() })
}
