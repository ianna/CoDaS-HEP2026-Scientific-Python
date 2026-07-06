# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.23.13",
# ]
# ///

import marimo

__generated_with = "0.23.13"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    import marimo as mo

    def show_img(name, width=250):
            """Displays a local image from the 'img' directory relative to the notebook."""
            img_path = mo.notebook_location() / "img" / name
            return mo.image(src=str(img_path), width=width)

    return mo, show_img


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Reading ROOT files with uproot
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Introduction
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [uproot](https://uproot.readthedocs.io/) is a pure-Python library for reading and writing ROOT files. It does **not** depend on ROOT itself — it speaks the ROOT binary format directly, returning data as NumPy arrays or Awkward Arrays.

    **RNTuple** is the current default storage format for new CMS data. It replaces the older TTree format and is better designed for modern storage systems, parallel I/O, and the columnar workflows you learned in the previous tutorial. uproot has fully supported reading RNTuples since v5.3 and writing since v5.7 (where it became the default).

    Key concepts:

    * A ROOT file is a **key–value store**: keys are strings, values are ROOT objects (histograms, RNTuples, TTrees, ...).
    * An **RNTuple** is a table: **fields** are columns, **entries** are rows (usually events). (TTree called them "branches"; the RNTuple equivalent is "fields".)
    * uproot reads data **lazily** — nothing is loaded from disk until you ask for it.
    * The output is an **Awkward Array**, which plugs straight into everything you learned in the columnar-analysis tutorial.

    Throughout this notebook we use a real CMS Run 2 dimuon dataset from [scikit-hep-testdata](https://github.com/scikit-hep/scikit-hep-testdata), a package that ships small example ROOT files for testing and tutorials:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## RNTuple's layered memory layout
    """)
    return


@app.cell(hide_code=True)
def _(show_img):
    show_img("rntuple_memory_layout.svg", width=600)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Five nested layers, reading from outside in:

    **File** — a ROOT key-value store. The RNTuple lives under one anchor key. Everything else is self-describing.

    **Header / Footer envelopes** — written once. The header holds the *schema*: the tree of fields (what the user sees) and the physical columns they map to. The footer holds cluster group locators so uproot can jump straight to any entry range without scanning the file.

    **Cluster group** — a coarse grouping of clusters, referenced by the footer. In practice most files have one cluster group.

    **Cluster** — the unit of parallel I/O. Each cluster covers a contiguous entry range (e.g. events 0–999). Crucially, every column has its own independent slice within each cluster, so uproot can read `Muon_pt` without touching `Muon_eta` at all. This is what makes column projection fast.

    **Pages** — the actual compressed bytes. A page holds ≥100 kB of a single column's data for one cluster. Pages are individually compressed (LZ4, ZSTD, etc.) and can be decompressed in parallel. This is the leaf node — the only layer that contains event data.

    The key difference from TTree: in TTree, a *basket* mixes all branches of one entry together. In RNTuple, each column lives in completely separate pages, so reading one field never touches another field's bytes.

    </div>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Opening a file
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `uproot.open()` works the same way for RNTuple files as for TTree files. The `with` statement is recommended so the file handle is always closed cleanly.
    """)
    return


@app.cell
def _():
    import uproot
    import skhep_testdata

    # Resolve the path once; reuse everywhere
    PATH = skhep_testdata.data_path(
        "Run2012BC_DoubleMuParked_Muons_1000evts_rntuple_v1-0-0-0.root"
    )
    print(PATH)
    return PATH, skhep_testdata, uproot


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH) as _file:
        print(_file)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `file` behaves like a Python `dict`. `.keys()` lists everything stored in the file, and `.classnames()` shows each object's type.
    """)
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH) as _file:
        print(_file.classnames())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can jump straight to an object by putting its name after a colon in the path string:
    """)
    return


@app.cell
def _(PATH, uproot):
    # These two are equivalent:
    # uproot.open(PATH)["Events"]
    # uproot.open(PATH + ":Events")   ← colon shorthand
    #
    # Note: "Events" IS the RNTuple — there is no sub-tree inside it.
    _ntuple = uproot.open(PATH + ':Events')
    _ntuple
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inspecting an RNTuple
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    RNTuple uses the word **field** where TTree used **branch**. `.keys()` lists field names; `.show()` includes their C++ types.

    One thing to be aware of: this file stores the muon collection both as **top-level fields** (`Muon_pt`, `Muon_eta`, …) and as an internal record field named `_collection0`. The `_collection0` field is an implementation detail of how ROOT writes RVec fields — you can safely ignore it and work with the top-level fields directly.
    """)
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        _ntuple.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Filter by glob pattern — works the same as for TTrees:
    """)
    return


@app.cell
def _(PATH, uproot):
    # keys() returns dotted sub-field paths too (_collection0.Muon_pt etc.)
    # filter to top-level user fields only:
    with uproot.open(PATH + ':Events') as _ntuple:
        print('All keys:       ', _ntuple.keys())
        print()
        print('Muon_* keys:    ', _ntuple.keys(filter_name='Muon_*'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Check the entry count:
    """)
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        print(f'{_ntuple.num_entries:,} events')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading arrays
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reading a single field

    `.array()` reads one field. Variable-length fields (particles per event) come back as ragged Awkward Arrays; flat fields (one value per event) come back as NumPy arrays.
    """)
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        muon_pt = _ntuple['Muon_pt'].array()
    muon_pt
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        n_muon = _ntuple['nMuon'].array()
    print(type(n_muon))
    n_muon
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reading multiple fields at once

    `.arrays()` (plural) reads a set of fields and returns an Awkward record array — the same structure the columnar tutorial started with.
    """)
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        muons = _ntuple.arrays(filter_name=lambda name: not name.startswith('_'))  # filter_name skips _collection0 and its dotted sub-paths
    muons
    return (muons,)


@app.cell
def _(muons):
    muons["Muon_pt"]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reading a slice of entries

    Use `entry_start` and `entry_stop` for quick checks on large files:
    """)
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        first_hundred = _ntuple.arrays(filter_name=lambda name: not name.startswith('_'), entry_start=0, entry_stop=100)
    print(f'{len(first_hundred):,} events read')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inspecting a single event
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Indexing into the record array gives you one event as an Awkward `Record`. `.tolist()` converts it to plain Python dicts and lists:
    """)
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        _dataset = _ntuple.arrays(filter_name=lambda name: not name.startswith('_'))
    _dataset[1].tolist()  # second event
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choosing which fields to read
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Reading only what you need is important for performance with large files.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Explicit list:**
    """)
    return


@app.cell
def _(PATH, uproot):
    # An explicit list reads exactly the named fields — no _collection0 leakage.
    with uproot.open(PATH + ':Events') as _ntuple:
        muon_kin = _ntuple.arrays(['Muon_pt', 'Muon_eta', 'Muon_phi', 'Muon_mass', 'Muon_charge'])
    muon_kin
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Glob pattern** — wildcard matching on field names:
    """)
    return


@app.cell
def _(PATH, uproot):
    # Glob "Muon_*" matches top-level Muon_ fields but NOT _collection0 sub-paths
    # (those start with "_", not "Muon_").
    with uproot.open(PATH + ':Events') as _ntuple:
        muon_fields = _ntuple.arrays(filter_name='Muon_*')
    print(muon_fields.fields)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Regular expression** — uproot's RNTuple `filter_name` uses a **`/pattern/` slash-delimited string**, not a compiled `re.Pattern`. (TTree accepts compiled patterns; RNTuple does not — pass a string instead.)
    """)
    return


@app.cell
def _(PATH, uproot):
    import re
    with uproot.open(PATH + ':Events') as _ntuple:
        _kin = _ntuple.arrays(filter_name='/Muon_(pt|eta|phi|mass)$/')
    print(_kin.fields)  # For RNTuple, filter_name accepts a regex in /pattern/ slash syntax,  # NOT a compiled re.Pattern object (that's only for TTree).
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Output formats
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `library` argument controls what uproot returns. The default is `"ak"` (Awkward Array), which handles ragged data naturally.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `library="ak"` (default)
    """)
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        ak_out = _ntuple['Muon_pt'].array(library='ak')
    print(type(ak_out))
    ak_out
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `library="np"` — NumPy (flat fields only)
    """)
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        np_out = _ntuple['nMuon'].array(library='np')
    print(type(np_out))
    np_out[:10]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `library="pd"` — pandas DataFrame

    `library="pd"` is not yet implemented for RNTuple (it's a TTree-only feature for now). Read with the default Awkward Array and convert flat fields using `ak.to_dataframe()`:
    """)
    return


@app.cell
def _(PATH, uproot):
    # Note: library="pd" is not yet implemented for RNTuple — it silently
    # returns an Awkward Array instead. Convert explicitly with ak.to_dataframe():
    with uproot.open(PATH + ':Events') as _ntuple:
        arr = _ntuple.arrays(['nMuon'])
    import awkward as ak
    import pandas as pd
    df = ak.to_dataframe(arr)
    df.head(10)
    return (ak,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Processing files too large to fit in memory
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `uproot.iterate()` processes a file (or many files) in chunks, never loading the whole dataset at once. It works identically for RNTuples and TTrees.
    """)
    return


@app.cell
def _(PATH, ak, uproot):
    total_muon_pt_sum = 0
    _total_events = 0
    for _batch in uproot.iterate(PATH + ':Events', expressions=['Muon_pt'], step_size=200):
        total_muon_pt_sum = total_muon_pt_sum + ak.sum(ak.flatten(_batch['Muon_pt']))
        _total_events = _total_events + len(_batch)
    print(f'Processed {_total_events:,} events')
    print(f'Sum of all muon pT values: {total_muon_pt_sum:.1f} GeV')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Iterating over multiple files

    In real analyses you run over many files at once. `uproot.iterate()` accepts a **list** of `"path:TreeName"` strings, or a **glob** like `"data/Run*.root:Events"` — it crosses file boundaries automatically and presents a seamless stream of chunks. Here we use both skhep-testdata files to demonstrate:
    """)
    return


@app.cell
def _(ak, skhep_testdata, uproot):
    import numpy as np
    PATH_DIMUON = skhep_testdata.data_path('Run2012BC_DoubleMuParked_Muons_1000evts_rntuple_v1-0-0-0.root')
    PATH_TTBAR = skhep_testdata.data_path('cmsopendata2015_ttbar_19980_NANOAOD_RNTupleImporter_rntuple_v1-0-0-1.root')
    pt_bins = np.linspace(0, 200, 41)
    pt_counts = np.zeros(len(pt_bins) - 1, dtype=np.int64)
    _total_events = 0
    _total_muons = 0
    for _batch in uproot.iterate([PATH_DIMUON + ':Events', PATH_TTBAR + ':Events'], expressions=['Muon_pt', 'Muon_eta'], step_size=100):
        flat_pt = ak.to_numpy(ak.flatten(_batch['Muon_pt']))
        _counts, _ = np.histogram(flat_pt, bins=pt_bins)
        pt_counts = pt_counts + _counts
        _total_muons = _total_muons + len(flat_pt)
        _total_events = _total_events + len(_batch)
    print(f'Events processed : {_total_events:,}  (across 2 files)')
    print(f'Total muons      : {_total_muons:,}')
    peak = pt_counts.argmax()
    print(f'Peak pT bin      : {pt_bins[peak]:.0f}–{pt_bins[peak + 1]:.0f} GeV  ({pt_counts[peak]:,} muons)')
    return (np,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `uproot.concatenate()` — all at once

    When the dataset fits in memory, `concatenate` is simpler than iterating:
    """)
    return


@app.cell
def _(PATH, uproot):
    _dataset = uproot.concatenate(PATH + ':Events', filter_name=lambda name: not name.startswith('_'))
    _dataset
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Connecting back to the columnar tutorial
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Once you have an Awkward Array from uproot, everything from the columnar tutorial applies. Here is the full pipeline: file → Lorentz vectors → dimuon mass spectrum.
    """)
    return


@app.cell
def _():
    import vector
    vector.register_awkward()
    return


@app.cell
def _(PATH, ak, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        raw = _ntuple.arrays(['Muon_pt', 'Muon_eta', 'Muon_phi', 'Muon_mass', 'Muon_charge'])
    muons_1 = ak.zip({'pt': raw['Muon_pt'], 'eta': raw['Muon_eta'], 'phi': raw['Muon_phi'], 'mass': raw['Muon_mass'], 'charge': raw['Muon_charge']}, with_name='Momentum4D')
    muons_1
    return (muons_1,)


@app.cell
def _(ak, muons_1):
    muon_plus = muons_1[muons_1.charge > 0]
    muon_minus = muons_1[muons_1.charge < 0]
    mu1, mu2 = ak.unzip(ak.cartesian([muon_plus, muon_minus]))
    dimuon_mass = ak.flatten((mu1 + mu2).mass)
    dimuon_mass
    return (dimuon_mass,)


@app.cell
def _(dimuon_mass):
    from hist import Hist

    Hist.new.Reg(100, 0, 120, label="Dimuon mass (GeV)").Double().fill(dimuon_mass)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Writing RNTuples
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since uproot v5.7, **assigning a dict to a file key creates an RNTuple by default**. This is the recommended way to write data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quick write — assign a dict
    """)
    return


@app.cell
def _(PATH, np, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        _dataset = _ntuple.arrays(['nMuon', 'Muon_pt', 'Muon_eta', 'Muon_charge'])
    two_muon = _dataset[_dataset['nMuon'] == 2]
    with uproot.recreate('/tmp/two_muon_skim.root') as _f:
        _f['TwoMuon'] = {'nMuon': np.asarray(two_muon['nMuon']), 'Muon_pt': two_muon['Muon_pt'], 'Muon_eta': two_muon['Muon_eta'], 'Muon_charge': two_muon['Muon_charge']}
    print('Written.')
    return (two_muon,)


@app.cell
def _(uproot):
    # Round-trip check
    with uproot.open('/tmp/two_muon_skim.root:TwoMuon') as _t:
        print(type(_t).__name__, '—', _t.num_entries, 'events')
        print('Fields:', _t.keys())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `mkrntuple()` — explicit creation for chunked writing

    Use this when the dataset is too large to load at once. The trick is to **initialise from the first real batch** (so the schema is derived from actual array types) and then `.extend()` with subsequent batches. Build each batch as a plain `ak.Array` dict — not `ak.zip`, which wraps in an extra list dimension:
    """)
    return


@app.cell
def _(PATH, ak, uproot):
    # Helper: keep only the fields we want as a plain RecordArray.
    # ak.Array({...}) gives a RecordArray; ak.zip({...}) would wrap in
    # an extra ListOffsetArray layer and break mkrntuple.
    def select(batch):
        return ak.Array({'nMuon': _batch['nMuon'], 'Muon_pt': _batch['Muon_pt']})
    batches = [select(b) for b in uproot.iterate(PATH + ':Events', expressions=['nMuon', 'Muon_pt'], step_size=200)]
    with uproot.recreate('/tmp/chunked.root') as _f:
        _f.mkrntuple('Events', batches[0])
        for _batch in batches[1:]:
            _f['Events'].extend(_batch)
    with uproot.open('/tmp/chunked.root:Events') as _t:
        print(_t.num_entries, 'events written in chunks')
        print('Fields:', _t.keys())  # Initialise from the first batch — schema comes from real data types.  # Extend with the remaining batches.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Writing a histogram
    """)
    return


@app.cell
def _(ak, muons_1, np, uproot):
    _counts, edges = np.histogram(np.asarray(ak.flatten(muons_1.pt)), bins=50, range=(0, 100))
    with uproot.recreate('/tmp/muon_pt_hist.root') as _f:
        _f['h_muon_pt'] = (_counts, edges)
    print('Histogram written.')
    with uproot.open('/tmp/muon_pt_hist.root:h_muon_pt') as h:
        print(h)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Remote access (HTTP and XRootD)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    uproot reads ROOT files over HTTP or XRootD without downloading them first:
    """)
    return


@app.cell
def _(uproot):
    with uproot.open("https://scikit-hep.org/uproot3/examples/Zmumu.root:events") as tree:
        print(tree.keys()[:6], "... (", tree.num_entries, "events)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For CMS data on EOS, replace `http://` with `root://` (requires the `xrootd` Python package):

    ```python
    uproot.open("root://eoscms.cern.ch//eos/cms/store/...file.root:Events")
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading legacy TTree files
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The API for reading TTrees is identical to RNTuples — the same `.keys()`, `.show()`, `.array()`, `.arrays()`, `uproot.iterate()`, and `uproot.concatenate()` calls all work. The only differences are terminology (TTree says "branches"; RNTuple says "fields") and the class name you see when printing the object.

    You may encounter TTree files from older CMS datasets (Run 2 NanoAOD and earlier). You can tell from the object's type:
    """)
    return


@app.cell
def _(skhep_testdata, uproot):
    # The Zmumu sample from skhep-testdata is a legacy TTree file
    zmumu_path = skhep_testdata.data_path('uproot-Zmumu.root')
    with uproot.open(zmumu_path) as _f:
        for key, classname in _f.classnames().items():
            print(f'{key:30s}  {classname}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If the class name is `TTree`, you have a legacy file. Everything else in this notebook still applies — just replace "field" with "branch" when reading the uproot docs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Writing TTrees explicitly

    If you need to write a TTree (e.g. for compatibility with older ROOT-based code), use `mktree()` instead of the default dict assignment:
    """)
    return


@app.cell
def _(np, two_muon, uproot):
    with uproot.recreate('/tmp/legacy_ttree.root') as _f:
        _f.mktree('Events', {'nMuon': 'int32', 'Muon_pt': 'var * float32'})
        _f['Events'].extend({'nMuon': np.asarray(two_muon['nMuon']), 'Muon_pt': two_muon['Muon_pt']})
    with uproot.open('/tmp/legacy_ttree.root:Events') as _t:
        print(type(_t).__name__, '—', _t.num_entries, 'events')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Quick reference
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    | Task | Code |
    |------|------|
    | Open a file | `uproot.open("file.root")` |
    | Jump to an object | `uproot.open("file.root:Name")` |
    | List contents | `file.keys()` / `file.classnames()` |
    | Inspect fields | `ntuple.show()` / `ntuple.keys()` |
    | Count events | `ntuple.num_entries` |
    | Read one field | `ntuple["field"].array()` |
    | Read several fields | `ntuple.arrays(["f1", "f2"])` |
    | Read by glob | `ntuple.arrays(filter_name="Muon_*")` |
    | Read by regex | `ntuple.arrays(filter_name=re.compile(r"..."))` |
    | Read a slice | `ntuple.arrays(entry_start=0, entry_stop=1000)` |
    | Choose output type | `library="ak"` (default) / `"np"` / `"pd"` |
    | Chunked iteration | `uproot.iterate("file.root:T", step_size=10_000)` |
    | Many files | `uproot.iterate(["a.root:T", "b.root:T"])` or glob `"*.root:T"` |
    | All → one array | `uproot.concatenate("*.root:T")` |
    | Write new file | `uproot.recreate("out.root")` |
    | Write RNTuple (default) | `f["Name"] = {"field": array}` |
    | Write RNTuple (explicit) | `f.mkrntuple("Name", {"field": "type"})` then `.extend()` |
    | Write TTree (legacy) | `f.mktree("Name", {"branch": "type"})` then `.extend()` |
    | Write histogram | `f["h"] = (counts, edges)` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Puzzles
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Puzzle 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Print the number of events in the `Events` RNTuple **without reading any field data**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br><br><br>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Solution
    """)
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        print(_ntuple.num_entries)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br><br><br>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Puzzle 2
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read only `Muon_pt` and `Muon_charge` for the first 200 events. Print the mean $p_T$ of **positively charged muons** (`charge > 0`) across those events.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br><br><br>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Solution
    """)
    return


@app.cell
def _(PATH, ak, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        m = _ntuple.arrays(['Muon_pt', 'Muon_charge'], entry_stop=200)
    pos_pt = m['Muon_pt'][m['Muon_charge'] > 0]
    print(f'Mean μ⁺ pT: {ak.mean(ak.flatten(pos_pt)):.2f} GeV')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br><br><br>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Puzzle 3
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Use a regular expression to read all fields whose names end in `_pt`, `_eta`, or `_phi`. Print the field names you get back.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br><br><br>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Solution
    """)
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        _kin = _ntuple.arrays(filter_name='/Muon_(pt|eta|phi|mass)$/')
    print(_kin.fields)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br><br><br>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Puzzle 4
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Use `uproot.iterate()` with `step_size=200` to process the file in chunks. Count the total number of muons (sum of `nMuon`) across all 1,000 events.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br><br><br>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Solution
    """)
    return


@app.cell
def _(PATH, ak, uproot):
    _total_muons = 0
    for _batch in uproot.iterate(PATH + ':Events', expressions=['nMuon'], step_size=200):
        _total_muons = _total_muons + int(ak.sum(_batch['nMuon']))
    print(f'Total muons across all events: {_total_muons:,}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br><br><br>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Puzzle 5
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Write a skim: keep only events where **both** muons have the same charge (`nMuon == 2` and `Muon_charge[0] == Muon_charge[1]`). Save `Muon_pt` and `Muon_charge` to `/tmp/same_sign_skim.root` as an RNTuple named `SameSign`. Verify by reopening and printing the number of events and field names.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br><br><br>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Solution
    """)
    return


@app.cell
def _(PATH, uproot):
    with uproot.open(PATH + ':Events') as _ntuple:
        _dataset = _ntuple.arrays(['nMuon', 'Muon_pt', 'Muon_charge'])
    two_mu = _dataset[_dataset['nMuon'] == 2]
    same_sign = two_mu[two_mu['Muon_charge'][:, 0] == two_mu['Muon_charge'][:, 1]]
    with uproot.recreate('/tmp/same_sign_skim.root') as _f:
        _f['SameSign'] = {'Muon_pt': same_sign['Muon_pt'], 'Muon_charge': same_sign['Muon_charge']}
    with uproot.open('/tmp/same_sign_skim.root:SameSign') as _t:
        print(type(_t).__name__, '—', _t.num_entries, 'same-sign dimuon events')
        print('Fields:', _t.keys())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <br><br><br>
    """)
    return


if __name__ == "__main__":
    app.run()
