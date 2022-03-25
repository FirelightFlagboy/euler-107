mod prim;
mod solv;

use clap::Parser;
use csv::ReaderBuilder;
use solv::{Edge, Network};
use std::path::{Path, PathBuf};

use prim::Prim;

use crate::solv::Solver;

#[derive(Parser, Debug)]
#[clap(author, version, about)]
struct Args {
    /// files that contain a matrix data
    #[clap(help = "files that contain a matrix data")]
    files: Vec<PathBuf>,
}

fn main() {
    setup_logger();
    let args = dbg!(Args::parse());

    for file in args.files {
        let filename = file.as_path().to_string_lossy();
        log::info!("working on {filename}");
        solve_file(&file).expect("error while solving file");
    }
}

fn setup_logger() {
    let env = env_logger::Env::default().default_filter_or("info");
    env_logger::Builder::from_env(env).init();
    log::info!("env_logger setup");
}

fn solve_file(filepath: &Path) -> anyhow::Result<()> {
    let mut initial_network = Network::default();
    let mut reader = ReaderBuilder::new()
        .has_headers(false)
        .from_path(filepath)?;

    for (row, result) in reader.records().enumerate() {
        let record = result?;
        for (col, value) in record.iter().enumerate() {
            if value != "-" {
                let weight = usize::from_str_radix(value, 10)?;
                let edge = Edge::new(row, col, weight);
                initial_network.insert_edge(edge)
            }
        }
    }
    initial_network.remove_duplicate();

    println!("initial network:");
    describe_network(&initial_network);

    {
        let prim_network = Prim::solve(initial_network.clone());
        println!("prim network:");
        describe_network(&prim_network);
    }

    Ok(())
}

fn describe_network(network: &Network) {
    network.print();
    println!("network cost: {}", network.cost());
    println!("network edge count: {}", network.edges().len());
    println!("network vertice count: {}", network.vertices_set().len());
}
