import Lake
open Lake DSL

package «planar-line-query» where
  version := v!"0.1.0"

require mathlib from "mathlib-git"

@[default_target]
lean_lib PlanarQuery where
  roots := #[`PlanarQuery]
