import math
import random

NONE = 0
CMP  = 1 # type supports equality and inequelity operators
TCMP = 3 # type supports all comparison operators
HASH = 4 # type can be hashed
ALL  = TCMP | HASH

# definisci la curva di probabilita'
# f(x) = e^kx
# integrale di f(x) = e^kx / k
# e^kx / k = y
# inverso dell'integrale
# x = log(y * k)/k

def choose(k, s):
    if k == 0:
        return random.choice(s)

    # integrale definito in [0, n]
    a, b = math.exp(k * 0) / k, math.exp(k * len(s)) / k
    y = random.uniform(a, b)
    # funzione inversa dell'integrale
    x = math.log(y * k) / k
    return s[int(x)]

def cs(flags2, flags3):
    def f(k, flags4):
        flags = flags2 | flags3 & flags4
        l = [(g, f) for op, g, f in TEMPLATES if op & flags == flags]
        gens, f = choose(k, l)
        return f.format(*(g(k - 0.10 - random.uniform(0.01, 0.1), flags) for g in gens))
    return f

def craft_flag():
    return f'`{cs(NONE, ALL)(0.2, NONE)} flag[10];`'

TEMPLATES = [
    (ALL , [], 'int'),
    (ALL , [], 'size_t'),
    (ALL , [], 'uint32_t'),
    (ALL , [], 'int32_t'),
    (ALL , [], 'll'),
    (ALL , [], 'unsigned ll int'),
    (ALL , [], '__int128_t'),
    (ALL , [], 'uint64_t'),
    (ALL , [], 'int64_t'),
    (NONE, [], 'std::mt19937_64'),
    (NONE, [], 'std::string'),
    (NONE, [], 'std::any'),
    (NONE, [], 'null_type'),
    (NONE, [], 'bool'),
    (NONE, [], 'std::byte'),
    (NONE, [], 'signed char'),
    (NONE, [], 'unsigned char'),
    (NONE, [], 'std::strong_ordering'),
    (NONE, [], 'std::weak_ordering'),
    (NONE, [], 'std::partial_ordering'),
    (NONE, [], 'std::mutex'),
    (NONE, [], 'std::thread'),
    (NONE, [], 'std::bitset<262144>'),
    (NONE, [], 'std::chrono::duration'),
    (NONE, [], 'FILE'),
    (NONE, [], 'std::ifstream'),
    (NONE, [], 'std::ofstream'),
    (NONE, [cs(NONE, ALL)], '{}*'),
    (NONE, [cs(NONE, ALL)], '{}&'),
    (NONE, [cs(NONE, ALL)], '{}[]'),
    (NONE, [cs(NONE, ALL)], '{} const'),
    (NONE, [cs(NONE, ALL)], 'std::deque<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::set<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::multiset<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::unordered_set<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::unordered_multiset<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::priority_queue<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::array<{}, 2>'),
    (NONE, [cs(NONE, ALL)], 'std::array<{}, 3>'),
    (NONE, [cs(NONE, ALL)], 'std::vector<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::unique_ptr<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::shared_ptr<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::weak_ptr<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::auto_ptr<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::optional<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::span<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::priority_queue<{0}, std::vector<{0}>, std::greater<{0}>>'),
    (NONE, [cs(NONE, ALL)], 'std::chrono::time_point<std::chrono::high_resolution_clock, std::chrono::duration<{}, std::ratio<1, 1000000000>>>'),
    (NONE, [cs(NONE, ALL)], '__gnu_pbds::tree<{0}, __gnu_pbds::null_type, std::less<{0}>, __gnu_pbds::rb_tree_tag, __gnu_pbds::tree_order_statistics_node_update>'),
    (NONE, [cs(NONE, ALL), cs(NONE, ALL)], 'std::pair<{}, {}>'),
    (NONE, [cs(NONE, ALL), cs(NONE, ALL)], 'std::variant<{}, {}>'),
    (NONE, [cs(NONE, ALL), cs(NONE, ALL)], 'std::map<{}, {}>'),
    (NONE, [cs(NONE, ALL), cs(NONE, ALL)], 'std::unordered_map<{}, {}>'),
    (NONE, [cs(NONE, ALL), cs(NONE, ALL)], 'std::multimap<{}, {}>'),
    (NONE, [cs(NONE, ALL), cs(NONE, ALL)], 'std::unordered_multimap<{}, {}>'),
    (NONE, [cs(NONE, ALL), cs(NONE, ALL)], 'std::conditional_t<true, {}, {}>'),
    (NONE, [cs(NONE, ALL), cs(NONE, ALL)], 'std::conditional_t<false, {}, {}>'),
    (NONE, [cs(NONE, ALL), cs(NONE, ALL), cs(NONE, ALL)], 'std::tuple<{}, {}, {}>'),
    (NONE, [cs(NONE, ALL), cs(NONE, ALL), cs(NONE, ALL), cs(NONE, ALL)], 'std::tuple<{}, {}, {}, {}>')
]

if __name__ == '__main__':
    print(craft_flag())
