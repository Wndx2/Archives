// 21.09.2025
// VERY first program I wrote -- there are no error prevention or anything.
// It ONLY does the basics

use std::io;
use std::process::Command;

fn clear() {
	Command::new("clear").status().unwrap();
}

fn main() {
	clear();
	println!("\n\n\n\nPolynomial (Degree 2):");
	println!("ax^2 + bx + c");
	println!("\n====================\n");

	loop {
		// Making a, b, c as strings so that stdio can read it
		let mut a = String::new();
		let mut b = String::new();
		let mut c = String::new();

		// Reading 'a'
		println!("\nEnter first unknown (a):");
		io::stdin().read_line(&mut a).expect("Error");
		let a: i32 = a.trim().parse().expect("Error");

		// Breaks when a=0, as 0 makes it non-quadratic
		if a == 0 {
			break;
		}

		// Reading 'b'
		println!("\nEnter second unknown (b):");
		io::stdin().read_line(&mut b).expect("Error");
		let b: i32 = b.trim().parse().expect("Error");

		// Reading 'c'
		println!("\nEnter third unknown (c):");
		io::stdin().read_line(&mut c).expect("Error");
		let c: i32 = c.trim().parse().expect("Error");

		clear();

		println!("\n====================\n");

		println!("a = {}, b = {}, c = {}", a, b, c);

		// Calculating discriminant
		let d = b.pow(2) - 4 * a * c;
		println!("Discriminant: {}\n", d);

		// Solve roots
		if d < 0 {
			println!("D < 0: No real roots\n");
		} else {
			let d_f64 = d as f64;
			let sqrt_d = d_f64.sqrt();
			let a_f64 = a as f64;
			let b_f64 = b as f64;

			if d == 0 {
				println!("D = 0: One real root");
			} else {
				println!("D > 0: Two real roots");
			}

			let x1 = (-b_f64 + sqrt_d) / (2.0 * a_f64);
			let x2 = (-b_f64 - sqrt_d) / (2.0 * a_f64);

			println!("X1 = {}", x1);
			println!("X2 = {}", x2);

			println!("\n====================\n");
		}
	}
}
