/// Sparse Table for immutable array queries where the operation is idempotent (like min, gcd).
/// - Build: O(n log n)
/// - Query: O(1)
///
/// Generic over T: Copy + Ord. The combining operation implemented here is `min`.
pub struct SparseTable<T>
where
    T: Copy + Ord,
{
    table: Vec<Vec<T>>,
    log: Vec<usize>,
}

impl<T> SparseTable<T>
where
    T: Copy + Ord,
{
    pub fn from_slice(arr: &[T]) -> Self {
        let n = arr.len();
        let mut log = vec![0usize; n + 1];
        for i in 2..=n {
            log[i] = log[i / 2] + 1;
        }
        let max_k = if n == 0 { 0 } else { log[n] + 1 };
        let mut table: Vec<Vec<T>> = Vec::with_capacity(max_k);
        if n == 0 {
            return SparseTable { table, log };
        }
        table.push(arr.to_vec()); // k = 0
        for k in 1..max_k {
            let len = n - (1 << k) + 1;
            let mut row = Vec::with_capacity(len);
            let prev = &table[k - 1];
            for i in 0..len {
                let a = prev[i];
                let b = prev[i + (1 << (k - 1))];
                row.push(std::cmp::min(a, b));
            }
            table.push(row);
        }
        SparseTable { table, log }
    }

    /// Query range [l, r] inclusive. Returns None if l or r out of bounds or l > r.
    pub fn query(&self, l: usize, r: usize) -> Option<T> {
        if self.table.is_empty() {
            return None;
        }
        let n = self.table[0].len();
        if l > r || r >= n {
            return None;
        }
        let k = self.log[r - l + 1];
        let left = self.table[k][l];
        let right = self.table[k][r + 1 - (1 << k)];
        Some(std::cmp::min(left, right))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sparse_table_min_basic() {
        let arr = vec![5, 2, 4, 7, 1, 3];
        let st = SparseTable::from_slice(&arr);
        assert_eq!(st.query(0, 0), Some(5));
        assert_eq!(st.query(0, 2), Some(2));
        assert_eq!(st.query(1, 4), Some(1));
        assert_eq!(st.query(4, 5), Some(1));
        assert_eq!(st.query(5, 5), Some(3));
    }

    #[test]
    fn test_invalid_queries() {
        let arr: Vec<i64> = vec![];
        let st = SparseTable::from_slice(&arr);
        assert_eq!(st.query(0, 0), None);

        let arr2 = vec![1, 2, 3];
        let st2 = SparseTable::from_slice(&arr2);
        assert_eq!(st2.query(2, 1), None);
        assert_eq!(st2.query(0, 10), None);
    }
}
