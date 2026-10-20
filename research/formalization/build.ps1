$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$localBin = Join-Path $projectRoot 'toolchain\lean-4.19.0-windows\bin'
if (Test-Path -LiteralPath (Join-Path $localBin 'lake.exe')) {
    $env:PATH = $localBin + ';' + $env:PATH
}
if (-not (Get-Command lake.exe -ErrorAction SilentlyContinue)) {
    throw 'Install the pinned toolchain in lean-toolchain, or place it in formalization/toolchain/. See README.md.'
}
Push-Location -LiteralPath $projectRoot
try {
    # One target at a time avoids multiple simultaneous large Lean imports.
    $targets = @('PlanarQuery.Model', 'PlanarQuery.Accounting',
                 'PlanarQuery.ArityAccounting',
                 'PlanarQuery.CountCredit', 'PlanarQuery.Lookahead',
                 'PlanarQuery.Restricted', 'PlanarQuery.Reduction',
                 'PlanarQuery.Programming', 'PlanarQuery.Randomized',
                 'PlanarQuery.FiniteSearch', 'PlanarQuery.Prefix', 'PlanarQuery.TreePotentials',
                 'PlanarQuery.Properization', 'PlanarQuery.Majority',
                 'PlanarQuery.LiveHeight',
                 'PlanarQuery.WitnessPrefix',
                 'PlanarQuery.PlanarSemantics',
                 'PlanarQuery.GeometryEncoding',
                 'PlanarQuery.AverageInvoice',
                 'PlanarQuery.AverageInternalPenalty',
                 'PlanarQuery.AverageCalibration',
                 'PlanarQuery.AverageFloorCorrection',
                 'PlanarQuery.AverageReferenceBound',
                 'PlanarQuery.AveragePairPerturbation',
                 'PlanarQuery.AverageConstructionCorrection',
                 'PlanarQuery.AverageThresholdBound',
                 'PlanarQuery.ThreePartitionBounds',
                 'PlanarQuery.ExpectedModeCosts',
                 'PlanarQuery.ExpectedModeChoiceAlgebra',
                 'PlanarQuery.ExpectedCoarseningAccounting',
                 'PlanarQuery.ExpectedCoarseningTent',
                 'PlanarQuery.GreedyRunAccounting',
                 'PlanarQuery.OddPathMatching',
                 'PlanarQuery.Examples',
                 'PlanarQuery.Helly', 'PlanarQuery.NormalizedGeometry',
                 'PlanarQuery.Boundary', 'PlanarQuery.LookaheadCompletion',
                 'PlanarQuery.Entropy', 'PlanarQuery.EntropyPartitions',
                 'PlanarQuery.ExpectedTranscriptCoarsening',
                 'PlanarQuery.EntropyInequalities', 'PlanarQuery.EntropyStages',
                 'PlanarQuery.Coding', 'PlanarQuery.CodingConverse',
                 'PlanarQuery.CodingTree', 'PlanarQuery.CodingDyadic', 'PlanarQuery.AlphabeticDP',
                 'PlanarQuery.IntervalCover', 'PlanarQuery.PriorityInterval', 'PlanarQuery.DeadlineScheduling',
                 'PlanarQuery.BatchFirstCover',
                 'PlanarQuery.BatchPhaseCoverage',
                 'PlanarQuery.BatchPhaseLength',
                 'PlanarQuery.PriorityPrefix',
                 'PlanarQuery.GradedDP', 'PlanarQuery.MWURegret',
                 'PlanarQuery.FiniteDuality', 'PlanarQuery.BoundaryGeometry',
                 'PlanarQuery.Rollout', 'PlanarQuery.UniformEntropy',
                 'PlanarQuery')
    foreach ($target in $targets) {
        & lake.exe build $target
        if ($LASTEXITCODE -ne 0) { throw "Lean build failed: $target" }
    }
    & python audit.py
    if ($LASTEXITCODE -ne 0) { throw 'Source audit failed.' }
    & lake.exe env lean.exe AxiomAudit.lean 2>&1 |
        Set-Content -LiteralPath 'axiom-audit.log' -Encoding utf8
    if ($LASTEXITCODE -ne 0) { throw 'Lean axiom audit failed.' }
    if (Select-String -LiteralPath 'axiom-audit.log' -Pattern 'sorryAx' -Quiet) {
        throw 'The checked declarations depend on sorryAx.'
    }
    & python verify_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'Axiom dependency validation failed.' }
    & python inventory.py
    if ($LASTEXITCODE -ne 0) { throw 'Claim inventory failed.' }
    Write-Output 'Lean build, source audit, axiom audit, and manuscript inventory passed.'
}
finally {
    Pop-Location
}
