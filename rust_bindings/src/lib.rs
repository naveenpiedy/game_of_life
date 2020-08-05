use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::thread;

static WHITE: usize = 16777215;
static BLACK: usize = 0;

#[pyfunction]
fn pixel_array_manipulator(pixel_array: Vec<Vec<usize>>, height: usize, width: usize) -> PyResult<Vec<Vec<usize>>> {
    let mut new_pixel_vector: Vec<Vec<usize>> = Vec::new();

    // let (left, right) = pixel_array.split_at(150);

    for i in 0..height {
        let mut temp_vector: Vec<usize> = Vec::new();
        for j in 0..width {
            let life = game_of_life(&pixel_array, i, j, height, width);
            temp_vector.push(life)
        }
        new_pixel_vector.push(temp_vector);
    }

    Ok(new_pixel_vector)
}


fn game_of_life(pixel_vector: &Vec<Vec<usize>>, x: usize, y: usize, height: usize, width: usize) -> usize {
    let mut x_0 = 0;
    let mut y_0 = 0;

    if x > 0 {
        x_0 = x - 1;
    }
    if y > 0 {
        y_0 = y - 1;
    }

    let x_values = [x_0, x, x + 1];
    let y_values = [y_0, y, y + 1];

    let mut live_neighbours = 0;

    for i in x_values.iter() {
        for j in y_values.iter() {
            if (i < &height) && (j < &width) {
                if (i, j) != (&x, &y) {
                    {
                        if pixel_vector[i.clone()][j.clone()] == WHITE {
                            live_neighbours += 1;
                        }
                    }
                }
            }
        }
    }

    if pixel_vector[x][y] == WHITE && !(1 < live_neighbours && live_neighbours < 4) {
        BLACK
    } else if pixel_vector[x][y] == BLACK && live_neighbours == 3 {
        WHITE
    } else {
        pixel_vector[x][y]
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn pixel_array_manipulation(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(pixel_array_manipulator))?;
    Ok(())
}
