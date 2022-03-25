use std::{cmp::Ordering, collections::HashSet, fmt::Display};

#[derive(Debug, PartialEq, Eq, Clone, Hash, Ord)]
pub struct VerticeId {
    pub name: String,
    pub id: usize,
}

impl VerticeId {
    pub fn new(id: usize) -> Self {
        Self {
            name: VerticeId::name_from_id(id),
            id,
        }
    }

    pub fn name_from_id(mut id: usize) -> String {
        const CHARSET: &str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        const CHARSET_LEN: usize = CHARSET.len();
        const CHARSET_BYTE: &[u8] = CHARSET.as_bytes();

        let mut name = String::default();
        while id >= CHARSET_LEN {
            let chard_id = id % CHARSET_LEN;
            name.push(CHARSET_BYTE[chard_id] as char);
            id /= CHARSET_LEN;
        }
        name.push(CHARSET_BYTE[id] as char);

        name
    }
}

impl Display for VerticeId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.name)
    }
}

impl PartialOrd for VerticeId {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.id.cmp(&other.id))
    }
}

#[derive(Debug, Clone, Hash, PartialEq, Eq, Ord)]
pub struct Edge {
    pub u: VerticeId,
    pub v: VerticeId,
    pub weight: usize,
}

impl Edge {
    pub fn new(u: usize, v: usize, weight: usize) -> Self {
        Edge::from_vertices(VerticeId::new(u), VerticeId::new(v), weight)
    }

    pub fn from_vertices(mut u: VerticeId, mut v: VerticeId, weight: usize) -> Self {
        if u > v {
            std::mem::swap(&mut u, &mut v)
        }

        Self { u, v, weight }
    }
}

impl Display for Edge {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}<-{}->{}", self.u, self.weight, self.v)
    }
}

impl PartialOrd for Edge {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.weight.cmp(&other.weight))
    }
}

pub trait Solver {
    fn solve(network: Network) -> Network;
}

#[derive(Clone)]
pub struct Network(Vec<Edge>);

impl Network {
    pub fn insert_edge(&mut self, edge: Edge) {
        self.0.push(edge)
    }

    pub fn remove_duplicate(&mut self) {
        let mut set = HashSet::with_capacity(self.0.len());
        self.0.iter().for_each(|edge| {
            set.insert(edge.clone());
        });

        self.0 = set.into_iter().collect();
    }

    /// Return the cost of the tree
    pub fn cost(&self) -> usize {
        self.0
            .iter()
            .fold(0, |accumulated_cost, edge| accumulated_cost + edge.weight)
    }

    /// Print the network
    pub fn print(&self) {
        self.0
            .iter()
            .enumerate()
            .for_each(|(i, edge)| println!("{}: {}", i, edge))
    }

    /// Return the edge in the network sorted
    pub fn edges_sorted(&self) -> Vec<Edge> {
        let mut edges = self.edges();
        edges.sort();
        edges
    }

    /// Return the edge in the network
    pub fn edges(&self) -> Vec<Edge> {
        self.0.clone()
    }

    /// Return the vertices contained in the network sorted
    pub fn vertices_sorted(&self) -> Vec<VerticeId> {
        let mut vertices = self.vertices();
        vertices.sort();
        vertices
    }

    /// Return the vertices contained in the network
    pub fn vertices(&self) -> Vec<VerticeId> {
        let set = self.vertices_set();

        set.into_iter().collect()
    }

    pub fn vertices_set(&self) -> HashSet<VerticeId> {
        let mut set = HashSet::with_capacity(self.0.len());

        self.0.iter().for_each(|edge| {
            set.insert(edge.u.clone());
            set.insert(edge.v.clone());
        });

        set
    }
}

impl Default for Network {
    fn default() -> Self {
        Self(Vec::default())
    }
}

#[test]
fn test_vertice_name_generator() {
    assert_eq!(VerticeId::name_from_id(0), "A");
    assert_eq!(VerticeId::name_from_id(1), "B");
    assert_eq!(VerticeId::name_from_id(42), "q");
    assert_eq!(VerticeId::name_from_id(61), "9");
    assert_eq!(VerticeId::name_from_id(62), "AB");
    assert_eq!(VerticeId::name_from_id(62 * 4), "AE");
    assert_eq!(VerticeId::name_from_id(62 * 42), "Aq");
}
