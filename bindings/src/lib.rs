use pyo3::prelude::*;
use pyo3::exceptions::PyIndexError;
use rust::union_find::UnionFind as RustUnionFind;

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

/// A Python module implemented in Rust
#[pymodule]
fn advanced_ds_playground(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyUnionFind>()?;
    Ok(())
}
