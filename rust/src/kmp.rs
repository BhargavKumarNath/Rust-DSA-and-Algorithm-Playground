// rust/src/kmp.rs
/// Knuth-Morris-Pratt (KMP) algorithm implementation for substring search.
/// - prefix_function computes the longest proper prefix which is also suffix for each prefix.
/// - find_all returns start indices where pattern matches text. Works on bytes (UTF-8).
///
/// Complexity: O(n + m)
pub fn prefix_function(pattern: &str) -> Vec<usize> {
    let s = pattern.as_bytes();
    let n = s.len();
    let mut pi = vec![0usize; n];
    for i in 1..n {
        let mut j = pi[i - 1];
        while j > 0 && s[i] != s[j] {
            j = pi[j - 1];
        }
        if s[i] == s[j] {
            j += 1;
        }
        pi[i] = j;
    }
    pi
}


/// Find all occurrences of `pattern` in `text`. Returns vector of starting indices.
/// Returns empty vec if pattern is empty or longer than text.
pub fn find_all(text: &str, pattern: &str) -> Vec<usize> {
    let n = text.len();
    let m = pattern.len();
    if m == 0 || m > n {
        return vec![];
    }
    let mut res = vec![];
    let pi = prefix_function(pattern);
    let t_bytes = text.as_bytes();
    let p_bytes = pattern.as_bytes();
    let mut j = 0;
    for i in 0..n {
        while j > 0 && t_bytes[i] != p_bytes[j] {
            j = pi[j - 1];
        }
        if t_bytes[i] == p_bytes[j] {
            j += 1;
        }
        if j == m {
            res.push(i + 1 - m);
            j = pi[j - 1];
        }
    }
    res
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_prefix_function_basic() {
        let p = "ababcabab";
        let pi = prefix_function(p);
        let expected = vec![0, 0, 1, 2, 0, 1, 2, 3, 4]; 
        assert_eq!(pi, expected);
    }

    #[test]
    fn test_find_all_simple() {
        let text = "ababcabababc";
        let pattern = "abab";
        let occ = find_all(text, pattern);
        assert_eq!(occ, vec![0, 5, 7]);
    }

    #[test]
    fn test_find_all_no_match() {
        let text = "hello world";
        let pattern = "abc";
        assert!(find_all(text, pattern).is_empty());
    }

    #[test]
    fn test_find_all_overlapping() {
        let text = "aaaaa";
        let pattern = "aa";
        assert_eq!(find_all(text, pattern), vec![0, 1, 2, 3]);
    }

    #[test]
    fn test_empty_pattern() {
        assert!(find_all("anytext", "").is_empty());
    }
}