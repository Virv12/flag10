const NONE: u32 = 0;
const CMP: u32 = 1; // type supports equality and inequelity operators
const TCMP: u32 = 3; // type supports all comparison operators
const HASH: u32 = 5; // type can be hashed
const DEFC: u32 = 8; // default constructor
const ALL: u32 = TCMP | HASH | DEFC;

#[derive(Debug, Clone, Copy)]
enum X {
    Str(&'static str),
    Gen(u32, u32),
}

fn choose<T>(k: f64, mut it: impl Iterator<Item = T>) -> Option<T> {
    let mut val = it.next()?;
    let k = k.exp();
    let mut p = 1.0;
    let mut total = 0.0;
    for val2 in it {
        total += p;
        p *= k;
        if rand::random::<f64>() * total < p {
            val = val2;
        }
    }
    Some(val)
}

fn gen_type(out: &mut String, k: f64, flags: u32) {
    let it = TEMPLATES.iter().filter(|(f, _)| f & flags == flags);
    let &(_, gens) = choose(k, it).expect("No template found");
    for &gen in gens {
        match gen {
            X::Str(s) => out.push_str(s),
            X::Gen(or, and) => {
                let del = rand::random::<f64>() * (0.20 - 0.10) + 0.10;
                gen_type(out, k - del, or | and & flags);
            }
        }
    }
}

pub async fn get_flag() -> String {
    let mut out = String::new();
    out.push('`');
    gen_type(&mut out, 0.2, DEFC);
    out.push_str(" flag[10];`");
    out
}

static TEMPLATES: &[(u32, &[X])] = &[
    (ALL, &[X::Str("int")]),
    (ALL, &[X::Str("size_t")]),
    (ALL, &[X::Str("uint32_t")]),
    (ALL, &[X::Str("int32_t")]),
    (ALL, &[X::Str("ll")]),
    (ALL, &[X::Str("unsigned ll int")]),
    (TCMP | DEFC, &[X::Str("__int128_t")]),
    (ALL, &[X::Str("uint64_t")]),
    (ALL, &[X::Str("int64_t")]),
    (DEFC, &[X::Str("std::mt19937_64")]),
    (ALL, &[X::Str("std::string")]),
    (DEFC, &[X::Str("std::any")]),
    (ALL, &[X::Str("bool")]),
    (ALL, &[X::Str("std::byte")]),
    (ALL, &[X::Str("signed char")]),
    (ALL, &[X::Str("unsigned char")]),
    (CMP, &[X::Str("std::strong_ordering")]),
    (CMP, &[X::Str("std::weak_ordering")]),
    (CMP, &[X::Str("std::partial_ordering")]),
    (DEFC, &[X::Str("std::mutex")]),
    (DEFC, &[X::Str("std::thread")]),
    (CMP | HASH | DEFC, &[X::Str("std::bitset<262144>")]),
    (TCMP | DEFC, &[X::Str("std::chrono::seconds")]),
    (DEFC, &[X::Str("FILE")]),
    (DEFC, &[X::Str("std::ifstream")]),
    (DEFC, &[X::Str("std::ofstream")]),
    (ALL, &[X::Gen(NONE, NONE), X::Str(" *")]),
    (
        TCMP | DEFC,
        &[X::Str("std::deque<"), X::Gen(NONE, TCMP), X::Str(">")],
    ),
    (
        TCMP | DEFC,
        &[X::Str("std::set<"), X::Gen(TCMP, NONE), X::Str(">")],
    ),
    (
        TCMP | DEFC,
        &[X::Str("std::multiset<"), X::Gen(TCMP, NONE), X::Str(">")],
    ),
    (
        CMP | DEFC,
        &[
            X::Str("std::unordered_set<"),
            X::Gen(HASH, NONE),
            X::Str(">"),
        ],
    ),
    (
        CMP | DEFC,
        &[
            X::Str("std::unordered_multiset<"),
            X::Gen(HASH, NONE),
            X::Str(">"),
        ],
    ),
    (
        DEFC,
        &[
            X::Str("std::priority_queue<"),
            X::Gen(TCMP, NONE),
            X::Str(">"),
        ],
    ),
    (
        TCMP | DEFC,
        &[
            X::Str("std::array<"),
            X::Gen(NONE, TCMP | DEFC),
            X::Str(", 2>"),
        ],
    ),
    (
        TCMP | DEFC,
        &[
            X::Str("std::array<"),
            X::Gen(NONE, TCMP | DEFC),
            X::Str(", 3>"),
        ],
    ),
    (
        TCMP | DEFC,
        &[X::Str("std::vector<"), X::Gen(NONE, TCMP), X::Str(">")],
    ),
    (
        TCMP | DEFC,
        &[X::Str("std::unique_ptr<"), X::Gen(NONE, NONE), X::Str(">")],
    ),
    (
        ALL,
        &[X::Str("std::shared_ptr<"), X::Gen(NONE, NONE), X::Str(">")],
    ),
    (
        DEFC,
        &[X::Str("std::weak_ptr<"), X::Gen(NONE, NONE), X::Str(">")],
    ),
    (
        ALL,
        &[
            X::Str("std::optional<"),
            X::Gen(NONE, TCMP | HASH),
            X::Str(">"),
        ],
    ),
    (
        DEFC,
        &[
            X::Str("std::span<"),
            X::Gen(NONE, ALL),
            X::Str(", std::dynamic_extent>"),
        ],
    ),
    (
        TCMP | DEFC,
        &[
            X::Str("std::pair<"),
            X::Gen(NONE, ALL),
            X::Str(", "),
            X::Gen(NONE, ALL),
            X::Str(">"),
        ],
    ),
    (
        ALL,
        &[
            X::Str("std::variant<"),
            X::Gen(NONE, TCMP | HASH),
            X::Str(", "),
            X::Gen(NONE, TCMP | HASH),
            X::Str(">"),
        ],
    ),
    (
        ALL,
        &[
            X::Str("std::variant<"),
            X::Gen(NONE, TCMP | HASH),
            X::Str(", "),
            X::Gen(NONE, TCMP | HASH),
            X::Str(", "),
            X::Gen(NONE, TCMP | HASH),
            X::Str(">"),
        ],
    ),
    (
        TCMP | DEFC,
        &[
            X::Str("std::map<"),
            X::Gen(TCMP, NONE),
            X::Str(", "),
            X::Gen(NONE, TCMP),
            X::Str(">"),
        ],
    ),
    (
        TCMP | DEFC,
        &[
            X::Str("std::multimap<"),
            X::Gen(TCMP, NONE),
            X::Str(", "),
            X::Gen(NONE, TCMP),
            X::Str(">"),
        ],
    ),
    (
        CMP | DEFC,
        &[
            X::Str("std::unordered_map<"),
            X::Gen(HASH, NONE),
            X::Str(", "),
            X::Gen(NONE, CMP),
            X::Str(">"),
        ],
    ),
    (
        CMP | DEFC,
        &[
            X::Str("std::unordered_multimap<"),
            X::Gen(HASH, NONE),
            X::Str(", "),
            X::Gen(NONE, CMP),
            X::Str(">"),
        ],
    ),
    (
        ALL,
        &[
            X::Str("std::conditional_t<true, "),
            X::Gen(NONE, ALL),
            X::Str(", "),
            X::Gen(NONE, ALL),
            X::Str(">"),
        ],
    ),
    (
        ALL,
        &[
            X::Str("std::conditional_t<false, "),
            X::Gen(NONE, ALL),
            X::Str(", "),
            X::Gen(NONE, ALL),
            X::Str(">"),
        ],
    ),
    (
        TCMP | DEFC,
        &[
            X::Str("std::tuple<"),
            X::Gen(NONE, ALL),
            X::Str(", "),
            X::Gen(NONE, ALL),
            X::Str(", "),
            X::Gen(NONE, ALL),
            X::Str(">"),
        ],
    ),
    (
        TCMP | DEFC,
        &[
            X::Str("std::tuple<"),
            X::Gen(NONE, ALL),
            X::Str(", "),
            X::Gen(NONE, ALL),
            X::Str(", "),
            X::Gen(NONE, ALL),
            X::Str(", "),
            X::Gen(NONE, ALL),
            X::Str(">"),
        ],
    ),
];
