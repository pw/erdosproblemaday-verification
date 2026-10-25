/* Breakout search for Erdos #813.  Reuse the audited incremental state
 * engine, but give both violated K5 and triangle-free-7 constraints dynamic
 * GLS weights. */
#define main original_tabu_main
#include "/home/exedev/MathDyad/erdos813/tabu.c"
#undef main

static uint32_t k5w[N5];
static long long k5wsum;

static long long k5_weight_delta(int p) {
    const uint16_t *I5 = p5i + (size_t)p * L5;
    long long delta = 0;
    int a = pa_[p], b = pb_[p];
    if (!((adj[a] >> b) & 1)) {
        for (int j = 0; j < L5; j++) {
            int f = I5[j];
            if (m5[f] == 1) delta += k5w[f];
        }
    } else {
        for (int j = 0; j < L5; j++) {
            int f = I5[j];
            if (m5[f] == 0) delta -= k5w[f];
        }
    }
    return delta;
}

static void recompute_k5wsum(void) {
    k5wsum = 0;
    for (int f = 0; f < N5; f++) if (m5[f] == 0) k5wsum += k5w[f];
}

int main(int argc, char **argv) {
    uint64_t seed = 1;
    double timeout = 120;
    int base7 = 1, base5 = 1, tmin = 7, tspan = 17;
    int stag_limit = 6000, kick = 8, smooth_every = 1200;
    const char *seedfile = NULL, *outpath = NULL;

    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--seed")) seed = strtoull(argv[++i], NULL, 10);
        else if (!strcmp(argv[i], "--timeout")) timeout = atof(argv[++i]);
        else if (!strcmp(argv[i], "--seedfile")) seedfile = argv[++i];
        else if (!strcmp(argv[i], "--out")) outpath = argv[++i];
        else if (!strcmp(argv[i], "--base7")) base7 = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--base5")) base5 = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--tmin")) tmin = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--tspan")) tspan = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--stag")) stag_limit = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--kick")) kick = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--smooth")) smooth_every = atoi(argv[++i]);
        else { fprintf(stderr, "unknown option %s\n", argv[i]); return 2; }
    }
    if (!seedfile) { fprintf(stderr, "--seedfile required\n"); return 2; }

    build_tables();
    rng_s = seed ? seed : 1;
    for (int i = 0; i < N7; i++) w[i] = (uint32_t)base7;
    for (int f = 0; f < N5; f++) k5w[f] = (uint32_t)base5;
    if (read_maskfile(seedfile, adj)) return 2;
    recompute_state();
    recompute_k5wsum();

    FILE *out = outpath ? fopen(outpath, "a") : stderr;
    if (!out) return 2;
    double t0 = now_sec();
    long long iter = 0, tabu[NPAIRS];
    memset(tabu, 0, sizeof tabu);
    int bumps = 0, kicks = 0, stag = 0;
    int best_sum = tf + k5, best_tf0 = k5 == 0 ? tf : (1 << 30);
    uint32_t best_adj[N], best_tf0_adj[N];
    memcpy(best_adj, adj, sizeof adj);
    if (k5 == 0) memcpy(best_tf0_adj, adj, sizeof adj);
    fprintf(out, "# both seed=%llu base7=%d base5=%d start tf=%d k5=%d\n",
            (unsigned long long)seed, base7, base5, tf, k5);

    while (1) {
        if ((iter & 255) == 0 && now_sec() - t0 >= timeout) break;
        iter++;
        long long best_delta = (1LL << 62);
        int chosen = -1, ties = 0;
        for (int p = 0; p < NPAIRS; p++) {
            int dtf, dk;
            long long delta = delta_flip(p, &dtf, &dk) + k5_weight_delta(p);
            int aspir = tf + dtf + k5 + dk < best_sum;
            if (tabu[p] >= iter && !aspir) continue;
            if (delta < best_delta) { best_delta = delta; chosen = p; ties = 1; }
            else if (delta == best_delta && rndn(++ties) == 0) chosen = p;
        }
        if (chosen < 0) { memset(tabu, 0, sizeof tabu); continue; }
        long long kd = k5_weight_delta(chosen);
        commit_flip(chosen);
        k5wsum += kd;
        tabu[chosen] = iter + tmin + rndn(tspan);

        int raw = tf + k5;
        if (raw < best_sum) {
            best_sum = raw; memcpy(best_adj, adj, sizeof adj); stag = 0;
            fprintf(out, "RAW tf=%d k5=%d sum=%d iter=%lld t=%.1f\n",
                    tf, k5, raw, iter, now_sec() - t0);
        } else stag++;
        if (k5 == 0 && tf < best_tf0) {
            best_tf0 = tf; memcpy(best_tf0_adj, adj, sizeof adj); stag = 0;
            fprintf(out, "FEAS tf=%d iter=%lld t=%.1f", tf, iter, now_sec() - t0);
            print_masks(out, adj, "");
        }
        if (tf == 0 && k5 == 0) {
            print_masks(out, adj, "WITNESS");
            print_masks(stdout, adj, "WITNESS");
            if (out != stderr) fclose(out);
            return 0;
        }

        if (best_delta >= 0) {
            for (int i = 0; i < N7; i++) if (tcnt[i] == 0) { w[i]++; sumw++; }
            for (int f = 0; f < N5; f++) if (m5[f] == 0) { k5w[f]++; k5wsum++; }
            bumps++;
            if (smooth_every > 0 && bumps % smooth_every == 0) {
                for (int i = 0; i < N7; i++) w[i] = (w[i] + base7) / 2;
                for (int f = 0; f < N5; f++) k5w[f] = (k5w[f] + base5) / 2;
                recompute_state(); recompute_k5wsum();
            }
        }

        if (stag > stag_limit) {
            memcpy(adj, best_adj, sizeof adj);
            for (int r = 0; r < kick; r++) {
                int p = rndn(NPAIRS);
                adj[pa_[p]] ^= 1u << pb_[p];
                adj[pb_[p]] ^= 1u << pa_[p];
            }
            recompute_state(); recompute_k5wsum();
            memset(tabu, 0, sizeof tabu); stag = 0; kicks++;
        }
    }

    fprintf(out, "END best_sum=%d best_feas_tf=%d iter=%lld bumps=%d kicks=%d t=%.1f\n",
            best_sum, best_tf0 == (1 << 30) ? -1 : best_tf0, iter, bumps,
            kicks, now_sec() - t0);
    print_masks(out, best_adj, "BESTRAW");
    if (best_tf0 < (1 << 30)) print_masks(out, best_tf0_adj, "BESTFEAS");
    if (out != stderr) fclose(out);
    return 3;
}
