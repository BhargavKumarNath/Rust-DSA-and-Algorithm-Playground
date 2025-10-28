use pyo3::prelude::*;
use pyo3::exceptions::PyIndexError;
use pyo3::exceptions::PyValueError;
use rust::union_find::UnionFind as RustUnionFind;
use rust::fenwick_tree::FenwickTree as RustFenwickTree;
use rust::{kmp, sparse_table::SparseTable, treap::Treap};

#[pyclass(name="UnionFind")]
struct PyUnionFind {
    uf: RustUnionFind,
    size: usize,
}

#[allow(non_local_definitions)]
#[pymethods]
impl PyUnionFind {
    #[new]
    fn new(n: usize) -> Self {
        PyUnionFind { 
            uf: RustUnionFind::new(n),
            size: n,
        }
    }

    fn find(&mut self, p: usize) -> PyResult<usize> {
        if p >= self.size {
            return Err(PyIndexError::new_err("Index out of bounds"));
        }
        Ok(self.uf.find(p))
    }
    fn union(&mut self, p: usize, q: usize) -> PyResult<bool> {
        if p >= self.size || q >= self.size {
            return Err(PyIndexError::new_err("Index out of bounds"));
        }
        Ok(self.uf.union(p, q))
    }

    fn connected(&mut self, p: usize, q: usize) -> PyResult<bool> {
        if p >= self.size || q >= self.size {
            return Err(PyIndexError::new_err("Index out of bounds"));
        }
        Ok(self.uf.connected(p, q))
    }

    #[getter]
    fn count(&self) -> usize {
        self.uf.count()
    }

    #[getter]
    fn parents(&self) -> PyResult<Vec<usize>> {
        Ok(self.uf.get_parents())
    }

}

#[pyclass(name = "FenwickTree")]
struct PyFenwickTree {
    ft:RustFenwickTree,
}

#[allow(non_local_definitions)]

#[pymethods]
impl PyFenwickTree {
    #[new]
    #[pyo3(signature = (size_or_values, /))]
    fn new(size_or_values: &Bound<'_, PyAny>) -> PyResult<Self> {
        if let Ok(size) = size_or_values.extract::<usize>() {
            Ok(PyFenwickTree { ft: RustFenwickTree::new(size) })
        } else if let Ok(values) = size_or_values.extract::<Vec<i64>>() {
            Ok(PyFenwickTree { ft: RustFenwickTree::from_vec(&values) })
        } else {
            Err(PyValueError::new_err("Argument must be an integer size or a list of numbers"))
        }
    }

    fn add(&mut self, index: usize, delta: i64) -> PyResult<()> {
        if index >= self.ft.len() {
            return Err(PyIndexError::new_err("Index out of bounds"));
        }
        self.ft.add(index, delta);
        Ok(())
    }

    fn query(&self, index: usize) -> PyResult<i64> {
        if index >= self.ft.len() {
            return Err(PyIndexError::new_err("Index out of bounds"));
        }
        Ok(self.ft.query(index))
    }

    fn range_sum(&self, start: usize, end: usize) -> PyResult<i64> {
        if end >= self.ft.len() {
             return Err(PyIndexError::new_err("End index out of bounds"));
        }
        Ok(self.ft.range_sum(start, end))
    }

    pub fn __len__(&self) -> usize {
        self.ft.len()
    }

    #[getter]
    fn internal_tree(&self) -> PyResult<Vec<i64>> {
        Ok(self.ft.get_internal_tree())
    }
    
}

// --- START: Added KMP Bindings ---

#[pyfunction]
fn prefix_function(pattern: &str) -> PyResult<Vec<usize>> {
    Ok(kmp::prefix_function(pattern))
}

#[pyfunction]
fn find_all(text: &str, pattern: &str) -> PyResult<Vec<usize>> {
    Ok(kmp::find_all(text, pattern))
}

// --- END: Added KMP Bindings ---

// --- START: Added Sparse Table Binding ---
#[pyclass(name = "SparseTable")]
struct PySparseTable {
    st: SparseTable<i64>,
}

#[allow(non_local_definitions)]
#[pymethods]
impl PySparseTable {
    #[new]
    fn new(arr: Vec<i64>) -> Self {
        PySparseTable {
            st: SparseTable::from_slice(&arr),
        }
    }

    /// Query the minimum value in the range [l, r] inclusive.
    fn query(&self, l: usize, r: usize) -> Option<i64> {
        self.st.query(l, r)
    }
}
// --- END: Added Sparse Table Binding ---

// --- START: Added Treap Binding ---
#[pyclass(name = "Treap")]
struct PyTreap {
    t: Treap,
}

#[allow(non_local_definitions)]
#[pymethods]
impl PyTreap {
    #[new]
    fn new() -> Self {
        PyTreap { t: Treap::new() }
    }

    fn insert(&mut self, key: i64) {
        self.t.insert(key);
    }

    fn remove(&mut self, key: i64) {
        self.t.remove(key); 
    }

    fn contains(&self, key: i64) -> bool {
        self.t.contains(key) 
    }

    fn len(&self) -> usize {
        self.t.len()
    }

    fn is_empty(&self) -> bool {
        self.t.is_empty()
    }

    /// Returns an in-order list of keys.
    fn inorder_vec(&self) -> Vec<i64> {
        self.t.inorder_vec()
    }

    // Add Python dunder methods for convenience
    fn __len__(&self) -> usize {
        self.t.len()
    }

    fn __contains__(&self, key: i64) -> bool {
        self.t.contains(key) 
    }
}
// --- END: Added Treap Binding ---

#[pymodule]
fn advanced_ds_playground_bindings(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Add existing classes
    m.add_class::<PyUnionFind>()?;
    m.add_class::<PyFenwickTree>()?;

    m.add_function(wrap_pyfunction!(prefix_function, m)?)?;
    m.add_function(wrap_pyfunction!(find_all, m)?)?;
    m.add_class::<PySparseTable>()?;
    m.add_class::<PyTreap>()?;
    Ok(())
}
