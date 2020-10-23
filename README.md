# MachSMT Artifact for TACAS'21 AE

Joseph Scott, Aina Niemetz, Mathias Preiner, Saeed Nejati, and Vijay Ganesh

## Setup Steps

1. Change directory
  ```
  cd machsmt_artifact
  ```

2. Set permission on installation and demonstration scripts
  ```
  chmod 755 install.sh
  chmod 755 demo.sh
  ```

3. Install MachSMT
  ```
  sudo ./install.sh
  ```
  **Note** This script installs all the dependencies of MachSMT. The artifact
  includes a `depends` directory in which all the pip requirements are saved.
  This artifact assumes access to Python3.8 and pip3 20.0.0

4. Run MachSMT
  ```
  ./demo.sh
  ```
  **Note** This script provides a demonstration of MachSMT. Specifically, this
  script produces all cactus/cdf plots in the paper from scratch. This script 
  builds MachSMT on the select logics, evaluates under k-fold cross validation,
  and provides example ussage on how to use MachSMT to make predictions on  smt2
  benchmarks


## Artifact Instructions

We provide a short script `demo.sh` to demonstrate our tool and reproduce
several results that were included in the paper. Due to the large nature of the
SMT-LIB benchmark repository (>100GB), we will only provide the benchmarks
required to closely reproduce all plots in our paper.The artifact provides
benchmarks for the logics BV, NRA, QF_BVFPLRA, QF_LIA, and QF_UFBV.

In order to test algorithm selection on benchmarks from SMT-LIB not included
in the artifact, download benchmarks of interest from the [SMT-LIB initiative's
benchmark page](http://smtlib.cs.uiowa.edu/benchmarks.shtml). For latest competition
timing analysis, see [the smt-comp github repo](https://github.com/smt-comp)

As with all machine learning, it can be very difficult to reproduce all results
precisely. Further, reproducing the entire experimental evaluation of our paper
takes up to 12 hours on a single Intel i7-4790 with 16GB of RAM, which is
clearly out of scope for this artifact. Since were not able to include the
entirety of the SMT-LIB benchmarks due to space constraints, we only include
the aforementioned logics in this artifact.

Script `demo.sh` performs the following steps:

* Call `machsmt_build`
    * Perform feature preprocessing and constructs full learned models for
    the following logics and store them in directory `lib/`.
        * BV in the Single Query Track (SQ)
        * NRA in the Single Query Track (SQ)
        * QF_BVFPLRA in the Single Query Track (SQ)
        * QF_LIA in the Single Query Track (SQ)
        * QF_UFBV in the Single Query Track (SQ)
        
    **Note** By default, only BV is processed. To process all use the -a option on `demo.sh`

* Call `machsmt_eval`
    * Separately, using Cross Validation as described in our paper:
        * Reproduce cdf + cactus plots for figures 2-6.
        * Provide a csv of PAR-2 for above logics and tracks.
    **Note** By default, only BV is processed. To process all use the -a option on `demo.sh`

* Call `machsmt` on random BV benchmarks:
    * Make selections for 10 random BV benchmarks.

## Directory structure of the artifact


### Directory structure of `lib`

The models generated by `machsmt_build` are stored in directory `lib`.
By default, MachSMT uses the SolverLogicEHM ML technqiue for predictions, 
but will evaluate all of them. 


### Directory structure of `results`

The results generated by `machsmt_build` are stored in directory `results`,
which is structued as follows:

```
  results
    |- <track>
       |- <logic>
          |- scores.csv
          |- cactus.png
          |- cdf.png
          |- *_loss.csv
```

* `scores.csv` contains the computed PAR-2 score for all solvers, including
  MachSMT and the virtual best solver (denoted as Oracle) for `<logic>` in `<track>`.
* `cactus.png,cdf.png` corresponds to the cactus/cdf plots for `<logic>` in `<track>`.
   **Note** that the solver names from the generated plots in the artifact and
   the plots in the paper differ. We manually cleaned up the solver names in
   the paper, whereas the generated plots show the raw names as specified in
   the csv result files.
* `*_loss.csv` contains the benchmark wise loss of each predictor. These csv files
  show which benchmarks a particular learnt variant of MachSMT struggles with compared
  to the virtual best solver


### Reproducing all results

The following steps are required to reproduce all results from the paper.

1. Download all SMT-LIB logics into `benchmarks`
2. Run `machsmt_build` (without options)


## Artifact Description

MachSMT provides the following two scripts:

* `machsmt_build` - a script that builds machsmt based on the provided data. This script precomputes features and builds learnt models.
* `machsmt_eval`  - a script to evaluate machsmt under k-fold cross validation
* `machsmt`  - the primary interface to MachSMT's algorithm selection


These script can be found in directory `bin`.


### `machsmt_build`

Building a learned algorithm selection model has two dependencies:
* Benchmark files
* Scoring Files

To build a model for a target application, MachSMT expects a score csv containing with at least the following 3 columns: `benchmark,solver,score`. Each `benchmark` is a path to the location of the benchmark, a `solver` is any string to denote a specific solver, and a score
is any floating-point value. MachSMT will try to minimize the score when making predictions.

For timing analysis, we use data collected from the SMT-COMP '19 and '20. Please see  [SMT-COMP's repository](https://github.com/SMT-COMP/smt-comp) However, arbitrary timing analysis can be used.

Running `machsmt_build` will build models for all solvers/logics/tracks in the input csv files. MachSMT will automatically organize benchmarks based on their logic and track (i.e., SQ or INC).

```machsmt_build --f data1.csv data2.csv -l /path/to/lib```

`machsmt_build` allows for users to adjust the anatomy of the regression model and further add additional features to its pipeline. 

#### machsmt/features/

We provide an interface for users to add extra features when building learned models for MachSMT. An extra feature can be added easily to the MachSMT pipeline by including an additional python method that computes said feature given the filepath to an instance. Additional methods in `machsmt/features/` will be automatically included in the MachSMT pipeline. For more, please see the examples in the directory.

#### machsmt/ml/model_maker.py

The internal regressor within machsmt can be adjusted to any regressor for the EHM can be adjusted to any scikit styled regressor. The interface for this is in `machsmt/model_maker.py`. In this file, a single method can be found that returns an instance of a regressor. This file can be modified appropriately to user needs for their target application. The only requirement is the MachSMT pipeline presupposes the returned regressor object has a `fit(X, Y)` and `predict(X)` attributes to it.  

### `machsmt_eval`

This script will evaluate the resultant build of a call of `machsmt_build`. This script constructs all formulations of MachSMT and evaluates
all of which under k-fold cross validation.

```machsmt_select -l /path/to/lib/dir```

This script outputs a directory named `results` whose contents are specified above. 

### `machsmt`

The algorithm selection script can be run as follows:

```machsmt input.smt2 -l /path/to/lib/dir```

where `/path/to/lib/dir` is the lib directory containing the learnt models
built by `machsmt_build` that should be used for predicting a solver on
input benchmark `input.smt2`.

MachSMT will then print a full ranking over the input solvers it selects to have the shortest
score/runtime.
