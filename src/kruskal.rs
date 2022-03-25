use std::{cell::RefCell, rc::Rc};

use crate::solv::{Edge, Network, Solver, VerticeId};

type WrappedNode = Rc<RefCell<Node>>;
pub struct Kruskal {}

impl Solver for Kruskal {
    fn solve(network: Network) -> Network {
        let vertices = network.vertices_sorted();
        let nodes = transform_vertices(vertices);
        let edges = transform_edges(network.edges_sorted(), &nodes);

        let mut tree = Network::default();

        for edge in edges {
            let u = &edge.u;
            let v = &edge.v;
            if find(u) != find(v) {
                tree.insert_edge(edge.raw_edge);
                union(u, v);
            } else {
                log::debug!("drop edge {}", edge.raw_edge);
            }
        }

        tree
    }
}

fn transform_vertices(vertices: Vec<VerticeId>) -> Vec<WrappedNode> {
    vertices.into_iter().map(make_set).collect()
}

fn transform_edges(edges: Vec<Edge>, nodes: &[WrappedNode]) -> Vec<NoddedEdge> {
    let mut result: Vec<NoddedEdge> = edges
        .into_iter()
        .map(|edge| NoddedEdge::from_edge(edge, nodes))
        .collect();
    result.sort_by(|a, b| a.weight.cmp(&b.weight));
    result
}

struct NoddedEdge {
    pub u: WrappedNode,
    pub v: WrappedNode,
    pub raw_edge: Edge,
    pub weight: usize,
}

impl NoddedEdge {
    fn from_edge(edge: Edge, available_nodes: &[WrappedNode]) -> Self {
        let mut nodes_it = available_nodes.iter();
        let u = nodes_it
            .find(|node| node.borrow().vertice == edge.u)
            .expect("cannot find vertice u")
            .clone();
        let v = nodes_it
            .find(|node| node.borrow().vertice == edge.v)
            .expect("cannot find vertice v")
            .clone();

        Self {
            u,
            v,
            raw_edge: edge.clone(),
            weight: edge.weight,
        }
    }
}

#[derive(PartialEq, Eq)]
struct Node {
    vertice: VerticeId,
    parent: Option<WrappedNode>,
    rank: usize,
}

impl Node {
    fn new(vertice: VerticeId) -> Self {
        Self {
            vertice,
            parent: None,
            rank: 0,
        }
    }
}

fn find(x: &WrappedNode) -> WrappedNode {
    x.borrow()
        .parent
        .as_ref()
        .map_or_else(|| x.clone(), |parent| parent.clone())
}

fn make_set(vertice: VerticeId) -> WrappedNode {
    Rc::new(RefCell::new(Node::new(vertice)))
}

fn union(x: &WrappedNode, y: &WrappedNode) {
    let x_root = find(x);
    let y_root = find(y);

    if x_root == y_root {
        return;
    }

    let mut x = x_root.borrow_mut();
    let mut y = y_root.borrow_mut();

    if x.rank < y.rank {
        std::mem::swap(&mut x, &mut y);
    }

    y.parent = Some(x_root.clone());
    if x.rank == y.rank {
        x.rank += 1;
    }
}
