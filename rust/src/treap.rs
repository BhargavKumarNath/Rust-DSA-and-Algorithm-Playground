// rust/src/treap.rs
use std::sync::atomic::{AtomicU64, Ordering};

static SPLITMIX64_SEED: AtomicU64 = AtomicU64::new(0x9E3779B97F4A7C15);

#[inline]
fn splitmix64(x: &mut u64) -> u64 {
    *x = x.wrapping_add(0x9E3779B97F4A7C15);
    let mut z = *x;
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58476D1CE4E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D049BB133111EB);
    z ^ (z >> 31)
}

#[derive(Debug)]
struct Node {
    key: i64,
    priority: u64,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
    size: usize,
    count: usize, // count of equal keys
}

impl Node {
    fn new(key: i64) -> Self {
        let mut s = SPLITMIX64_SEED.fetch_add(0x9E3779B97F4A7C15, Ordering::Relaxed);
        let prio = splitmix64(&mut s);
        Node {
            key,
            priority: prio,
            left: None,
            right: None,
            size: 1,
            count: 1,
        }
    }

    fn recalc(&mut self) {
        let left_size = self.left.as_ref().map(|n| n.size).unwrap_or(0);
        let right_size = self.right.as_ref().map(|n| n.size).unwrap_or(0);
        self.size = left_size + self.count + right_size;
    }
}

/// A Treap (Cartesian tree) keyed by i64 with randomized priorities.
pub struct Treap {
    root: Option<Box<Node>>,
}

impl Treap {
    pub fn new() -> Self {
        Treap { root: None }
    }

    pub fn len(&self) -> usize {
        self.root.as_ref().map(|n| n.size).unwrap_or(0)
    }

    pub fn is_empty(&self) -> bool {
        self.root.is_none()
    }

    pub fn contains(&self, key: i64) -> bool {
        let mut cur = self.root.as_ref();
        while let Some(node) = cur {
            if key < node.key {
                cur = node.left.as_ref();
            } else if key > node.key {
                cur = node.right.as_ref();
            } else {
                return true;
            }
        }
        false
    }

    /// Insert one occurrence of `key`.
    pub fn insert(&mut self, key: i64) {
        self.root = Self::insert_rec(self.root.take(), key);
    }

    fn insert_rec(node: Option<Box<Node>>, key: i64) -> Option<Box<Node>> {
        match node {
            None => Some(Box::new(Node::new(key))),
            Some(mut boxed) => {
                if key == boxed.key {
                    boxed.count += 1;
                    boxed.recalc();
                    Some(boxed)
                } else if key < boxed.key {
                    boxed.left = Self::insert_rec(boxed.left.take(), key);
                    // heap property
                    if boxed.left.as_ref().map(|n| n.priority).unwrap_or(0) > boxed.priority {
                        boxed = Self::rotate_right(boxed);
                    } else {
                        boxed.recalc();
                    }
                    Some(boxed)
                } else {
                    boxed.right = Self::insert_rec(boxed.right.take(), key);
                    if boxed.right.as_ref().map(|n| n.priority).unwrap_or(0) > boxed.priority {
                        boxed = Self::rotate_left(boxed);
                    } else {
                        boxed.recalc();
                    }
                    Some(boxed)
                }
            }
        }
    }

    pub fn remove(&mut self, key: i64) {
        self.root = Self::remove_rec(self.root.take(), key);
    }

    fn remove_rec(node: Option<Box<Node>>, key: i64) -> Option<Box<Node>> {
    match node {
        None => None,
        Some(mut boxed) => {
            if key < boxed.key {
                boxed.left = Self::remove_rec(boxed.left.take(), key);
                boxed.recalc();
                Some(boxed)
            } else if key > boxed.key {
                boxed.right = Self::remove_rec(boxed.right.take(), key);
                boxed.recalc();
                Some(boxed)
            } else {
                // found node
                if boxed.count > 1 {
                    boxed.count -= 1;
                    boxed.recalc();
                    return Some(boxed);
                }
                // merge children
                Self::merge(boxed.left.take(), boxed.right.take())
            }
        }
    }
}


    fn merge(a: Option<Box<Node>>, b: Option<Box<Node>>) -> Option<Box<Node>> {
        match (a, b) {
            (None, r) => r,
            (l, None) => l,
            (Some(mut la), Some(mut rb)) => {
                if la.priority > rb.priority {
                    la.right = Self::merge(la.right.take(), Some(rb));
                    la.recalc();
                    Some(la)
                } else {
                    rb.left = Self::merge(Some(la), rb.left.take());
                    rb.recalc();
                    Some(rb)
                }
            }
        }
    }

    fn rotate_right(mut y: Box<Node>) -> Box<Node> {
        // y.left is Some
        let mut x = y.left.take().expect("rotate_right called with no left child");
        y.left = x.right.take();
        y.recalc();
        x.right = Some(y);
        x.recalc();
        x
    }

    fn rotate_left(mut x: Box<Node>) -> Box<Node> {
        let mut y = x.right.take().expect("rotate_left called with no right child");
        x.right = y.left.take();
        x.recalc();
        y.left = Some(x);
        y.recalc();
        y
    }

    pub fn inorder_vec(&self) -> Vec<i64> {
        let mut out = Vec::with_capacity(self.len());
        Self::inorder_rec(&self.root, &mut out);
        out
    }

    fn inorder_rec(node: &Option<Box<Node>>, out: &mut Vec<i64>) {
        if let Some(n) = node {
            Self::inorder_rec(&n.left, out);
            for _ in 0..n.count {
                out.push(n.key);
            }
            Self::inorder_rec(&n.right, out);
        }
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_insert_contains_len_inorder() {
        // reset seed for deterministic behavior in tests
        SPLITMIX64_SEED.store(12345, Ordering::Relaxed);

        let mut t = Treap::new();
        assert!(t.is_empty());
        t.insert(5);
        t.insert(3);
        t.insert(7);
        t.insert(3); // duplicate
        assert_eq!(t.len(), 4);
        assert!(t.contains(3));
        assert!(t.contains(5));
        assert!(t.contains(7));
        assert!(!t.contains(42));
        assert_eq!(t.inorder_vec(), vec![3, 3, 5, 7]);
    }

    #[test]
    fn test_remove_and_duplicates() {
        SPLITMIX64_SEED.store(999, Ordering::Relaxed);
        let mut t = Treap::new();
        t.insert(10);
        t.insert(10);
        t.insert(5);
        t.insert(15);
        assert_eq!(t.len(), 4);
        t.remove(10);
        assert!(t.contains(10));
        assert_eq!(t.len(), 3);
        t.remove(10);
        assert!(!t.contains(10));
        assert_eq!(t.len(), 2);
        t.remove(42); 
        assert_eq!(t.len(), 2);
        assert_eq!(t.inorder_vec(), vec![5, 15]);
    }

    #[test]
    fn test_mass_inserts_removes_stability() {
        SPLITMIX64_SEED.store(0xFEED, Ordering::Relaxed);
        let mut t = Treap::new();
        for v in 0..100 {
            t.insert(v);
        }
        assert_eq!(t.len(), 100);
        for v in 0..100 {
            assert!(t.contains(v));
        }
        for v in 0..100 {
            t.remove(v);
        }
        assert!(t.is_empty());
    }
}
