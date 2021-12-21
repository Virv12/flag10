import math
import random

TEMPLATES = [
    (0, 'int'),
    (0, 'size_t'),
    (0, 'uint32_t'),
    (0, 'int32_t'),
    (0, 'll'),
    (0, 'unsigned ll int'),
    (0, '__int128_t'),
    (0, 'uint64_t'),
    (0, 'int64_t'),
    (0, 'std::mt19937_64'),
    (0, 'std::string'),
    (0, 'std::any'),
    (0, 'null_type'),
    (0, 'bool'),
    (0, 'std::byte'),
    (0, 'signed char'),
    (0, 'unsigned char'),
    (0, 'std::strong_ordering'),
    (0, 'std::weak_ordering'),
    (0, 'std::partial_ordering'),
    (0, 'std::mutex'),
    (0, 'std::thread'),
    (0, 'std::bitset<262144>'),
    (0, 'std::chrono::duration'),
    (0, 'FILE'),
    (0, 'std::ifstream'),
    (0, 'std::ofstream'),
    (1, '{}*'),
    (1, '{}&'),
    (1, '{}[]'),
    (1, '{} const'),
    (1, 'std::deque<{}>'),
    (1, 'std::set<{}>'),
    (1, 'std::multiset<{}>'),
    (1, 'std::unordered_set<{}>'),
    (1, 'std::unordered_multiset<{}>'),
    (1, 'std::priority_queue<{}>'),
    (1, 'std::array<{}, 2>'),
    (1, 'std::array<{}, 3>'),
	(1, 'std::vector<{}>'),
    (1, 'std::unique_ptr<{}>'),
    (1, 'std::shared_ptr<{}>'),
    (1, 'std::weak_ptr<{}>'),
    (1, 'std::auto_ptr<{}>'),
    (1, 'std::optional<{}>'),
    (1, 'std::span<{}>'),
    (1, 'std::priority_queue<{0}, std::vector<{0}>, std::greater<{0}>>'),
    (1, 'std::chrono::time_point<std::chrono::high_resolution_clock, std::chrono::duration<{}, std::ratio<1, 1000000000>>>'),
    (1, '__gnu_pbds::tree<{0}, __gnu_pbds::null_type, std::less<{0}>, __gnu_pbds::rb_tree_tag, __gnu_pbds::tree_order_statistics_node_update>'),
    (2, 'std::pair<{}, {}>'),
    (2, 'std::variant<{}, {}>'),
	(2, 'std::map<{}, {}>'),
	(2, 'std::unordered_map<{}, {}>'),
	(2, 'std::multimap<{}, {}>'),
	(2, 'std::unordered_multimap<{}, {}>'),
    (2, 'std::conditional_t<true, {}, {}>'),
    (2, 'std::conditional_t<false, {}, {}>'),
    (3, 'std::tuple<{}, {}, {}>'),
    (4, 'std::tuple<{}, {}, {}, {}>')
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
    c, f = choose(k, TEMPLATES)
    return f.format(*(create_str(k - 0.10 - random.uniform(0.01, 0.1)) for i in range(c)))

def craft_flag():
    return f'`{create_str(0.2)} flag[10];`'

if __name__ == '__main__':
    print(craft_flag())
