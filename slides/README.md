## Modern HEP Analysis Pipeline: The Muscles & The Brain

Think of **NumPy, CuPy, and CUDA** as the raw muscles (the mathematical engines running on hardware). Think of **Scikit-HEP tools** as the brain (giving those numbers physical meaning, organizing them into histograms, and formatting them for physics publications). You use the engines to process raw arrays, and then pass the results into the HEP stack.

# Hardware Performance and the Scikit-HEP Ecosystem

```text
        THE MUSCLES: RAW MATH ENGINES                 THE BRAIN: HEP STACK
          (Hardware Performance)                     (Scikit-HEP Ecosystem)

┌──────────────────────────────────┐      ┌──────────────────────────────────────────┐
│                                  │      │                                          │
│  NumPy (Vectorized CPU)     ─────┼──┐   │  Physics Metadata & Constants            │
│                                  │  │   │  (particle, hepunits)                    │
└──────────────────────────────────┘  │   └──────────────────────────────────────────┘
                                      │
┌──────────────────────────────────┐  │   ┌──────────────────────────────────────────┐
│                                  │  ├──▶│                                          │
│  CuPy (Vectorized GPU)      ─────┼──┤   │  High-Performance Histogramming          │
│                                  │  │   │  (hist, boost-histogram)                 │
└──────────────────────────────────┘  │   └──────────────────────────────────────────┘
                                      │
┌──────────────────────────────────┐  │   ┌──────────────────────────────────────────┐
│                                  │  │   │                                          │
│  CUDA Python / CCCL         ─────┼──┘   │  High-Level Columnar Analysis            │
│                                  │      │  (uproot, awkward, vector)               │
└──────────────────────────────────┘      └──────────────────────────────────────────┘
                                              ┌──────────────────────────────────────┐
Raw computing engines                         │                                      │
running directly on the hardware              │  Publication Output & Plotting       │
                                              │  (mplhep)                            │
                                              └──────────────────────────────────────┘
                                                               │
                                                               ▼
                                                  ┌──────────────────────────────┐
                                                  │                              │
                                                  │     Physics Publication      │
                                                  │   Official Journal Layouts   │
                                                  │                              │
                                                  └──────────────────────────────┘
```

