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
from serpentTools import read
from serpentTools.settings import rc


rc['xs.variableGroups'] = ['eig']
rc['serpentVersion'] = '2.1.30'


def buildSss2Cmd(sss2Exe, opts=None):
    if not isfile(sss2Exe):
        raise IOError(
            "SERPENT executable {} not found".format(sss2Exe))
    if opts is None:
        opts = []
    elif isinstance(opts, str):
        opts = opts.split()
    elif isinstance(opts, dict):
        opts = []
        for key, value in opts.items():
            opts.extend(['-' + key, value.split()])
    return [sss2Exe] + opts


class Runner(object):

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

    def run(self, fuelr, mpitch):
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
        try:
            reader = read(resfile, 'results')
            kinf = reader.resdata['absKeff'][0:2]
        except Exception as ee:
            move(resfile, self._pwd)
            raise ee
        return kinf
