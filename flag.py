import math
import random
import sys
import re

NONE = 0
CMP  = 1 # type supports equality and inequelity operators
TCMP = 3 # type supports all comparison operators
HASH = 5 # type can be hashed
DEFC = 8 # default constructor
ALL  = TCMP | HASH | DEFC

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

def craft_flag(n : int = 10):
    return f'`{cs(NONE, ALL)(0.2, DEFC)} flag[{n}];`'

TEMPLATES = [
    (ALL , [], 'int'),
    (ALL , [], 'size_t'),
    (ALL , [], 'uint32_t'),
    (ALL , [], 'int32_t'),
    (ALL , [], 'll'),
    (ALL , [], 'unsigned ll int'),
    (TCMP | DEFC , [], '__int128_t'),
    (ALL , [], 'uint64_t'),
    (ALL , [], 'int64_t'),
    (DEFC, [], 'std::mt19937_64'),
    (ALL , [], 'std::string'),
    (DEFC, [], 'std::any'),
    # (NONE, [], 'null_type'),
    (ALL , [], 'bool'),
    (ALL , [], 'std::byte'),
    (ALL , [], 'signed char'),
    (ALL , [], 'unsigned char'),
    (CMP , [], 'std::strong_ordering'),
    (CMP , [], 'std::weak_ordering'),
    (CMP , [], 'std::partial_ordering'),
    (DEFC, [], 'std::mutex'),
    (DEFC, [], 'std::thread'),
    (CMP | HASH | DEFC, [], 'std::bitset<262144>'),
    (TCMP | DEFC, [], 'std::chrono::seconds'),
    (DEFC, [], 'FILE'),
    (DEFC, [], 'std::ifstream'),
    (DEFC, [], 'std::ofstream'),
    (ALL , [cs(NONE, NONE)], '{} *'),
    # (ALL , [cs(NONE, ALL)], '{}&'),
    # (ALL , [cs(NONE, ALL)], '{}[]'),
    # (ALL , [cs(NONE, ALL)], '{} const'),
    (TCMP | DEFC, [cs(NONE, TCMP)], 'std::deque<{}>'),
    (TCMP | DEFC, [cs(TCMP, NONE)], 'std::set<{}>'),
    (TCMP | DEFC, [cs(TCMP, NONE)], 'std::multiset<{}>'),
    (CMP | DEFC, [cs(HASH, NONE)], 'std::unordered_set<{}>'),
    (CMP | DEFC, [cs(HASH, NONE)], 'std::unordered_multiset<{}>'),
    (DEFC, [cs(TCMP, NONE)], 'std::priority_queue<{}>'),
    (TCMP | DEFC, [cs(NONE, TCMP | DEFC)], 'std::array<{}, 2>'),
    (TCMP | DEFC, [cs(NONE, TCMP | DEFC)], 'std::array<{}, 3>'),
    (TCMP | DEFC, [cs(NONE, TCMP)], 'std::vector<{}>'),
    (TCMP | DEFC, [cs(NONE, NONE)], 'std::unique_ptr<{}>'),
    (ALL , [cs(NONE, NONE)], 'std::shared_ptr<{}>'),
    (DEFC, [cs(NONE, NONE)], 'std::weak_ptr<{}>'),
    # (NONE, [cs(NONE, ALL)], 'std::auto_ptr<{}>'),
    (ALL , [cs(NONE, TCMP | HASH)], 'std::optional<{}>'),
    (DEFC, [cs(NONE, ALL)], 'std::span<{}>'),
    (DEFC, [cs(TCMP, NONE)], 'std::priority_queue<{0}, std::vector<{0}>, std::greater<{0}>>'),
    # (NONE, [cs(NONE, ALL)], 'std::chrono::time_point<std::chrono::high_resolution_clock, std::chrono::duration<{}, std::ratio<1, 1000000000>>>'),
    (DEFC, [cs(TCMP, NONE)], '__gnu_pbds::tree<{0}, __gnu_pbds::null_type, std::less<{0}>, __gnu_pbds::rb_tree_tag, __gnu_pbds::tree_order_statistics_node_update>'),
    (TCMP | DEFC, [cs(NONE, ALL), cs(NONE, ALL)], 'std::pair<{}, {}>'),
    (ALL , [cs(NONE, TCMP | HASH), cs(NONE, TCMP | HASH)], 'std::variant<{}, {}>'),
    (TCMP | DEFC, [cs(TCMP, NONE), cs(NONE, TCMP)], 'std::map<{}, {}>'),
    (TCMP | DEFC, [cs(TCMP, NONE), cs(NONE, TCMP)], 'std::multimap<{}, {}>'),
    (CMP | DEFC, [cs(HASH, NONE), cs(NONE, CMP)], 'std::unordered_map<{}, {}>'),
    (CMP | DEFC, [cs(HASH, NONE), cs(NONE, CMP)], 'std::unordered_multimap<{}, {}>'),
    (ALL , [cs(NONE, ALL), cs(NONE, NONE)], 'std::conditional_t<true, {}, {}>'),
    (ALL , [cs(NONE, NONE), cs(NONE, ALL)], 'std::conditional_t<false, {}, {}>'),
    (TCMP | DEFC, [cs(NONE, ALL), cs(NONE, ALL), cs(NONE, ALL)], 'std::tuple<{}, {}, {}>'),
    (TCMP | DEFC, [cs(NONE, ALL), cs(NONE, ALL), cs(NONE, ALL), cs(NONE, ALL)], 'std::tuple<{}, {}, {}, {}>'),
]

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        if re.match(r'^\[\d+\]$', sys.argv[1]):
            n = int(re.search(r'^\[(\d+)\]$', sys.argv[1]).group(1))
            print(craft_flag(n))
        else:
            print('Usage: python3 flag.py [N]')
            print('N is the number of flags to generate')
            print('If N is not specified, 10 flags will be generated')
            exit(0)
    else:
        print(craft_flag())
