# ans-student19-serpenttools
Repository containing examples and slides for ANS 2019 Student Conference

## Objectives

1. Provide a modest understanding of the SERPENT Monte Carlo Code
2. Comprehensive overview of `serpentTools` API
3. Demonstrate capabilities for follow-on analysis

## Helpful links:

- [SERPENT Website](http://montecarlo.vtt.fi)
- [SERPENT Wiki](http://serpent.vtt.fi/mediawiki/index.php/Main_Page)
- [Repository for serpent-tools](https://github.com/CORE-GATECH-GROUP/serpent-tools)
- [Main documentation](https://serpent-tools.readthedocs.io/en/latest/)
- [Example directory](https://serpent-tools.readthedocs.io/en/latest/examples/index.html)
- [Install guide](https://serpent-tools.readthedocs.io/en/latest/install.html)

## Workshop tools

SERPENT and `serpentTools` will be utilized live during the workshop. 
If you wish to follow along, you will need the following

1. Python environment (3.5+ preferred)
1. Jupyter notebook
1. Latest `serpentTools` installed

## Workshop not-pre-reqs

The following are not necessary to make the workshop benefitial. 
Basic familiarity with Monte Carlo neutron transport codes (MCNP, SERPENT, SCALE-KENO, etc.)
will make some things easier to understand, but not strictly required.

1. Python mastery
1. Knowlege of SERPENT

## Layout

- `simple` - 6x6 toy assembly designed to show basic input structure.
  Particle count taken to be deliberately low to make demonstrations easier.
  All subsequent input files use this.
- `his` - input file for using history capabilities in SERPENT
- `det` - input file with a collection of detector settings
- `dep` - input file with depletion steps
- `sens` - input file for sensitivity calculation
- `coe` - input file for automated burnup sequence
- `archive.sh` - archival script used to collect all output files
- `files.tgz` and `file.zip` - compressed archives of all output files needed for
  the analysis.
- `files.sha256` and `files.md5` - text files containing hashes of compressed archives.
  Can be verified with `sha256sum -c files.sha256` and `md5sum -c files.md5`
- `Makefile` - Makefile that can be used to run all SERPENT cases to produce the files
  contained in `files.tgz` and `files.zip`.

### Archived files

The compressed `files.tgz` and `files.zip` can be extracted with standard unzipping utilities.
From the command line,
```
$ unzip files.zip
```
or
```
$ tar xzvf files.tgz
```

Either of these commands will extract the following files into this directory.

```
coe.coe
dep_dep.m
dep_res.m
depmtx_fuelpfpr10.m
det_det0.m
hist_his0.m
simple_res.m
```

### Makefile

Using the `Makefile`, you can run all the SERPENT cases and produce the outputs files used
in this workshop. The command `make serpent` will execute SERPENT on all cases. By default,
this looks for `sss2` to be in this directory, calling SERPENT with
```
sss2 -omp 4 {input} > {input}.txt
```

You can change the SERPENT execution by passing `SERPENT_EXE` and `SERPENT_OPTS`
during `make`.
```
make SERPENT_EXE="mpirun -n 4" SERPENT_OPTS="-omp 4" serpent
```
would use `mpirun` with four nodes, and a total of four OMP threads. 
The generation of the coefficient file, `coe.coe`, may take a while,
as 50 perturbation states are calculated.

The `Makefile` can also be used to generate the slides for the workshop. The command
```
make slides
```
will use `pdflatex` to build a pdf of the presentation. 
