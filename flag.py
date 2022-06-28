import math
import random
import sys
import re

NONE = 0
CMP  = 1 # type supports equality and inequelity operators
TCMP = 3 # type supports all comparison operators
HASH = 5 # type can be hashed
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

def craft_flag(n : int = 10):
    return f'`{cs(NONE, ALL)(0.2, NONE)} flag[{n}];`'

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
    (ALL , [], 'std::string'),
    (NONE, [], 'std::any'),
    # (NONE, [], 'null_type'),
    (ALL , [], 'bool'),
    (ALL , [], 'std::byte'),
    (ALL , [], 'signed char'),
    (ALL , [], 'unsigned char'),
    (CMP , [], 'std::strong_ordering'),
    (CMP , [], 'std::weak_ordering'),
    (CMP , [], 'std::partial_ordering'),
    (NONE, [], 'std::mutex'),
    (NONE, [], 'std::thread'),
    (CMP | HASH, [], 'std::bitset<262144>'),
    (ALL , [], 'std::chrono::seconds'),
    (NONE, [], 'FILE'),
    (NONE, [], 'std::ifstream'),
    (NONE, [], 'std::ofstream'),
    (ALL , [cs(NONE, ALL)], '{} *'),
    # (ALL , [cs(NONE, ALL)], '{}&'),
    # (ALL , [cs(NONE, ALL)], '{}[]'),
    # (ALL , [cs(NONE, ALL)], '{} const'),
    (TCMP, [cs(NONE, ALL)], 'std::deque<{}>'),
    (TCMP, [cs(TCMP, ALL)], 'std::set<{}>'),
    (TCMP, [cs(TCMP, ALL)], 'std::multiset<{}>'),
    (CMP , [cs(HASH, ALL)], 'std::unordered_set<{}>'),
    (CMP , [cs(HASH, ALL)], 'std::unordered_multiset<{}>'),
    (NONE, [cs(TCMP, ALL)], 'std::priority_queue<{}>'),
    (TCMP, [cs(NONE, ALL)], 'std::array<{}, 2>'),
    (TCMP, [cs(NONE, ALL)], 'std::array<{}, 3>'),
    (TCMP, [cs(NONE, ALL)], 'std::vector<{}>'),
    (ALL , [cs(NONE, NONE)], 'std::unique_ptr<{}>'),
    (ALL , [cs(NONE, NONE)], 'std::shared_ptr<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::weak_ptr<{}>'),
    # (NONE, [cs(NONE, ALL)], 'std::auto_ptr<{}>'),
    (ALL , [cs(NONE, ALL)], 'std::optional<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::span<{}>'),
    (NONE, [cs(NONE, ALL)], 'std::priority_queue<{0}, std::vector<{0}>, std::greater<{0}>>'),
    # (NONE, [cs(NONE, ALL)], 'std::chrono::time_point<std::chrono::high_resolution_clock, std::chrono::duration<{}, std::ratio<1, 1000000000>>>'),
    (NONE, [cs(TCMP, ALL)], '__gnu_pbds::tree<{0}, __gnu_pbds::null_type, std::less<{0}>, __gnu_pbds::rb_tree_tag, __gnu_pbds::tree_order_statistics_node_update>'),
    (TCMP, [cs(NONE, ALL), cs(NONE, ALL)], 'std::pair<{}, {}>'),
    (ALL , [cs(NONE, ALL), cs(NONE, ALL)], 'std::variant<{}, {}>'),
    (TCMP, [cs(TCMP, ALL), cs(NONE, ALL)], 'std::map<{}, {}>'),
    (TCMP, [cs(TCMP, ALL), cs(NONE, ALL)], 'std::multimap<{}, {}>'),
    (CMP , [cs(HASH, ALL), cs(NONE, ALL)], 'std::unordered_map<{}, {}>'),
    (CMP , [cs(HASH, ALL), cs(NONE, ALL)], 'std::unordered_multimap<{}, {}>'),
    (ALL , [cs(NONE, ALL), cs(NONE, ALL)], 'std::conditional_t<true, {}, {}>'),
    (ALL , [cs(NONE, ALL), cs(NONE, ALL)], 'std::conditional_t<false, {}, {}>'),
    (TCMP, [cs(NONE, ALL), cs(NONE, ALL), cs(NONE, ALL)], 'std::tuple<{}, {}, {}>'),
    (TCMP, [cs(NONE, ALL), cs(NONE, ALL), cs(NONE, ALL), cs(NONE, ALL)], 'std::tuple<{}, {}, {}, {}>')
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
