package main

import (
	"bufio"
	"flag"
	"fmt"
	"math/big"
	"math/bits"
	"os"
	"sort"
)

const (
	d     int64 = 22270
	k     int64 = 2002
	bound int64 = 96000
)

var distances = [7][7]int64{
	{0, 22270, 22098, 16637, 9248, 8908, 8636},
	{22270, 0, 21488, 11397, 15138, 20698, 13746},
	{22098, 21488, 0, 10795, 14450, 13430, 20066},
	{16637, 11397, 10795, 0, 7395, 11135, 11049},
	{9248, 15138, 14450, 7395, 0, 5780, 5916},
	{8908, 20698, 13430, 11135, 5780, 0, 10744},
	{8636, 13746, 20066, 11049, 5916, 10744, 0},
}

type point struct {
	x int64
	y int64
}

type candidate struct {
	a int64
	b int64
	s uint64
}

// exactSqrt returns sqrt(n) for a square and zero otherwise. Newton iteration
// starts above the root and uses integer division only.
func exactSqrt(n uint64) uint64 {
	if n == 0 {
		return 0
	}
	x := uint64(1) << ((bits.Len64(n) + 1) / 2)
	for {
		y := (x + n/x) / 2
		if y >= x {
			break
		}
		x = y
	}
	if x*x == n {
		return x
	}
	return 0
}

func heron(a, b, c int64) uint64 {
	return uint64((a + b + c) * (a + b - c) * (a - b + c) * (-a + b + c))
}

func reconstructHeptagon() [7]point {
	var p [7]point
	p[0] = point{0, 0}
	p[1] = point{2 * d * d, 0}
	for j := 2; j < 7; j++ {
		a, b := distances[0][j], distances[1][j]
		h := heron(d, a, b)
		if h%uint64(k) != 0 {
			panic("characteristic mismatch")
		}
		s := exactSqrt(h / uint64(k))
		if s == 0 {
			panic("non-square characteristic quotient")
		}
		p[j] = point{a*a - b*b + d*d, int64(s)}
	}

	den := 4 * d * d
	for j := 3; j < 7; j++ {
		matches := 0
		var chosen int64
		for _, sign := range []int64{-1, 1} {
			dx := p[j].x - p[2].x
			dy := sign*p[j].y - p[2].y
			if dx*dx+k*dy*dy == den*distances[2][j]*distances[2][j] {
				matches++
				chosen = sign * p[j].y
			}
		}
		if matches != 1 {
			panic("orientation not uniquely forced")
		}
		p[j].y = chosen
	}
	return p
}

func boundedIntegralDistance(a, b point) (int64, bool) {
	dx, dy := a.x-b.x, a.y-b.y
	var x, y, n, divisor, q big.Int
	x.SetInt64(dx)
	x.Mul(&x, &x)
	y.SetInt64(dy)
	y.Mul(&y, &y)
	y.Mul(&y, big.NewInt(k))
	n.Add(&x, &y)
	if n.Sign() <= 0 {
		return 0, false
	}
	den := 4 * d * d
	divisor.SetInt64(den)
	var remainder big.Int
	q.QuoRem(&n, &divisor, &remainder)
	if remainder.Sign() != 0 || !q.IsUint64() || q.Uint64() > uint64(bound*bound) {
		return 0, false
	}
	r := exactSqrt(q.Uint64())
	return int64(r), r != 0
}

func matchesAll(h [7]point, a, b, s, side int64) bool {
	c := point{a*a - b*b + d*d, side * s}
	return pointMatchesAll(h, c)
}

func pointMatchesAll(h [7]point, c point) bool {
	for _, p := range h {
		if _, ok := boundedIntegralDistance(c, p); !ok {
			return false
		}
	}
	return true
}

func main() {
	emitPath := flag.String("emit-candidates", "", "write characteristic candidates as TSV")
	flag.Parse()
	var candidateFile *os.File
	var candidateWriter *bufio.Writer
	if *emitPath != "" {
		var err error
		candidateFile, err = os.Create(*emitPath)
		if err != nil {
			panic(err)
		}
		defer candidateFile.Close()
		candidateWriter = bufio.NewWriter(candidateFile)
		defer candidateWriter.Flush()
		fmt.Fprintln(candidateWriter, "a\tb\ts")
	}

	h := reconstructHeptagon()
	for i := 0; i < 7; i++ {
		for j := i + 1; j < 7; j++ {
			got, ok := boundedIntegralDistance(h[i], h[j])
			if !ok || got != distances[i][j] {
				panic(fmt.Sprintf("metric reconstruction failed at %d,%d", i, j))
			}
		}
	}

	var trianglePairs, characteristic2002, orientedCandidates uint64
	var degenerateCandidates, extensions uint64
	var candidates []candidate
	testDegenerate := func(x int64) {
		degenerateCandidates++
		c := point{2 * d * x, 0}
		if pointMatchesAll(h, c) {
			extensions++
			fmt.Printf("degenerate extension x=%d\n", x)
		}
	}

	// Collinear candidates are outside the characteristic reduction.
	for t := int64(1); t < d; t++ {
		testDegenerate(t)
	}
	for t := int64(1); t <= bound-d; t++ {
		testDegenerate(-t)
		testDegenerate(d + t)
	}

	// Put u=a+b-d, v=d+a-b, w=d-a+b. Then v+w=2d,
	// a=(u+v)/2, b=(u+w)/2, and the Heron product is
	// u*v*w*(2d+u). Taking v<=w is exactly a<=b.
	for v := int64(1); v <= d; v++ {
		w := 2*d - v
		firstU := int64(2)
		if v%2 == 1 {
			firstU = 1
		}
		lastU := 2*(bound-d) + v
		for u := firstU; u <= lastU; u += 2 {
			trianglePairs++
			// This Heron product is at most 4*d^2*bound^2, below 2^64
			// for the frozen constants d=22270 and bound=96000.
			hp := uint64(u) * uint64(v) * uint64(w) * uint64(2*d+u)
			if hp%uint64(k) != 0 {
				continue
			}
			s := exactSqrt(hp / uint64(k))
			if s == 0 {
				continue
			}
			characteristic2002++
			a, b := (u+v)/2, (u+w)/2
			if candidateWriter != nil {
				candidates = append(candidates, candidate{a, b, s})
			}
		forSwap:
			for swap := 0; swap < 2; swap++ {
				if swap == 1 && a == b {
					break forSwap
				}
				aa, bb := a, b
				if swap == 1 {
					aa, bb = b, a
				}
				for _, side := range []int64{-1, 1} {
					orientedCandidates++
					if matchesAll(h, aa, bb, int64(s), side) {
						extensions++
						fmt.Printf("extension a=%d b=%d s=%d side=%d\n", aa, bb, s, side)
					}
				}
			}
		}
	}
	if candidateWriter != nil {
		sort.Slice(candidates, func(i, j int) bool {
			if candidates[i].a != candidates[j].a {
				return candidates[i].a < candidates[j].a
			}
			if candidates[i].b != candidates[j].b {
				return candidates[i].b < candidates[j].b
			}
			return candidates[i].s < candidates[j].s
		})
		for _, c := range candidates {
			fmt.Fprintf(candidateWriter, "%d\t%d\t%d\n", c.a, c.b, c.s)
		}
	}

	fmt.Printf("triangle_pairs=%d\n", trianglePairs)
	fmt.Printf("distance_bound=%d\n", bound)
	fmt.Printf("characteristic_2002=%d\n", characteristic2002)
	fmt.Printf("oriented_candidates=%d\n", orientedCandidates)
	fmt.Printf("degenerate_candidates=%d\n", degenerateCandidates)
	fmt.Printf("extensions=%d\n", extensions)
	if extensions != 0 {
		panic("unexpected bounded extension")
	}
}
