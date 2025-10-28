/// A Binary Indexed Tree (or Fenwick Tree) supports point updates and prefix sum queries
/// in O(log n) time. It is space efficient data structure for these operations.
pub struct FenwickTree{
    tree: Vec<i64>,
}

impl FenwickTree{
    pub fn new(size: usize) -> Self{
        FenwickTree{
            tree: vec![0; size + 1],
        }
    }

    /// Creates a new Fenwick Tree from an existing  array of numbers
    /// This is more efficient then creating an empty tree and adding elements one by one
    pub fn from_vec(values: &[i64]) -> Self{
        let mut tree = vec![0; values.len() + 1];
        for (i, &val) in values.iter().enumerate(){
            let idx = i + 1;
            tree[idx] += val;
            let parent_idx = idx + (idx & idx.wrapping_neg());
            if parent_idx < tree.len(){
                tree[parent_idx] += tree[idx];
            }
        }
        FenwickTree{tree}
    }

    /// Adds `delta` to the element at `index`
    /// The index is 0 based for the user
    pub fn add(&mut self, mut index: usize, delta: i64){
        index += 1;
        while index < self.tree.len(){
            self.tree[index] += delta;
            index += index & index.wrapping_neg();
        }
    }

    /// Queries the cumulative sum from the beginning up to the `index`
    /// The index is 0 based for the user
    pub fn query(&self, mut index: usize) -> i64{
        index += 1;
        let mut sum = 0;
        while index > 0{
            sum += self.tree[index];
            index -= index & index.wrapping_neg();
        }
        sum
    }

    /// Queries the sum of the range
    /// Both indicies are 0 based
    pub fn range_sum(&self, start: usize, end: usize) -> i64{
        if start > end{
            return 0;
        }
        if start == 0{
            self.query(end)
        } else{
            self.query(end) - self.query(start - 1)
        }
    }

    /// Returns the size of the array the Fenwick Tree represents
    pub fn len(&self) -> usize {
        self.tree.len() - 1
    }

    pub fn get_internal_tree(&self) -> Vec<i64> {
        self.tree.clone()
    }

}

#[cfg(test)]
mod tests{
    use super::*;

    #[test]
    fn test_from_vec_and_query(){
        let values = vec![1, 2, 3, 4, 5, 6, 7, 8];
        let ft = FenwickTree::from_vec(&values);

        assert_eq!(ft.query(0), 1);
        assert_eq!(ft.query(2), 6);
        assert_eq!(ft.query(7), 36);
    }

    #[test]
    fn test_add_and_query() {
        let mut ft = FenwickTree::new(10);
        ft.add(2, 5);
        assert_eq!(ft.query(1), 0);
        assert_eq!(ft.query(2), 5);
        assert_eq!(ft.query(9), 5);

        ft.add(2, -2);
        assert_eq!(ft.query(2), 3);

        ft.add(5, 10);
        assert_eq!(ft.query(4), 3);
        assert_eq!(ft.query(5), 13);
    }

    #[test]
    fn test_range_sum() {
        let values = vec![1, 1, 1, 1, 1, 1, 1, 1];
        let ft = FenwickTree::from_vec(&values);

        assert_eq!(ft.range_sum(0, 7), 8);
        assert_eq!(ft.range_sum(2, 4), 3);
        assert_eq!(ft.range_sum(5, 5), 1);
        assert_eq!(ft.range_sum(7, 6), 0);
    }
}




