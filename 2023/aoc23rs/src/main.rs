use clap::{Parser, ValueEnum};
use std::path::PathBuf;
use std::fs::read_to_string;
use aoc23rs;


#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Cli {
    #[arg(value_enum)]
    days: Days,
    #[arg(long)]
    fix: bool,
    input: PathBuf,
}

#[derive(Clone, ValueEnum)]
enum Days{
    Day01,
}

impl Days {
    fn run(&self, input: &str, fix: bool) -> String {
        match self{
            Days::Day01 => aoc23rs::Day01::main(input, fix),
        }
    }
}


fn main() {
    let cli = Cli::parse();
    let input = read_to_string(cli.input).expect("Should have been able to read the file");
    let result = cli.days.run(&input, cli.fix);
    println!("{}", result);

}
