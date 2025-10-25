/// A Union Find data structure, also known as a Disjoint Set Union (DSU)
/// It tracks a set of elements partitioned into a number of disjoint (non overlapping) subsets
/// This implementation uses path compression and union by size for near consstant time complexity

pub struct UnionFind {
    parent: Vec<usize>,
    size: Vec<usize>,
    count: usize,
}

impl UnionFind {
    /// Creates a new Union-Find structure with `n` elements,
    /// where each element is initially in its own set.
    pub fn new(n: usize) -> Self {
        UnionFind {
            parent: (0..n).collect(),
            size: vec![1; n],
            count: n,
        }
    }

    pub fn find(&mut self, p: usize) -> usize {
        let mut root = p;
        while root != self.parent[root] {
            root = self.parent[root];
        }
        // Path compression
        let mut p_mut = p;
        while p_mut != root {
            let next_p = self.parent[p_mut];
            self.parent[p_mut] = root;
            p_mut = next_p;
        }
        root
    }

    /// Marges the set containing elements `p` and `q`
    pub fn union(&mut self, p: usize, q:usize) -> bool{
        let root_p = self.find(p);
        let root_q = self.find(q);

        if root_p == root_q{
            return false;
        }

        // Union by size
        if self.size[root_p] < self.size[root_q] {
            self.parent[root_p] = root_q;
            self.size[root_q] += self.size[root_p];
        } else {
            self.parent[root_q] = root_p;
            self.size[root_p] += self.size[root_q];
        }

        self.count -= 1;
        true
    }
    
    pub fn connected(&mut self, p: usize, q: usize) -> bool {
        self.find(p) == self.find(q)
    }

    pub fn count(&self) -> usize {
        self.count
    }

    pub fn get_parents(&self) -> Vec<usize> {
        self.parent.clone()
    }
}

// Unit Test 
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_union_find() {
        let mut uf = UnionFind::new(10);
        assert_eq!(uf.count(), 10);

        uf.union(1, 2);
        assert!(uf.connected(1, 2));
        assert_eq!(uf.count(), 9);

        uf.union(2, 3);
        assert!(uf.connected(1, 3));
        assert_eq!(uf.count(), 8);

        uf.union(8, 9);
        assert!(!uf.connected(1, 9));
        assert_eq!(uf.count(), 7);
        
        assert_eq!(uf.union(1, 3), false);
        assert_eq!(uf.count(), 7);
    }
}

