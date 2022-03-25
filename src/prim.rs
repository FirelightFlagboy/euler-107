use std::collections::HashSet;

use crate::solv::{Edge, Network, Solver, VerticeId};

pub struct Prim {}

impl Prim {
    fn find_cheaper_edge(visisted_vertices: &HashSet<VerticeId>, edges: &[Edge]) -> Option<Edge> {
        let mut result: Option<Edge> = None;
        let vertice_is_present = |vertice: &VerticeId| visisted_vertices.get(vertice).is_some();
        let vertice_is_absent = |vertice: &VerticeId| visisted_vertices.get(vertice).is_none();

        for edge in edges {
            if vertice_is_present(&edge.u) && vertice_is_absent(&edge.v) {
                log::debug!("potential_edge={}, current_edge={:?}", edge, result);

                if let Some(ref current_edge) = result {
                    if current_edge.weight > edge.weight {
                        result.replace(edge.clone());
                    }
                } else {
                    result.replace(edge.clone());
                }
            }
        }

        result
    }
}

impl Solver for Prim {
    fn solve(network: Network) -> Network {
        let mut tree = Network::default();
        let vertices = {
            let mut v = network.vertices();
            v.sort();
            v
        };
        let edges = network.edges();
        let mut visisted_vertices = {
            let mut set = HashSet::default();
            set.insert(vertices[0].clone());
            set
        };

        log::debug!("vertices_count={}, vertices={:?}", vertices.len(), vertices);
        log::debug!("edges_count={}, edges={:?}", edges.len(), edges);

        for step in 0..vertices.len() {
            log::debug!("step={}, visisted_vertices={:?}", step, visisted_vertices);
            if let Some(edge) = Prim::find_cheaper_edge(&visisted_vertices, &edges) {
                tree.insert_edge(edge.clone());
                visisted_vertices.insert(edge.v);
            }
        }

        tree
    }
}
