# Copyright (c) 2018-2019 Andrew Johnson

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Run SERPENT inside python and collect some results
"""

from shutil import move
from warnings import warn
from os import getcwd
from os.path import isfile, join
from tempfile import TemporaryDirectory
from subprocess import run, PIPE
from numpy import empty_like
from serpentTools import read
from serpentTools.settings import rc


# Tell serpentTools that we only want criticalities
rc['xs.variableGroups'] = ['eig']


def buildSss2Cmd(sss2Exe, opts=None):
    if not isfile(sss2Exe):
        raise IOError(
            "SERPENT executable {} not found".format(sss2Exe))
    if opts is None:
        opts = []
    elif isinstance(opts, str):
        opts = opts.split()
    else:
        raise ValueError("Will not build executable path from {}".format(opts))
    return [sss2Exe] + opts


class Runner(object):
    """
    Basic input file builder and SERPENT runner

    Parameters
    ----------
    tempalteFile: str
        Path to a template file used to build the geometry.
        Replaces {fuelr} with fuel pin radius, {cladr} with
        cladding radius, and {mpitch} with unit cell pitch
    sss2Exe: str
        Path to serpent executable
    sss2Opts: None or str
        Options used to control serpent run. If None, run SERPENT with
        no parallelization. Pass a string to be placed between the
        executable and the file path.

    Examples
    --------
    Plain, serial SERPENT runner

    >>> rs = Runner("template", "sss2")

    Use OMP with four threads

    >>> romp = Runner("template", "sss2", "-omp 4")
    # Executes on file the command ``sss2 -omp 4 <file>``

    Combine MPI and OMP

    >>> mpar = Runner("template", "mpirun -n 4 ./sss2", "-omp 4")
    """

    CLAD_THICK = 0.06

    def __init__(self, templateFile, sss2Exe, sss2Opts=None, verbose=True):
        if not isfile(templateFile):
            raise IOError(
                "File {} does not exist or is not file".format(templateFile))
        with open(templateFile) as stream:
            self._template = stream.read()
        self._exeList = buildSss2Cmd(sss2Exe, sss2Opts)
        self._pwd = getcwd()
        self._verbose = verbose

    @property
    def verbose(self):
        """Boolean controlling the amount of information printed"""
        return self._verbose

    @verbose.setter
    def verbose(self, val):
        self._verbose = bool(val)

    def run(self, fuelr, mpitch=0.63):
        """Return multiplication factor for a geometry

        Performs the following actions:
        1. Creates a temporary directory for input and output files
        2. Builds input file with fuel radius and moderator pitch
        3. Runs serpent given this geometry
        4. After a successful SERPENT run, return absKeff and uncertainty.
           Otherwise, move the input file into this directory and raise an
           error with the current geometry
        5. Destroy the temporary directory
        """
        cladr = fuelr + self.CLAD_THICK
        assert fuelr < cladr < mpitch, ' '.join(
            map(str, (fuelr, cladr, mpitch)))

        with TemporaryDirectory(dir=self._pwd) as tdir:
            inputFile = join(tdir, 'input')

            stat = self._run(fuelr, cladr, mpitch, inputFile)
            if stat:
                raise ValueError(
                    "Run failed.\nFuel pitch: {:7.5F}\nClad radius: {:7.5F}"
                    "\nPitch: {:7.5F}"
                    .format(fuelr, cladr, mpitch))
            kinf = self._scrape(join(tdir, 'input_res.m'))
        return kinf

    def _run(self, fuelr, cladr, mpitch, inputFile):
        """Build the input file and run SERPENT. Return return code"""
        with open(inputFile, 'w') as stream:
            stream.write(self._template.format(
                fuelr=fuelr, cladr=cladr, mpitch=mpitch))
        if self._verbose:
            print("Running with fuel radius: {:7.5F}, clad radius: {:7.5F}, "
                  "pitch: {:7.5F}"
                  .format(fuelr, cladr, mpitch))
        proc = run(self._exeList + [inputFile], stdout=PIPE, stderr=PIPE)
        if proc.returncode != 0:
            # failure
            stdoutF = "log.out"
            stderrF = "log.err"
            with open(stdoutF, 'w') as stream:
                stream.write(proc.stdout.decode())
            with open(stderrF, 'w') as stream:
                stream.write(proc.stderr.decode())
            move(inputFile, self._pwd)
            warn("Failure. Log files {} and {} written."
                 .format(stdoutF, stderrF))
        return proc.returncode

    def _scrape(self, resfile):
        """Read multiplication factor from resfile"""
        try:
            reader = read(resfile, 'results')
            kinf = reader.resdata['absKeff'][0:2]
        except Exception as ee:
            move(resfile, self._pwd)
            raise ee
        return kinf

    def getRangeKeff(self, fRads, mRads=None):
        """Return a vector of keff, unc for various fuel radii"""
        if mRads is None:
            mRads = empty_like(fRads)
            mRads.fill(0.63)
        keffVec = empty_like(fRads, dtype=float)
        uncVec = empty_like(keffVec)

        for ix, (fp, mp) in enumerate(zip(fRads, mRads)):
            keffVec[ix], uncVec[ix] = self.run(fp, mp)
        return keffVec, uncVec
