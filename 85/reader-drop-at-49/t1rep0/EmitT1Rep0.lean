import Proofs.Erdos85OrderFortyNineSevenHighCnf
import Proofs.Erdos85OrderFortyNineSevenHighCanonicalCensus

/-! Our emitter (erdos cron seat 2026-10-20): DIMACS for the cell checked by
`sevenHighT1Rep0_check`, rendered from the authors' live Lean definitions, plus a
runtime check that the DIMACS clause array maps clausewise to exactly
`(orderFortyNineGeneratedH7SatCnf (representativeMasks blocks index)).clauses`. -/

open Erdos85 Std Sat

def clauseLine (clause : DimacsClause) : String :=
  String.intercalate " " (clause.map toString) ++ " 0"

def main (args : List String) : IO UInt32 := do
  let blocks := (args.getD 0 "1").toNat!
  let index := (args.getD 1 "0").toNat!
  let masks := OrderFortyNineSevenHighCensus.representativeMasks blocks index
  let arr : Array DimacsClause :=
    orderFortyNineH7FixedClauses masks ++ orderFortyNineC4Clauses ++
    (orderFortyNineDegreeBlocks 7).clauses ++ orderFortyNineH7PartitionClauses masks
  let same := dimacsFormulaToSatClauses arr == (orderFortyNineGeneratedH7SatCnf masks).clauses
  IO.eprintln s!"masks.size={masks.size} clauses={arr.size} top={(orderFortyNineDegreeBlocks 7).top} same_as_lean_cnf={same}"
  if !same then return 2
  let out ← IO.FS.Handle.mk (args.getD 2 "out.cnf") IO.FS.Mode.write
  out.putStr s!"p cnf {(orderFortyNineDegreeBlocks 7).top} {arr.size}\n"
  let mut chunk := ""
  for i in [0:arr.size] do
    chunk := chunk ++ clauseLine arr[i]! ++ "\n"
    if i % 4096 = 4095 then
      out.putStr chunk
      chunk := ""
  if !chunk.isEmpty then out.putStr chunk
  out.flush
  pure 0
