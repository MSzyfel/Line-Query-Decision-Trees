import PlanarQuery.Model
import Mathlib.Algebra.BigOperators.Fin

namespace PlanarQuery

def singletonModel : QuerySystem (Fin 3) (Fin 3) where
  answer q h := q == h

def singletonTree : Tree (Fin 3) (Fin 3) :=
  .node 0 (.node 1 (.leaf 2) (.leaf 1)) (.leaf 0)

theorem singletonTree_identifies :
    Tree.Identifies singletonModel Finset.univ singletonTree := by
  unfold Tree.Identifies
  decide

theorem singletonTree_height : Tree.height singletonTree = 2 := by decide

theorem singletonTree_raw_cost :
    Tree.rawExpected singletonModel (fun _ => 1) Finset.univ singletonTree = 5 := by
  have h02 : (0 : Fin 3) ≠ 2 := by decide
  norm_num [Tree.rawExpected, Fin.sum_univ_succ, singletonModel, singletonTree, Tree.depth, h02]

theorem singletonTree_restriction :
    Tree.depth singletonModel
      (Tree.restrict singletonModel singletonTree {1, 2}) 1 = 1 := by decide

end PlanarQuery
