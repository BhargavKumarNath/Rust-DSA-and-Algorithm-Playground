use pyo3::prelude::*;
use pyo3::exceptions::PyIndexError;
use pyo3::exceptions::PyValueError;
use rust::union_find::UnionFind as RustUnionFind;
use rust::fenwick_tree::FenwickTree as RustFenwickTree;
#[pyclass(name="UnionFind")]
struct PyUnionFind {
    uf: RustUnionFind,
    size: usize,
}

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

}



#[pyclass(name = "FenwickTree")]
struct PyFenwickTree {
    ft:RustFenwickTree,
}

#[pymethods]
impl PyFenwickTree {
    #[new]
    #[pyo3(signature = (size_or_values, /))]
    fn new(size_or_values: &PyAny) -> PyResult<Self> {
        // This is a more advanced constructor. It can accept either an integer (size)
        // or a list of numbers (initial values). This is very Pythonic.
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
}



/// A Python module implemented in Rust
#[pymodule]
fn advanced_ds_playground(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyUnionFind>()?;
    m.add_class::<PyFenwickTree>()?;
    Ok(())
}
