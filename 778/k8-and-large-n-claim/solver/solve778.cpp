// solve778.cpp — exact solver for Erdős #778, second game: the (1:2)-biased clique game on K_n.
// Alice (red) claims 1 edge, Bob (blue) then claims 2 (successively; order irrelevant), ...; Alice moves first.
// Terminal: all edges claimed. Bob wins iff omega(blue) > omega(red), i.e. alpha(red) > omega(red).
// mode=triangle: Maker-Breaker (1:2) triangle game — Alice wins iff she ever owns a red triangle (stronger Bob objective:
// a Bob win here implies a Bob win in the clique game for n >= 6 by R(3,3) <= 6).
// Exact backward induction with (a) two monotone cutoffs, (b) transposition table keyed by a canonical form of the
// 3-edge-coloured K_n (colour refinement + exhaustive orderings inside cells), (c) a strategy certificate for the winner.
// Written 2026-10-13 (erdos cron seat). Independent of the July 2026 Python engine except for the problem statement.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
typedef unsigned __int128 u128;
struct Hash128 { size_t operator()(u128 x) const { u64 lo=(u64)x, hi=(u64)(x>>64); return (lo*0x9E3779B97F4A7C15ULL) ^ ((hi+0x7F4A7C159E3779B9ULL)*0xC2B2AE3D27D4EB4FULL); } };
static int n, m;
static int eidx[10][10];
static int eu[45], ev[45];
static u64 FULL;
static u64 cliqueMask[1024];
static int pc8[1024];
static int ALICE_TOTAL; // edges Alice gets in total
enum Mode { CLIQUE, TRIANGLE };
static Mode mode = CLIQUE;
static bool REVERSE = false, NOCUT = false;

static inline int pc(u64 x) { return __builtin_popcountll(x); }
static inline int ecol(u64 R, u64 B, int e) { return (R >> e & 1) ? 1 : ((B >> e & 1) ? 2 : 0); }

static int omegaOf(u64 mask) { // clique number of the graph with edge set mask (>=1 when n>=1)
    int best = n ? 1 : 0;
    for (int S = 1; S < (1 << n); S++) {
        if (pc8[S] <= best) continue;
        if ((cliqueMask[S] & mask) == cliqueMask[S]) best = pc8[S];
    }
    return best;
}
// largest clique Alice can still complete: no blue edge inside S, and at most k free edges inside S
static int omegaMaxBudget(u64 R, u64 B, int k) {
    int best = n ? 1 : 0;
    for (int S = 1; S < (1 << n); S++) {
        if (pc8[S] <= best) continue;
        u64 cm = cliqueMask[S];
        if (cm & B) continue;
        if (pc(cm & ~R) <= k) best = pc8[S];
    }
    return best;
}
static bool triangleCompletable(u64 R, u64 B, int k) {
    for (int S = 1; S < (1 << n); S++) {
        if (pc8[S] != 3) continue;
        u64 cm = cliqueMask[S];
        if (cm & B) continue;
        if (pc(cm & ~R) <= k) return true;
    }
    return false;
}

// ---------- canonical form ----------
struct CanonRes { u128 code; int lab[10]; };
static long long canonCalls = 0, canonOrderings = 0;

static CanonRes canon(u64 R, u64 B) {
    canonCalls++;
    int c[10]; for (int v = 0; v < n; v++) c[v] = 0;
    int ncls = 1;
    while (true) {
        vector<vector<int>> key(n);
        for (int v = 0; v < n; v++) {
            vector<int> nb; nb.reserve(n - 1);
            for (int u = 0; u < n; u++) if (u != v) nb.push_back(ecol(R, B, eidx[v][u]) * 64 + c[u]);
            sort(nb.begin(), nb.end());
            key[v].push_back(c[v]);
            key[v].insert(key[v].end(), nb.begin(), nb.end());
        }
        vector<int> order(n); iota(order.begin(), order.end(), 0);
        sort(order.begin(), order.end(), [&](int a, int b) { return key[a] < key[b]; });
        int nc[10]; int k = 0;
        for (int i = 0; i < n; i++) { if (i > 0 && key[order[i]] != key[order[i - 1]]) k++; nc[order[i]] = k; }
        int newcls = k + 1;
        for (int v = 0; v < n; v++) c[v] = nc[v];
        if (newcls == ncls) break;
        ncls = newcls;
    }
    // cells in colour order
    vector<vector<int>> cells(ncls);
    for (int v = 0; v < n; v++) cells[c[v]].push_back(v);
    for (auto& cl : cells) sort(cl.begin(), cl.end());
    // enumerate all orderings inside cells (odometer over permutations)
    CanonRes best; best.code = ~(u128)0;
    int lab[10];
    vector<int> cellStart(ncls); { int p = 0; for (int i = 0; i < ncls; i++) { cellStart[i] = p; p += cells[i].size(); } }
    // recursive odometer
    function<void(int)> rec = [&](int ci) {
        if (ci == ncls) {
            canonOrderings++;
            u128 code = 0;
            for (int e = 0; e < m; e++) {
                int col = ecol(R, B, e); if (!col) continue;
                int a = lab[eu[e]], b = lab[ev[e]];
                code |= (u128)col << (2 * eidx[a][b]);
            }
            if (code < best.code) { best.code = code; memcpy(best.lab, lab, sizeof(lab)); }
            return;
        }
        vector<int> cl = cells[ci];
        do {
            for (size_t i = 0; i < cl.size(); i++) lab[cl[i]] = cellStart[ci] + (int)i;
            rec(ci + 1);
        } while (next_permutation(cl.begin(), cl.end()));
    };
    rec(0);
    return best;
}

// ---------- transposition table ----------
struct Entry { u64 R, B; uint8_t val; int8_t m1, m2; }; // representative state, value (1 = Bob wins), winning move(s) in rep coords
static unordered_map<u128, Entry, Hash128> memo;
static long long nodes = 0, cutBob = 0, cutAlice = 0;
static chrono::steady_clock::time_point T0;

static bool aliceWinsNow(u64 R, u64 B) {
    if (mode == TRIANGLE) return omegaOf(R) >= 3;
    return omegaOf(R) >= omegaOf(~R & FULL); // alpha(R) = omega(complement); alpha only decreases, omega only increases
}
static bool bobWinsNow(u64 R, u64 B, int kA) {
    if (mode == TRIANGLE) return !triangleCompletable(R, B, kA);
    int alphaMin = omegaOf(B);           // alpha(final R) >= omega(B)
    int omegaMax = omegaMaxBudget(R, B, kA);
    return alphaMin > omegaMax;
}

// score free edges for move ordering
static void edgeScores(u64 R, u64 B, int kA, int sc[45]) {
    for (int e = 0; e < m; e++) sc[e] = 0;
    int om = omegaMaxBudget(R, B, kA);
    for (int S = 1; S < (1 << n); S++) {
        if (pc8[S] < max(2, om - 1)) continue;
        u64 cm = cliqueMask[S];
        if (cm & B) continue;
        u64 fr = cm & ~R;
        if (pc(fr) > kA) continue;
        int w = (pc8[S] == om) ? 4 : 1;
        for (int e = 0; e < m; e++) if (fr >> e & 1) sc[e] += w;
    }
}

static bool solve(u64 R, u64 B, bool aliceToMove) {
    nodes++;
    if ((nodes & ((1 << 20) - 1)) == 0) {
        double t = chrono::duration<double>(chrono::steady_clock::now() - T0).count();
        fprintf(stderr, "  ... nodes=%lld memo=%zu canon=%lld orderings=%lld cutBob=%lld cutAlice=%lld t=%.0fs\n",
                nodes, memo.size(), canonCalls, canonOrderings, cutBob, cutAlice, t);
    }
    int kA = ALICE_TOTAL - pc(R);
    u64 freeM = FULL & ~(R | B);
    if (freeM == 0) { // terminal
        if (mode == TRIANGLE) return omegaOf(R) <= 2;
        return omegaOf(~R & FULL) > omegaOf(R);
    }
    if (!NOCUT) {
        if (aliceWinsNow(R, B)) { cutAlice++; return false; }
        if (bobWinsNow(R, B, kA)) { cutBob++; return true; }
    }
    CanonRes cr = canon(R, B);
    auto it = memo.find(cr.code);
    if (it != memo.end()) return it->second.val;
    int sc[45]; edgeScores(R, B, kA, sc);
    vector<int> fe; for (int e = 0; e < m; e++) if (freeM >> e & 1) fe.push_back(e);
    Entry ent; ent.R = R; ent.B = B; ent.m1 = ent.m2 = -1;
    bool res;
    if (aliceToMove) {
        sort(fe.begin(), fe.end(), [&](int a, int b) { return REVERSE ? sc[a] < sc[b] : sc[a] > sc[b]; });
        res = true;
        for (int e : fe) {
            if (!solve(R | (1ULL << e), B, false)) { res = false; ent.m1 = e; break; }
        }
    } else {
        vector<pair<int,int>> prs;
        for (size_t i = 0; i < fe.size(); i++) for (size_t j = i + 1; j < fe.size(); j++) prs.push_back({fe[i], fe[j]});
        sort(prs.begin(), prs.end(), [&](const pair<int,int>& a, const pair<int,int>& b) {
            return REVERSE ? sc[a.first] + sc[a.second] < sc[b.first] + sc[b.second] : sc[a.first] + sc[a.second] > sc[b.first] + sc[b.second]; });
        res = false;
        for (auto& p : prs) {
            if (solve(R, B | (1ULL << p.first) | (1ULL << p.second), true)) { res = true; ent.m1 = p.first; ent.m2 = p.second; break; }
        }
    }
    ent.val = res ? 1 : 0;
    memo[cr.code] = ent;
    return res;
}

// ---------- certificate ----------
// Bob wins: for every Bob-to-move node in Bob's winning tree, emit "rep_R rep_B e f" (reply in the representative's coordinates).
// Alice wins: for every Alice-to-move node in Alice's winning tree, emit "rep_R rep_B e".
static set<u128> emitted;
static long long certLines = 0;
static void emitTree(u64 R, u64 B, bool aliceToMove, bool bobWon, FILE* f) {
    int kA = ALICE_TOTAL - pc(R);
    u64 freeM = FULL & ~(R | B);
    if (freeM == 0) return;
    if (!NOCUT) {
        if (aliceWinsNow(R, B)) return;      // (cannot occur inside the winner's tree when bobWon; marks Alice's terminal win otherwise)
        if (bobWinsNow(R, B, kA)) return;    // cutoff nodes: the checker re-derives the cutoff itself
    }
    CanonRes cr = canon(R, B);
    if (emitted.count(cr.code)) return;
    emitted.insert(cr.code);
    auto it = memo.find(cr.code);
    if (it == memo.end()) { fprintf(stderr, "CERT: missing memo entry at a tree node\n"); exit(3); }
    const Entry& ent = it->second;
    // work in the representative's coordinates
    u64 rR = ent.R, rB = ent.B; u64 rfree = FULL & ~(rR | rB);
    if (aliceToMove) {
        if (bobWon) {
            for (int e = 0; e < m; e++) if (rfree >> e & 1) emitTree(rR | (1ULL << e), rB, false, bobWon, f);
        } else {
            fprintf(f, "%llu %llu %d\n", rR, rB, ent.m1); certLines++;
            emitTree(rR | (1ULL << ent.m1), rB, false, bobWon, f);
        }
    } else {
        if (bobWon) {
            fprintf(f, "%llu %llu %d %d\n", rR, rB, ent.m1, ent.m2); certLines++;
            emitTree(rR, rB | (1ULL << ent.m1) | (1ULL << ent.m2), true, bobWon, f);
        } else {
            vector<int> fe; for (int e = 0; e < m; e++) if (rfree >> e & 1) fe.push_back(e);
            for (size_t i = 0; i < fe.size(); i++) for (size_t j = i + 1; j < fe.size(); j++)
                emitTree(rR, rB | (1ULL << fe[i]) | (1ULL << fe[j]), true, bobWon, f);
        }
    }
}

int main(int argc, char** argv) {
    n = 8; const char* certPath = nullptr;
    for (int i = 1; i < argc; i++) {
        string a = argv[i];
        if (a == "--n") { n = atoi(argv[++i]); if (n > 10) { fprintf(stderr, "n<=10\n"); return 2; } }
        else if (a == "--mode") { string v = argv[++i]; mode = (v == "triangle") ? TRIANGLE : CLIQUE; }
        else if (a == "--cert") certPath = argv[++i];
        else if (a == "--reverse") REVERSE = true;
        else if (a == "--nocut") NOCUT = true;
    }
    m = 0;
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) { eidx[i][j] = eidx[j][i] = m; eu[m] = i; ev[m] = j; m++; }
    FULL = (m == 64) ? ~0ULL : ((1ULL << m) - 1);
    for (int S = 0; S < (1 << n); S++) {
        pc8[S] = __builtin_popcount(S); u64 cm = 0;
        for (int i = 0; i < n; i++) if (S >> i & 1) for (int j = i + 1; j < n; j++) if (S >> j & 1) cm |= 1ULL << eidx[i][j];
        cliqueMask[S] = cm;
    }
    ALICE_TOTAL = (m + 2) / 3; // Alice moves at plies 1,4,7,...: ceil(m/3)
    T0 = chrono::steady_clock::now();
    bool bob = solve(0, 0, true);
    double t = chrono::duration<double>(chrono::steady_clock::now() - T0).count();
    printf("n=%d mode=%s edges=%d aliceEdges=%d RESULT: %s\n", n, mode == TRIANGLE ? "triangle" : "clique", m, ALICE_TOTAL,
           bob ? "BOB WINS" : "ALICE WINS");
    printf("nodes=%lld memo=%zu canonCalls=%lld orderings=%lld cutBob=%lld cutAlice=%lld time=%.1fs\n",
           nodes, memo.size(), canonCalls, canonOrderings, cutBob, cutAlice, t);
    if (certPath) {
        FILE* f = fopen(certPath, "w");
        fprintf(f, "# erdos778 certificate n=%d mode=%s winner=%s aliceEdges=%d edges=%d edgeorder=lex(i<j)\n", n,
                mode == TRIANGLE ? "triangle" : "clique", bob ? "bob" : "alice", ALICE_TOTAL, m);
        emitTree(0, 0, true, bob, f);
        fclose(f);
        printf("certificate: %lld lines -> %s\n", certLines, certPath);
    }
    return bob ? 0 : 1;
}
