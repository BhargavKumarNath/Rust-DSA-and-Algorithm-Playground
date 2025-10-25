// rust/src/lib.rs

pub mod union_find;
pub mod fenwick_tree;
pub mod treap;
pub mod sparse_table;
pub mod kmp;
pub trait DataStructure {
    fn name(&self) -> &'static str;
}