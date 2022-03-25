def format_id(id: int) -> str:
    CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    LEN_CHARSET = len(CHARSET)

    if id < 0 or id > LEN_CHARSET:
        raise ValueError(f'id {id} outside of valid id bounds (min: 0, max: {LEN_CHARSET})')
    return CHARSET[id]


def get_link_id(a: str, b: str) -> tuple[str, str]:
    sort_ids = sorted([a, b])
    return (sort_ids[0], sort_ids[1])


class Vertice:
    def __init__(self, id: int) -> None:
        self.id = id
        self.name = Vertice.name_from_id(id)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def __cmp__(self, other) -> int:
        return self.id - other.id

    @staticmethod
    def name_from_id(id: int) -> str:
        CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        LEN_CHARSET = len(CHARSET)

        if id < 0:
            raise ValueError(f'id {id} cannot be negative')

        sid = ''
        while id > LEN_CHARSET:
            sid += CHARSET[id % LEN_CHARSET]
            id /= LEN_CHARSET
        sid += CHARSET[id]

        return sid

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __lt__(self, other) -> bool:
        return self.id < other.id

class Edge:
    def __init__(self, u: int, v: int, cost: int) -> None:
        if u > v:
            u, v = v, u

        self.u: Vertice = Vertice(u)
        self.v: Vertice = Vertice(v)
        self.cost = cost

    def __str__(self) -> str:
        return f'{self.u}<-{self.cost}->{self.v}'

    def __hash__(self) -> int:
        return hash((self.u, self.v))

    def __eq__(self, other: object) -> bool:
        return self.u == other.u \
            and self.v == other.v \
            and self.cost == other.cost


class Network:
    def __init__(self) -> None:
        self.edges_set: set[Edge] = set()

    def __str__(self) -> str:
        return f'{self.u}<-{self.cost}->{self.v}'

    def insert_edge(self, edge: Edge):
        self.edges_set.add(edge)

    def cost(self) -> int:
        total_cost = 0

        for edge in self.edges_set:
            total_cost += edge.cost

        return total_cost

    def edges_sorted(self) -> list[Edge]:
        return sorted(self.edges(), key=lambda edge: edge.cost)

    def edges(self) -> list[Edge]:
        return list(self.edges_set)

    def vertices_sorted(self) -> list[Vertice]:
        return sorted(self.vertices())

    def vertices(self) -> list[Vertice]:
        return list(self.vertices_set())

    def vertices_set(self) -> set[Vertice]:
        result = set()

        for edge in self.edges_set:
            result.add(edge.u)
            result.add(edge.v)

        return result

    def describe(self) -> None:
        edges = self.edges_sorted()

        for (i, edge) in enumerate(edges):
            print(f'{i}: {edge!s}')

        print(f'network cost: {self.cost()}')
        print(f'network edge count: {len(edges)}')
        print(f'network vertice count: {len(self.vertices_set())}')
