#!/usr/bin/env python3
"""Independent exhaustive audit of the new c11 q=2 and q=3 kernels."""

from functools import lru_cache
from fractions import Fraction
from itertools import combinations, permutations


Q2_TABLE = (
    ("11111/11000/10100/00011", "00,01,02,10,11", "00,03,04,33,34"),
    ("11110/11100/10001/00011", "00,01,02,10,11", "00,03,10,20,24"),
    ("11110/11100/00011/00011", "00,01,02,10,11", "03,23,24,33,34"),
    ("11110/11001/10100/00011", "00,01,02,10,11", "00,03,10,14,33"),
    ("11110/11001/10001/00110", "00,01,02,03,10", "00,10,14,20,24"),
    ("11110/11001/00110/00101", "00,01,02,10,11", "02,03,14,22,23"),
    ("11110/11001/00101/00011", "00,01,10,11,14", "02,03,14,22,24"),
    ("11100/11100/10011/00011", "00,01,02,10,11", "00,10,20,23,24"),
    ("11100/11010/10101/00011", "00,01,02,10,11", "00,10,13,20,24"),
    ("11100/11010/10001/00111", "00,01,02,10,11", "00,10,13,20,24"),
    ("11100/11010/00111/00101", "00,01,02,10,11", "02,13,22,23,24"),
)

Q3_3X5_TABLE = (
    ("11111/11110/10001", "00,01,10,11", "00,04,10,20", "02,03,12,13"),
    ("11111/11100/10011", "00,01,10,11", "00,02,10,12", "03,04,23,24"),
    ("11110/11101/10011", "00,01,10,11", "00,02,10,12", "03,14,23,24"),
)

Q3_4X4_TABLE = (
    ("1111/1110/1100/1001", "00,01,02,10", "00,01,11,20", "00,03,30,33"),
    ("1111/1110/1100/0011", "00,01,02,10", "00,01,11,20", "02,03,32,33"),
    ("1111/1110/1001/1001", "00,01,02,10", "00,03,20,23", "00,03,30,33"),
    ("1111/1110/1001/0101", "00,01,02,10", "00,03,20,23", "01,03,11,31"),
    ("1110/1110/1101/1001", "00,01,02,10", "00,01,11,20", "20,23,30,33"),
    ("1110/1110/1101/0011", "00,01,02,10", "00,01,20,21", "12,23,32,33"),
    ("1110/1101/1100/1011", "00,01,02,10", "00,01,20,21", "10,13,30,33"),
    ("1110/1101/1011/0110", "00,01,02,10", "01,02,22,31", "10,13,20,23"),
)


def edge_bit(i, j, right):
    return 1 << (i * right + j)


def parse_graph(text):
    rows = text.split("/")
    left, right = len(rows), len(rows[0])
    mask = sum(
        edge_bit(i, j, right)
        for i, row in enumerate(rows)
        for j, value in enumerate(row)
        if value == "1"
    )
    return mask, left, right


def parse_block(text, right):
    return sum(edge_bit(int(item[0]), int(item[1]), right) for item in text.split(","))


@lru_cache(maxsize=None)
def row_permutations(left):
    return tuple(permutations(range(left)))


def canonical(mask, left, right):
    best = None
    for row_order in row_permutations(left):
        columns = tuple(
            sorted(
                sum(
                    1 << new_i
                    for new_i, old_i in enumerate(row_order)
                    if mask & edge_bit(old_i, j, right)
                )
                for j in range(right)
            )
        )
        best = columns if best is None or columns < best else best
    return best


@lru_cache(maxsize=None)
def endpoint_filters(left, right):
    records = []
    for row_mask in range(1 << left):
        for col_mask in range(1 << right):
            edge_filter = sum(
                edge_bit(i, j, right)
                for i in range(left)
                for j in range(right)
                if row_mask >> i & 1 and col_mask >> j & 1
            )
            records.append(
                (
                    edge_filter,
                    row_mask.bit_count() + col_mask.bit_count(),
                    row_mask == (1 << left) - 1 and col_mask == (1 << right) - 1,
                )
            )
    return tuple(records)


def degrees(mask, left, right):
    return (
        tuple(sum(bool(mask & edge_bit(i, j, right)) for j in range(right)) for i in range(left)),
        tuple(sum(bool(mask & edge_bit(i, j, right)) for i in range(left)) for j in range(right)),
    )


def is_critical(mask, left, right, defect):
    if mask.bit_count() - left - right != defect:
        return False
    row_degrees, col_degrees = degrees(mask, left, right)
    if min(row_degrees + col_degrees) < 2:
        return False
    return all(
        is_full or (mask & edge_filter).bit_count() - vertex_count < defect
        for edge_filter, vertex_count, is_full in endpoint_filters(left, right)
    )


def level_demands(mask, left, right):
    records = []
    for edge_filter, vertex_count, _ in endpoint_filters(left, right):
        level = mask & edge_filter
        demand = max(0, level.bit_count() - vertex_count)
        if demand:
            records.append((level, demand))
    return tuple(records)


def certificate_valid(mask, left, right, blocks):
    return all(
        sum((block & level) == block for block in blocks) >= demand
        for level, demand in level_demands(mask, left, right)
    )


def collision_safe(mask, left, right, block):
    for i in range(left):
        incident = sum(edge_bit(i, j, right) for j in range(right))
        if (block | (mask & ~incident)).bit_count() < 5:
            return False
    for j in range(right):
        incident = sum(edge_bit(i, j, right) for i in range(left))
        if (block | (mask & ~incident)).bit_count() < 5:
            return False
    return True


def candidate_blocks(mask, size):
    edge_bits = [1 << bit for bit in range(mask.bit_length()) if mask >> bit & 1]
    return tuple(sum(chosen) for chosen in combinations(edge_bits, size))


def discover_certificate(mask, left, right, defect):
    demands = level_demands(mask, left, right)
    demand_masks = {
        d: sum(1 << index for index, (_, value) in enumerate(demands) if value >= d)
        for d in range(1, defect + 1)
    }
    size = 5 if defect == 2 else 4
    candidates = candidate_blocks(mask, size)
    coverage = {
        block: sum(1 << index for index, (level, _) in enumerate(demands) if block & level == block)
        for block in candidates
    }
    if defect == 2:
        for ai, a in enumerate(candidates):
            for b in candidates[ai + 1 :]:
                if (a | b).bit_count() < 6:
                    continue
                if demand_masks[1] & ~(coverage[a] | coverage[b]):
                    continue
                if demand_masks[2] & ~(coverage[a] & coverage[b]):
                    continue
                return a, b
    else:
        for ai, a in enumerate(candidates):
            for bi in range(ai + 1, len(candidates)):
                b = candidates[bi]
                if (a | b).bit_count() < 6:
                    continue
                for c in candidates[bi + 1 :]:
                    if min((a | c).bit_count(), (b | c).bit_count()) < 6:
                        continue
                    if (a | b | c).bit_count() < 9:
                        continue
                    one = coverage[a] | coverage[b] | coverage[c]
                    two = (coverage[a] & coverage[b]) | (coverage[a] & coverage[c]) | (coverage[b] & coverage[c])
                    three = coverage[a] & coverage[b] & coverage[c]
                    if demand_masks[1] & ~one or demand_masks[2] & ~two or demand_masks[3] & ~three:
                        continue
                    return a, b, c
    return None


def enumerate_specification(defect, left, right):
    total_edges = left * right
    labelled = 0
    classes = {}
    for chosen in combinations(range(total_edges), 11):
        mask = sum(1 << bit for bit in chosen)
        if not is_critical(mask, left, right, defect):
            continue
        labelled += 1
        classes.setdefault(canonical(mask, left, right), mask)
    discovered = {}
    for form, mask in classes.items():
        certificate = discover_certificate(mask, left, right, defect)
        assert certificate is not None
        assert certificate_valid(mask, left, right, certificate)
        if defect == 2:
            assert all(block.bit_count() == 5 for block in certificate)
            assert (certificate[0] | certificate[1]).bit_count() >= 6
        else:
            assert all(block.bit_count() == 4 for block in certificate)
            assert all((a | b).bit_count() >= 6 for a, b in combinations(certificate, 2))
            assert (certificate[0] | certificate[1] | certificate[2]).bit_count() >= 9
        discovered[form] = certificate
    return labelled, classes, discovered


def audit_frozen_tables():
    tables = (
        (2, 4, 5, Q2_TABLE),
        (3, 3, 5, Q3_3X5_TABLE),
        (3, 4, 4, Q3_4X4_TABLE),
    )
    checked = 0
    frozen_forms = {}
    for defect, left, right, table in tables:
        forms = set()
        for row in table:
            mask, actual_left, actual_right = parse_graph(row[0])
            assert (actual_left, actual_right) == (left, right)
            blocks = tuple(parse_block(text, right) for text in row[1:])
            assert is_critical(mask, left, right, defect)
            assert all(block & ~mask == 0 for block in blocks)
            assert certificate_valid(mask, left, right, blocks)
            assert all(collision_safe(mask, left, right, block) for block in blocks)
            if defect == 2:
                assert all(block.bit_count() == 5 for block in blocks)
                assert (blocks[0] | blocks[1]).bit_count() >= 6
            else:
                assert all(block.bit_count() == 4 for block in blocks)
                assert all((a | b).bit_count() >= 6 for a, b in combinations(blocks, 2))
                assert (blocks[0] | blocks[1] | blocks[2]).bit_count() >= 9
            form = canonical(mask, left, right)
            assert form not in forms
            forms.add(form)
            checked += 1
        frozen_forms[defect, left, right] = forms
    return checked, frozen_forms


def multiples(maximum, start, divisor):
    return {
        value
        for value in range(start + 1, start + 2 * maximum)
        if value % divisor == 0
    }


def audit_progression_lemmas(limit=90):
    q2_pairs = 0
    q3_pairs = 0
    for maximum in range(4, limit + 1):
        for twice_start in range(0, 4 * maximum + 1):
            # Scaling by two includes integral and half-integral phases while
            # retaining exact integer interval points.
            start = Fraction(twice_start, 2)
            integer_points = range(int(start) - 1, int(start + 2 * maximum) + 2)

            def z(divisor):
                return {
                    value
                    for value in integer_points
                    if start < value < start + 2 * maximum and value % divisor == 0
                }

            sets = {d: z(d) for d in range(1, maximum // 4 + 1)}
            q2 = [d for d in range(1, maximum // 5 + 1) if len(sets[d]) >= 9]
            for d, e in combinations(q2, 2):
                if len(sets[d] | sets[e]) <= 10:
                    raise AssertionError(("q2", maximum, start, d, e))
                q2_pairs += 1
            q3 = [d for d in range(1, maximum // 4 + 1) if len(sets[d]) >= 7]
            for d, e in combinations(q3, 2):
                if len(sets[d] | sets[e]) <= 10:
                    raise AssertionError(("q3", maximum, start, d, e))
                q3_pairs += 1
    return q2_pairs, q3_pairs


def main():
    frozen_count, frozen_forms = audit_frozen_tables()
    expected = {
        (2, 4, 5): (13560, 11),
        (3, 3, 5): (390, 3),
        (3, 4, 4): (2304, 8),
    }
    summaries = {}
    for specification, target in expected.items():
        labelled, classes, discovered = enumerate_specification(*specification)
        assert (labelled, len(classes)) == target
        assert set(classes) == frozen_forms[specification]
        assert set(discovered) == set(classes)
        summaries[specification] = (labelled, len(classes))
    progression_pairs = audit_progression_lemmas()
    print(
        "C11_NEW_KERNELS_AUDIT=PASS",
        f"frozen_classes={frozen_count}",
        f"enumeration={summaries}",
        f"progression_pairs={progression_pairs}",
    )
    print("STATUS=NEW_KERNEL_COMPONENT full_c11_integration=SEPARATE_CANDIDATE")


if __name__ == "__main__":
    main()
