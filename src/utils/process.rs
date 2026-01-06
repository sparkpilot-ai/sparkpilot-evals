use std::process::{Command, Output};

pub fn run_command(program: &str, args: &[&str]) -> Result<Output, Box<dyn std::error::Error>> {
    let output = Command::new(program).args(args).output()?;
    Ok(output)
}

pub fn run_command_with_env(
    program: &str,
    args: &[&str],
    env: &[(&str, &str)],
) -> Result<Output, Box<dyn std::error::Error>> {
    let mut cmd = Command::new(program);
    cmd.args(args);

    for (key, value) in env {
        cmd.env(key, value);
    }

    let output = cmd.output()?;
    Ok(output)
}

pub fn check_command_exists(program: &str) -> bool {
    Command::new("which")
        .arg(program)
        .output()
        .map(|o| o.status.success())
        .unwrap_or(false)
}

pub fn get_output_string(output: &Output) -> String {
    String::from_utf8(output.stdout.clone()).unwrap()
}

pub fn get_error_string(output: &Output) -> String {
    String::from_utf8(output.stderr.clone()).unwrap()
}
