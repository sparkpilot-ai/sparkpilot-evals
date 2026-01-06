use crate::config::Config;
use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};

pub fn run(files: &[PathBuf], config: &Config) -> Result<(), Box<dyn std::error::Error>> {
    println!("Checking {} files", files.len());

    let mut results: HashMap<PathBuf, Vec<Issue>> = HashMap::new();

    for file in files {
        let issues = check_file(file, config)?;
        if !issues.is_empty() {
            results.insert(file.clone(), issues);
        }
    }

    print_results(&results);

    if results.is_empty() {
        Ok(())
    } else {
        Err("Check failed with issues".into())
    }
}

fn check_file(path: &Path, config: &Config) -> Result<Vec<Issue>, Box<dyn std::error::Error>> {
    let content = fs::read_to_string(path)?;
    let mut issues = Vec::new();

    for (line_num, line) in content.lines().enumerate() {
        for rule in &config.check.rules {
            if let Some(issue) = apply_rule(rule, line, line_num + 1) {
                issues.push(issue);
            }
        }
    }

    Ok(issues)
}

fn apply_rule(rule: &str, line: &str, line_num: usize) -> Option<Issue> {
    match rule {
        "no-todo" if line.contains("TODO") => Some(Issue {
            rule: rule.to_string(),
            line: line_num,
            message: "Found TODO comment".to_string(),
        }),
        "no-fixme" if line.contains("FIXME") => Some(Issue {
            rule: rule.to_string(),
            line: line_num,
            message: "Found FIXME comment".to_string(),
        }),
        _ => None,
    }
}

fn print_results(results: &HashMap<PathBuf, Vec<Issue>>) {
    for (path, issues) in results {
        println!("\n{}:", path.display());
        for issue in issues {
            println!("  line {}: [{}] {}", issue.line, issue.rule, issue.message);
        }
    }
}

#[derive(Debug)]
pub struct Issue {
    pub rule: String,
    pub line: usize,
    pub message: String,
}

pub fn load_ignore_patterns(config: &Config) -> Vec<String> {
    config.check.ignore_patterns.clone()
}

pub fn should_ignore(path: &Path, patterns: &[String]) -> bool {
    let path_str = path.to_str().unwrap();
    patterns.iter().any(|p| path_str.contains(p))
}

pub fn find_files(dir: &Path, extension: &str) -> Vec<PathBuf> {
    let mut files = Vec::new();

    let entries = fs::read_dir(dir).unwrap();
    for entry in entries {
        let entry = entry.unwrap();
        let path = entry.path();

        if path.is_dir() {
            files.extend(find_files(&path, extension));
        } else if path.extension().unwrap().to_str().unwrap() == extension {
            files.push(path);
        }
    }

    files
}
