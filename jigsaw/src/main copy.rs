use plotters::coord::types::RangedCoordf32;
use plotters::prelude::*;
use rand::Rng;

fn main() {
    // println!("Hello, world!");
    const W: usize = 13;
    const H: usize = 13;
    // const W: usize = 5;
    // const H: usize = 5;
    const PIECE_COUNT: usize = W * H;
    let edge_types = 7;

    let mut pieces = [[0, 0, 0, 0]; PIECE_COUNT];
    // seed 42 for reproducibility
    let mut rng: rand::rngs::StdRng = rand::SeedableRng::seed_from_u64(54);
    // let mut rng = rand::thread_rng();

    for y in 0..H {
        for x in 0..W {
            let idx = y * W + x;
            let idx_right = y * W + x + 1;
            let idx_down = (y + 1) * W + x;
            let right = rng.gen_range(1..edge_types);
            let down = rng.gen_range(1..edge_types);
            if x < W - 1 {
                pieces[idx][1] = right;
                pieces[idx_right][3] = -right;
            }
            if y < H - 1 {
                pieces[idx][2] = down;
                pieces[idx_down][0] = -down;
            }
        }
    }

    fn draw_puzzle(placed: [[(usize,usize); W]; H], pieces: [[i32; 4]; PIECE_COUNT], filename: &str) {
        let root = BitMapBackend::new(filename, (800, 800)).into_drawing_area();
        root.fill(&WHITE).unwrap();
        let root = root.apply_coord_spec(Cartesian2d::<RangedCoordf32, RangedCoordf32>::new(
            0f32..(W as f32),
            0f32..(H as f32),
            (0..800, 0..800),
        ));

        let blue = RGBColor(0, 0, 255);
        let black = RGBColor(0, 0, 0);
        let lightorange = RGBColor(255, 200, 100);

        // middle numbers in blue
        for y in 0..H {
            for x in 0..W {
                // let idx = y * W + x;
                let (idx, rot) = placed[y][x];
                if idx != y*W + x || rot != 0 {
                    root.draw(&Rectangle::new(
                        [(x as f32, y as f32), (x as f32 + 1.0, y as f32 + 1.0)],
                        lightorange.filled(),
                    )).unwrap();
                }
                // number of piece in the middle
                root.draw(&Text::new(
                    format!("{} (R{})", idx, rot),
                    (x as f32 + 0.5, y as f32 + 0.5),
                    ("sans-serif", 10).into_font().color(&blue),
                ))
                .unwrap();
            }
        }

        let k = 0.15;
        for y in 0..H {
            for x in 0..W {
                let (idx,rot) = placed[y][x];
                for i in 0..4 {
                    let (x1, y1) = match i {
                        0 => (x as f32 + 0.5, y as f32 + k),
                        1 => (x as f32 + 1.0 - k, y as f32 + 0.5),
                        2 => (x as f32 + 0.5, y as f32 + 1.0 - k),
                        3 => (x as f32 + k, y as f32 + 0.5),
                        _ => (0.0, 0.0),
                    };
                    root.draw(&Text::new(
                        format!("{}", pieces[idx][(i+rot)%4]),
                        (x1, y1),
                        ("sans-serif", 10).into_font().color(&black),
                    ))
                    .unwrap();
                }
                for i in 0..4 {
                    let (x1, y1, x2, y2) = match i {
                        0 => (x as f32, y as f32, x as f32 + 1.0, y as f32),
                        1 => (x as f32, y as f32, x as f32, y as f32 + 1.0),
                        2 => (x as f32, y as f32 + 1.0, x as f32 + 1.0, y as f32 + 1.0),
                        3 => (x as f32 + 1.0, y as f32, x as f32 + 1.0, y as f32 + 1.0),
                        _ => (0.0, 0.0, 0.0, 0.0),
                    };
                    root.draw(&PathElement::new(vec![(x1, y1), (x2, y2)], &BLACK))
                        .unwrap();
                }
            }
        }
    }

    // solve the puzzle

    fn solutions(
        x: usize,
        y: usize,
        remaining: Vec<usize>,
        pieces: [[i32; 4]; PIECE_COUNT],
        mut placed: [[(usize, usize); W]; H],
        found_solutions: &mut Vec<[[(usize,usize); W]; H]>,
    ) -> i32 {
        // let solutions = |x: usize, y: usize, remaining: Vec<i32>| -> i32 {
        if remaining.len() == 0 {
            // println!("solution found");
            let sol = placed.clone();
            let count = found_solutions.len();
            draw_puzzle(sol, pieces, &format!("puzzle_{}.png", count));
            found_solutions.push(sol);
            println!("Solution {} found", count);
            return 1;
        }
        if x == W {
            return solutions(0, y + 1, remaining, pieces, placed, found_solutions);
        }
        if y == H {
            assert!(false);
        }
        let side_left = if x == 0 {
            0
        } else {
            let (idx, rot) = placed[y][x - 1];
            pieces[idx][(1 + rot) % 4]
        };
        let side_up = if y == 0 {
            0
        } else {
            let (idx, rot) = placed[y - 1][x];
            pieces[idx][(2 + rot) % 4]
        };
        let mut count = 0;
        for i in 0..remaining.len() {
            for rot in 0..4 {
                let piece = remaining[i];
                if x == 0 && y == 0 && (rot != 0 || piece != 0) {
                    continue;
                }
                let sides = pieces[piece];
                // if (x > 0 && sides[3] != side_left) || (y > 0 && sides[0] != side_up) {
                //     continue;
                // }
                if sides[(3+rot)%4] != -side_left {
                    continue;
                }
                if sides[(0+rot)%4] != -side_up {
                    continue;
                }
                if x == W-1 && sides[1] != 0 {
                    continue;
                }
                if y == H-1 && sides[2] != 0 {
                    continue;
                }
                // if (sides[0] != side_up || sides[3] != side_left) {
                //     continue;
                // }
                let mut remaining2 = remaining.clone();
                remaining2.remove(i);
                placed[y][x] = (piece, rot);
                let result = solutions(x + 1, y, remaining2, pieces, placed, found_solutions);
                count += result;
                // let piece_edges = pieces[piece];
                // if (x == 0 || piece_edges[3] == side_left) && (y == 0 || piece_edges[0] == side_up) {
                //     let result = solutions(x + 1, y, remaining2, pieces, placed);
                //     if result == 1 {
                //         return 1;
                //     }
                // }
            }
        }
        return count;
    }

    let mut remaining = Vec::new();
    for i in 0..PIECE_COUNT {
        remaining.push(i);
    }
    let placed = [[(0, 0); W]; H];
    let mut found_solutions = Vec::new();
    let result = solutions(0, 0, remaining, pieces, placed, &mut found_solutions);
    if result == 0 {
        println!("no solution found");
    } else {
        println!("{:?} solutions found", result);
    }
}
