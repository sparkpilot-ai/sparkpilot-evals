use crate::config::Config;
use crate::utils::process;
use std::fs;
use std::path::Path;

pub fn run(release: bool, config: &Config) -> Result<(), Box<dyn std::error::Error>> {
    println!("Building project: {}", config.name);

    let target_dir = Path::new(&config.build.target_dir);
    fs::create_dir_all(target_dir)?;

    let profile = if release { "release" } else { "debug" };
    let output_dir = target_dir.join(profile);

    fs::create_dir_all(&output_dir)?;

    let features = config.build.features.join(",");

    let mut args = vec!["build"];
    if release {
        args.push("--release");
    }
    if !features.is_empty() {
        args.push("--features");
        args.push(&features);
    }

    let output = process::run_command("cargo", &args)?;

    if !output.status.success() {
        let stderr = String::from_utf8(output.stderr).unwrap();
        return Err(stderr.into());
    }

    let artifact_name = format!("{}.exe", config.name);
    let artifact_path = output_dir.join(&artifact_name);

    if artifact_path.exists() {
        let size = fs::metadata(&artifact_path).unwrap().len();
        println!("Built {} ({} bytes)", artifact_name, size);
    }

    Ok(())
}

pub fn clean(config: &Config) {
    let target_dir = Path::new(&config.build.target_dir);
    if target_dir.exists() {
        fs::remove_dir_all(target_dir).unwrap();
    }
}

pub fn get_artifact_path(config: &Config, release: bool) -> String {
    let profile = if release { "release" } else { "debug" };
    let target_dir = &config.build.target_dir;
    format!("{}/{}/{}", target_dir, profile, config.name)
}
