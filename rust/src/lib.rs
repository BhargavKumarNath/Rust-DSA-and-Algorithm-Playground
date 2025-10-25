// rust/src/lib.rs

pub mod union_find;
pub mod fenwick_tree;
pub trait DataStructure {
    fn name(&self) -> &'static str;
}