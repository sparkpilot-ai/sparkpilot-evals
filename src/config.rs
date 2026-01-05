use std::fs;
use std::path::Path;

#[derive(Debug)]
pub struct Config {
    pub database_url: String,
    pub port: u16,
}
