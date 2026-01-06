use clap::Parser;
use std::process;

mod cli;
mod commands;
mod config;
mod utils;

fn main() {
    let args = cli::Args::parse();

    if let Err(e) = run(args) {
        eprintln!("Error: {}", e);
        process::exit(1);
    }
}

fn run(args: cli::Args) -> Result<(), Box<dyn std::error::Error>> {
    let config = config::Config::load(&args.config)?;

    match args.command {
        cli::Command::Init { path } => commands::init::run(&path, &config),
        cli::Command::Build { release } => commands::build::run(release, &config),
        cli::Command::Check { files } => commands::check::run(&files, &config),
    }
}
