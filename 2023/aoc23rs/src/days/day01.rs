// Title: Day 1
use regex::Regex;
#[derive(Debug)]
pub struct Day01();

impl Day01 {
    pub fn main(input: &str, fix: bool) -> String {
        let f = if fix {
            first_last_digit_fix
        } else {
            first_last_digit
        };
        let lines = input.lines();
        let numbers: u32 = lines.map(f).sum();
        numbers.to_string()
    }
}


fn first_last_digit(input: &str) -> u32 {
    let chars = input.chars();
    let digits = chars.filter_map(|c| c.to_digit(10));
    let digits: Vec<u32> = digits.collect();
    (10 * digits.first().unwrap()) + digits.last().unwrap()
}

fn first_last_digit_fix(input: &str) -> u32 {
    let pattern = r"(one|two|three|four|five|six|seven|eight|nine|[0-9])"
    let re = Regex::new(pattern).unwrap();
    let numbers = input.char_indices().flat_map(|x| re.find( input[x.0..].as_ref()));
    let numbers = digits.map(str_to_u32);
    let digits: Vec<u32> = digits.collect();
    (10 * digits[0]) + digits[digits.len() - 1]
}

fn str_to_u32(input: regex::Match) -> u32 {
    let input = input.as_str();
    match input {
        "one" => 1,
        "two" => 2,
        "three" => 3,
        "four" => 4,
        "five" => 5,
        "six" => 6,
        "seven" => 7,
        "eight" => 8,
        "nine" => 9,
        _ => input.parse().unwrap(),
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    macro_rules! first_last_digit_test {
        ($($name:ident: $value:expr,)*) => {
        $(
            #[test]
            fn $name() {
                let (input, expected) = $value;
                assert_eq!(expected, first_last_digit(input));
            }
        )*
        }
    }

    macro_rules! first_last_digit_fix_test {
        ($($name:ident: $value:expr,)*) => {
        $(
            #[test]
            fn $name() {
                let (input, expected) = $value;
                assert_eq!(expected, first_last_digit_fix(input));
            }
        )*
        }
    }

    first_last_digit_test! {
        first_last_digit_test_1: ("1abc2", 12),
        first_last_digit_test_2: ("pqr3stu8vwx", 38),
        first_last_digit_test_3: ("a1b2c3d4e5f", 15),
        first_last_digit_test_4: ("treb7uchet", 77),
    }

    first_last_digit_fix_test! {
        first_last_digit_fix_test_1: ("two1nine", 29),
        first_last_digit_fix_test_2: ("eightwothree", 83),
        first_last_digit_fix_test_3: ("abcone2threexyz", 13),
        first_last_digit_fix_test_4: ("xtwone3four", 24),
        first_last_digit_fix_test_4: ("4nineeightseven2", 42),
        first_last_digit_fix_test_4: ("zoneight234", 14),
        first_last_digit_fix_test_4: ("7pqrstsixteen", 76),
        first_last_digit_fix_test_4: ("oneight", 18),
    }
}
