# MachSMT Artifact for CAV'20 AE

Joseph Scott, Aina Niemetz, Mathias Preiner, Saeed Nejati, and Vijay Ganesh

## Setup Steps

1. Unpack artifact archive
  ```
  tar xJf machsmt-artifact.tar.xz
  ```

2. Change directory
  ```
  cd machsmt-artifact
  ```

3. Install MachSMT
  ```
  sudo ./install.sh
  ```

4. Run MachSMT
  ```
  ./demo.sh
  ```
  **Note** asdf


## Artifact Instructions

We provide a short script `demo.sh` to demonstrate our tool and reproduce
several results that were included in the paper. Due to the large nature of the
SMT-LIB benchmark repository (>100GB), we will only provide the benchmarks
required to closely reproduce the four cactus plots in our paper.

The artifact provides benchmarks for the logics BV, QF_NRA, UFNIA, and QF_UFBV.
For BV we provide *all* SMT-LIB benchmarks to allow `demo.sh` and reviewers to
conveniently execute algorithm selection (script `machsmt_select`) on benchmarks
not included in our evaluation. Logics QF_NRA, UFNIA, and QF_UFBV contain only
the benchmarks used in SMT-COMP'19 (which is a subset of the benchmark sets in
SMT-LIB) in order to reduce the size of the artifact. By default `demo.sh` will
generate models and data for BV SQ only to reduce the runtime of the artifact.
To produce models and data for all of the above logics use option `-a`.

In order to test algorithm selection on benchmarks from SMT-LIB not included
in the artifact, download benchmarks of interest from the [SMT-LIB initiative's
benchmark page](http://smtlib.cs.uiowa.edu/benchmarks.shtml).

As with all machine learning, it can be very difficult to reproduce all results
precisely. Further, reproducing the entire experimental evaluation of our paper
takes up to 12 hours on a single Intel i7-4790 with 16GB of RAM, which is
clearly out of scope for this artifact. Since were not able to include the
entirety of the SMT-LIB benchmarks due to space constraints, we run all
experiments in `demo.sh` with the MachSMT's `--limit-training` option.

Script `demo.sh` performs the following steps:

* Call `machsmt_build`
    * Construct full learned models for the following logics and store them in
      directory `lib/`.
        * BV in the Single Query Track (SQ)
        * QF_NRA in the Single Query Track (SQ) (with option `-a`)
        * UFNIA in the Unsat Core Track (UC) (with option `-a`)
        * QF_UFBV in the Single Query Track (SQ) (with option `-a`)
    * Separately, using Cross Validation as described in our paper:
        * Reproduce cactus plots for figures 1-4.
        * Provide a csv of PAR-2 for above logics and tracks.
        * Provide a csv of all instance-wise computed features and the selected
          solver.
* Call `machsmt_select` on random BV benchmarks:
    * Make selections for 100 random BV benchmarks.

### Directory structure of the artifact


### Directory structure of `lib`

The models generated by `machsmt_build` are stored in directory `lib`, which
is structued as `lib/<logic>/<track>`, where `lib/<logic>` contains all learned
models by `<track>`. The `lib` directory further contains the file `db.p`,
which stores all benchmark information including extracted features.


### Directory structure of `results`

The results generated by `machsmt_build` are stored in directory `results`,
which is structued as follows:

```
  lib
    |- <logic>
       |- <track>
          |- par2.csv
          |- plot.png
          |- plot_data.p
          |- selections.csv
```

* `par2.csv` contains the computed PAR-2 score for all solvers, including
  MachSMT and the virtual best solver for `<logic>` in `<track>`.
* `plot.png` corresponds to the cactus plot for `<logic>` in `<track>`.
   **Note** that the solver names from the generated plots in the artifact and
   the plots in the paper differ. We manually cleaned up the solver names in
   the paper, whereas the generated plots show the raw names as specified in
   the csv result files.
* `plot_data.p`
* `selections.csv` contains the extracted feature information and the selected
  solver per benchmark


### Reproducing all results

The following steps are required to reproduce all results from the paper.

1. Download all SMT-LIB logics into `benchmarks`
2. Run `machsmt_build` (without options)


## Artifact Description

MachSMT provides the following two scripts:

* `machsmt_select` - the primary interface to MachSMT's algorithm selection
* `machsmt_build`  - a script to learn models for algorithm selection in MachSMT's pipeline.

These script can be found in directory `bin`.


### `machsmt_build`

Building a learned algorithm selection model has two dependencies:
* Appropriate SMT-LIB Benchmarks
* SMT-COMP Timing Analysis

To build a model for a specific logic and track, MachSMT expects access to all benchmarks for said logic and track and will look for them in the  `benchmarks/`  repository in the root of the MachSMT repo. To do so, please download logics of interest from the [SMT-LIB initiative's benchmark page](http://smtlib.cs.uiowa.edu/benchmarks.shtml), and unzip the file. It is important the file structure within the downloaded zip file remains intact.

For timing analysis, please clone the [SMT-COMP's repository](https://github.com/SMT-COMP/smt-comp) at the root of the MachSMT repo, and decompress the timing analysis csv files. However, arbitrary timing analysis can be used as long as the csv header contains the following headers: 'result', 'expected', 'cpu time', 'wallclock time', 'correct-answers', and'wrong-answers'.

Running `machsmt_build` will build models for all logics and tracks. However, this can be narrowed to logics and tracks of interest by running it as:

```machsmt_build --logic LOGIC --track TRACK --limit-training```

By default, MachSMT will try to use runtime analysis from similar divisions and tracks. If benchmarks from similar tracks are not available, it is encouraged to use `--limit-training` flag. However, in the presence of the entirety of the SMT-LIB benchmark database, this flag can be disabled for potential performance improvement. 

`machsmt_build` allows for users to adjust the anatomy of the regression model and further add additional features to its pipeline. 

#### machsmt/extra_features.py

We provide an interface for users to add extra features when building learned models for MachSMT. An extra feature can be added easily to the MachSMT pipeline by including an additional python method that computes said feature given the filepath to an instance. Additional methods in `machsmt/extra_features.py` will be automatically included in the MachSMT pipeline. For more, please see the documentation in this file.

#### machsmt/model_maker.py

The internal regressor within machsmt can be adjusted to any regressor for the EHM can be adjusted to any scikit styled regressor. The interface for this is in `machsmt/model_maker.py`. In this file, a single method can be found that returns an instance of a regressor. This file can be modified appropriately to user needs for their target application. The only requirement is the MachSMT pipeline presupposes the returned regressor object has a `fit(X, Y)` and `predict(X)` attributes to it.  

### `machsmt_select`

The algorithm selection script can be run as follows:

```machsmt_select MODEL INPUT```

where `MODEL` corresponds to the learned EHMs built by `machsmt_build` that
should be used for predicting a solver on benchmark `INPUT`.

MachSMT will then print the name of the solver it selects to have the shortest
runtime.  The models can be either built independently with `machsmt_build` or
all models used in our paper can be downloaded
[here](https://www.dropbox.com/s/773l8axaxbah2yv/lib.zip?dl=1).
