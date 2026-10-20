# Executable recognition of the graph-gated product class

Auxiliary note, 19 October 2026. The article is unchanged. This implements the
automatic-recognition discussion in `research-general-dependency-graph.md`.
The resulting factor-two guarantee concerns a recognized structured class;
there is no unrestricted approximation claim.

The companion `research-general-graph-recognition.py` receives only the
original binary response matrix. It recovers coordinates, a loop-free parent
graph, test orientations, and the actual private-code rows, then executes the
charged count policy using original question indices. It receives no supplied
graph, hypothesis coordinates, test roles, or bit labels.

## 1. The recognized class and what acceptance certifies

For some `M=2^b>=4` and `n=M^d`, the hypotheses form the full uniform product
`[M]^d`. Every pure coordinate equality is supplied. Each coordinate i has a
fixed loop-free parent set `Pa(i)`. For every parent-value tuple a, there is a
private b-question palette

    q(i,a,j)=1 iff x_Pa(i)=a and local_bit_(i,a,j)(xi)=1.

The b-bit labels of the M target values are injective. Labels can be arbitrary
and can differ independently between parent contexts. Questions and hypotheses
can appear in any order. Every physical question can be complemented, and
duplicates and constants are harmless.

Acceptance is deliberately conservative. Every nonconstant original question
must have a permitted equality or private-box description, each target must
have one common parent set, every parent tuple must occur, and each local
palette must have exactly b distinct unordered target partitions giving M
different labels. Repeated questions or locally complementary versions of a
bit can share that same unordered partition. This slightly redundant accepted
class still satisfies the same simulation theorem: every original question
has one full-parent-conjunction description, and a complete enabled palette
of width b is available.

Self-parent graphs remain allowed by the supplied-representation theorem in
the dependency-graph note, but this automatic recognizer excludes them. It
also requires a complete fast palette for every vertex. Missing palettes are
rejected rather than interpreted as a different activation rule. `M=2` is
outside this recognizer; in the supplied product model its equalities alone
already achieve the entropy bound.

## 2. Recovery from the response matrix

For every power-of-two guess M with `n=M^d`, retain the original questions of
global minority at least `n/M`. Pure equalities and root bits survive. Every
nonroot private bit has minority

    n/(2 M^|Pa(i)|) < n/M,

and is removed, irrespective of its physical orientation. Exact Cartesian
factorization of the distinct retained response words therefore recovers the
coordinate axes, up to permutations of axes and of their values. Each axis
contains all its equality indicators, whose one-hot relation cannot factor
nontrivially; root bits belong to that same axis. The implementation reuses
`CONTEXT.ResponseFactors` from `research-general-factor-contexts.py` and
requires its quotient to contain all n hypotheses and all d factor alphabets
to equal M. Consequently each original hypothesis has a distinct recovered
coordinate tuple, and these tuples exhaust the full Cartesian product.

For each nonconstant original question, inspect both response cells. Compute
their coordinate projections and require that the cell is the **whole**
Cartesian box given by those projections. Since recovered tuples are a
bijection onto the full product, equality of the cell size and the product
of its projection sizes is sufficient; merely seeing compatible projection
sizes would not be sufficient without that bijection.

An equality box has one singleton axis and all other axes full. A private
box has exactly one axis of size `M/2>1`, the target; its parent axes are
singletons, and all remaining axes are full. This determines its target,
parent set, and parent tuple. A root bit can be parsed from either response
cell, giving complementary target partitions with the same meaning. A
nonroot private box has a unique semantic positive cell. The certificate
stores which original response, zero or one, represents that positive cell.

The final checks explicitly require all coordinate equalities, one common
parent set per target, every parent tuple, exactly b distinct local coding
partitions per tuple, and an injective M-value label map. Every original
nonconstant question must parse. An accepted certificate therefore establishes
all hypotheses and all original questions meet the model assumptions needed
by the factor-two proof, including the questions an unrestricted optimum
might use.

The enumeration has at most `log2 n` alphabet guesses. Parent-context counts
are at most `M^(d-1)<=n`, and all support, box, and palette checks operate on
the explicit matrix with integer arithmetic. `ResponseFactors` constructs at
most `n^(log2 3)` contexts even though recognition only needs its factors, so
this implementation retains a fixed-exponent polynomial runtime.

## 3. Executing the recovered policy with physical questions

`recognize(instance, alphabet=None)` returns a `Representation` certificate
or `None`, together with diagnostics for each attempted alphabet. The
certificate stores recovered cells, parent sets, equality references, and
private-palette references. A `QuestionRef` contains an original question
index, its semantic orientation, and its target-value subset.

`execute_recognized(certificate)` runs `ChargedActivationDP` with at most n
count vectors and activation charge `c_i=b` for every coordinate. It keeps
the actual candidate-value sets alongside those counts.

* If no coordinate is enabled, it asks the policy's selected pure equality.
  An equality whose semantic positive response is the physical zero response
  simply puts the singleton child on the physical-zero branch.
* If a coordinate is enabled, its parent values select the recovered palette
  group. It asks any still-proper palette row until that coordinate is known,
  skipping constant rows. Since the b rows identify all M values, they also
  identify every surviving subset, in at most b actual questions.

For each executed question the code checks that the physical-one child is
exactly the current hypothesis set intersected with the original response
mask. The physical-zero child is the complement within the current state.
Thus semantic relabeling never substitutes a synthetic question. The returned
tree is complete, proper, and uses only original indices.

The dependency-graph proof gives, for the optimal charged abstraction value V,

    actual_mean <= V <= OPTmean+d b <= 2 OPTmean.

Its pathwise comparison accounts for each extra simulated parent check by a
positive paid equality, which fixes a new coordinate and saves at least one
unit of that coordinate's later activation charge. Automatic recognition adds
no approximation loss. On rejection the routine makes no claim; a general
portfolio can retain an independently constructed incumbent.

## 4. Bounded verification

Run `.venv\\Scripts\\python.exe research-general-graph-recognition.py`.
The saved output is `research-general-graph-recognition.results.json`.
There is no unrestricted optimum oracle in this script.

Eight positive cases cover `M=4,d=1/2/3` and `M=8,d=2`, including DAGs, directed
cycles, and a complete directed graph. Every case independently permutes
hypothesis order, question order, and each parent context's target labels.
They include uncomplemented questions, all questions complemented, and mixed
orientations. Recognition is called without the true M. Every resulting
physical tree is executed on every hypothesis, and its raw cost is checked
against `n V`; the largest cases have 64 hypotheses and 108 questions.

Seven negative cases are rejected across all guessed alphabet sizes:

1. A same-size diagonal replacement for a private Cartesian box.
2. One missing local palette row.
3. One missing full parent-context palette.
4. An extra diagonal question coupling the recovered axes.
5. One missing pure equality.
6. A target with two different parent sets.
7. Three distinct balanced local bits that fail to identify eight values.

The last case uses two independent bits and their XOR, so checking row count
and balance alone would miss the defect. Rejection diagnostics identify the
failed condition. These tests exercise the automatic recognizer and physical
orientation handling; the factor-two theorem is established by the complete
representation checks and charged simulation proof, rather than inferred
from finite comparisons.
