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
- `history/his` - input file for using history capabilities in SERPENT
- `det/det` - input file with a collection of detector settings
- `dep/dep` - input file with depletion steps
- `sens/sens` - input file for sensitivity calculation
- `coe/coe` - input file for automated burnup sequence
- `archive.sh` - archival script used to collect all output files
- `files.tgz` and `file.zip` - compressed archives of all output files needed for
  the analysis.
- `files.sha256` and `files.md5` - text files containing hashes of compressed archives.
  Can be verified with `sha256sum -c files.sha256` and `md5sum -c files.md5`
- `runAll.sh` - script that runs all input files. Requires some environment variables
  to find the SERPENT executable and libraries. Useful if you want to generate all
  outputs outside of the compressed files

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
coe/coe.coe
dep/dep_dep.m
dep/dep_res.m
dep/depmtx_fuelpfpr10.m
det/bwr_det0.m
det/det_det0.m
history/hist_his0.m
simple_res.m
```
