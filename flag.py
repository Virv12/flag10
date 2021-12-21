import math
import random

NONE = 0
CMP  = 1 # type supports equality and inequelity operators
TCMP = 3 # type supports all comparison operators
HASH = 4 # type can be hashed

TEMPLATES = [
    (TCMP | HASH, 0, 'int'),
    (TCMP | HASH, 0, 'size_t'),
    (TCMP | HASH, 0, 'uint32_t'),
    (TCMP | HASH, 0, 'int32_t'),
    (TCMP | HASH, 0, 'll'),
    (TCMP | HASH, 0, 'unsigned ll int'),
    (TCMP | HASH, 0, '__int128_t'),
    (TCMP | HASH, 0, 'uint64_t'),
    (TCMP | HASH, 0, 'int64_t'),
    (NONE       , 0, 'std::mt19937_64'),
    (NONE       , 0, 'std::string'),
    (NONE       , 0, 'std::any'),
    (NONE       , 0, 'null_type'),
    (NONE       , 0, 'bool'),
    (NONE       , 0, 'std::byte'),
    (NONE       , 0, 'signed char'),
    (NONE       , 0, 'unsigned char'),
    (NONE       , 0, 'std::strong_ordering'),
    (NONE       , 0, 'std::weak_ordering'),
    (NONE       , 0, 'std::partial_ordering'),
    (NONE       , 0, 'std::mutex'),
    (NONE       , 0, 'std::thread'),
    (NONE       , 0, 'std::bitset<262144>'),
    (NONE       , 0, 'std::chrono::duration'),
    (NONE       , 0, 'FILE'),
    (NONE       , 0, 'std::ifstream'),
    (NONE       , 0, 'std::ofstream'),
    (NONE       , 1, '{}*'),
    (NONE       , 1, '{}&'),
    (NONE       , 1, '{}[]'),
    (NONE       , 1, '{} const'),
    (NONE       , 1, 'std::deque<{}>'),
    (NONE       , 1, 'std::set<{}>'),
    (NONE       , 1, 'std::multiset<{}>'),
    (NONE       , 1, 'std::unordered_set<{}>'),
    (NONE       , 1, 'std::unordered_multiset<{}>'),
    (NONE       , 1, 'std::priority_queue<{}>'),
    (NONE       , 1, 'std::array<{}, 2>'),
    (NONE       , 1, 'std::array<{}, 3>'),
    (NONE       , 1, 'std::vector<{}>'),
    (NONE       , 1, 'std::unique_ptr<{}>'),
    (NONE       , 1, 'std::shared_ptr<{}>'),
    (NONE       , 1, 'std::weak_ptr<{}>'),
    (NONE       , 1, 'std::auto_ptr<{}>'),
    (NONE       , 1, 'std::optional<{}>'),
    (NONE       , 1, 'std::span<{}>'),
    (NONE       , 1, 'std::priority_queue<{0}, std::vector<{0}>, std::greater<{0}>>'),
    (NONE       , 1, 'std::chrono::time_point<std::chrono::high_resolution_clock, std::chrono::duration<{}, std::ratio<1, 1000000000>>>'),
    (NONE       , 1, '__gnu_pbds::tree<{0}, __gnu_pbds::null_type, std::less<{0}>, __gnu_pbds::rb_tree_tag, __gnu_pbds::tree_order_statistics_node_update>'),
    (NONE       , 2, 'std::pair<{}, {}>'),
    (NONE       , 2, 'std::variant<{}, {}>'),
    (NONE       , 2, 'std::map<{}, {}>'),
    (NONE       , 2, 'std::unordered_map<{}, {}>'),
    (NONE       , 2, 'std::multimap<{}, {}>'),
    (NONE       , 2, 'std::unordered_multimap<{}, {}>'),
    (NONE       , 2, 'std::conditional_t<true, {}, {}>'),
    (NONE       , 2, 'std::conditional_t<false, {}, {}>'),
    (NONE       , 3, 'std::tuple<{}, {}, {}>'),
    (NONE       , 4, 'std::tuple<{}, {}, {}, {}>')
]

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

def create_str(k):
    _, c, f = choose(k, TEMPLATES)
    return f.format(*(create_str(k - 0.10 - random.uniform(0.01, 0.1)) for i in range(c)))

def craft_flag():
    return f'`{create_str(0.2)} flag[10];`'

if __name__ == '__main__':
    print(craft_flag())
