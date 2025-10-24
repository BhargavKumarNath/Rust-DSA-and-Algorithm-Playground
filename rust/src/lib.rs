// rust/src/lib.rs

pub mod union_find;

pub trait DataStructure {
    fn name(&self) -> &'static str;
}