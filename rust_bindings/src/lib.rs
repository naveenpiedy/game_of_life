use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

static WHITE: usize = 3555324;
static BLACK: usize = 0;

#[pyfunction]
fn pixel_array_manipulator(
    pixel_array: Vec<Vec<usize>>,
    height: usize,
    width: usize,
) -> PyResult<Vec<Vec<usize>>> {
    let mut new_pixel_vector: Vec<Vec<usize>> = Vec::new();

    crossbeam::scope(|scope| {
        let handle1 = scope.spawn(|_| threaded_function(&pixel_array, 0, 100, 300));
        let handle2 = scope.spawn(|_| threaded_function(&pixel_array, 100, 200, 300));
        let handle3 = scope.spawn(|_| threaded_function(&pixel_array, 200, 300, 300));

        let vec1 = handle1.join().unwrap();
        let vec2 = handle2.join().unwrap();
        let vec3 = handle3.join().unwrap();

        new_pixel_vector = [&vec1[..], &vec2[..], &vec3[..]].concat()
    });

    // new_pixel_vector = threaded_function(&pixel_array, 0, 300, 300);

    Ok(new_pixel_vector)
}

fn threaded_function(
    pixel_array: &Vec<Vec<usize>>,
    start_height: usize,
    height: usize,
    width: usize,
) -> Vec<Vec<usize>> {
    let mut new_pixel_vector: Vec<Vec<usize>> = Vec::new();

    for i in start_height..height {
        let mut temp_vector: Vec<usize> = Vec::new();
        for j in 0..width {
            let life = game_of_life(pixel_array, i, j, height, width);
            temp_vector.push(life)
        }
        new_pixel_vector.push(temp_vector);
    }
    new_pixel_vector
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
            if ((i < &height) && (j < &width)) && (i, j) != (&x, &y) {
                {
                    if pixel_vector[*i][*j] != BLACK {
                        live_neighbours += 1;
                    }
                }
            }
        }
    }

    if pixel_vector[x][y] != BLACK && !(1 < live_neighbours && live_neighbours < 4) {
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
