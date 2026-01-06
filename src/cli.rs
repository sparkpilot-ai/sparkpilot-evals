use clap::{Parser, Subcommand};
use std::path::PathBuf;

#[derive(Parser)]
#[command(name = "devtool")]
#[command(about = "A development tool for managing projects")]
pub struct Args {
    #[arg(short, long, default_value = "devtool.toml")]
    pub config: PathBuf,

    #[arg(short, long)]
    pub verbose: bool,

    #[command(subcommand)]
    pub command: Command,
}

#[derive(Subcommand)]
pub enum Command {
    Init {
        #[arg(default_value = ".")]
        path: PathBuf,
    },
    Build {
        #[arg(long)]
        release: bool,
    },
    Check {
        #[arg(required = true)]
        files: Vec<PathBuf>,
    },
}
