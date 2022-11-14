"""Utility module for auxiliary methods and classes."""

import warnings
import inspect
import os
from pathlib import Path
import urllib.request
import zipfile
import shutil


from impy import impy_config
import numpy as np

# Global debug flags that would be nice to have in some sort
# of config or other ideas?
print_module = True

# Standard stable particles for for fast air shower cascade calculation
# Particles with an anti-partner
standard_particles = [11, 13, 15, 211, 321, 2212, 2112, 3122, 411, 421, 431]
standard_particles += [-pid for pid in standard_particles]
# unflavored particles
standard_particles = tuple(standard_particles + [111, 130, 310, 221, 223, 333])


def getAZN(pdgid):
    """Returns mass number :math:`A`, charge :math:`Z` and neutron
    number :math:`N` of ``pdgid``.

    Note::

        PDG ID for nuclei is coded according to 10LZZZAAAI. For iron-52 it is 1000260520.

    Args:
        pdgid (int): PDG ID of nucleus/mass group
    Returns:
        (int,int,int): (Z,A) tuple
    """
    Z, A = 1, 1
    if pdgid < 2000:
        return 0, 0, 0
    elif pdgid == 2112:
        return 1, 0, 1
    elif pdgid == 2212:
        return 1, 1, 0
    elif pdgid > 1000000000:
        A = pdgid % 1000 / 10
        Z = pdgid % 1000000 / 10000
        return A, Z, A - Z
    else:
        return 1, 0, 0


def AZ2pdg(A, Z):
    """Conversion of nucleus with mass A and charge Z
    to PDG nuclear code"""
    # 10LZZZAAAI
    pdg_id = 1000000000
    pdg_id += 10 * A
    pdg_id += 10000 * Z
    return pdg_id


def fortran_chars(array_ref, char_seq):
    """Helper to set fortran character arrays with python strings"""
    info(10, "Setting fortran array with", char_seq)
    # Reset
    import numpy as np

    len_arr = int(str(array_ref.dtype)[2:])
    len_seq = len(char_seq)
    return np.array(
        [c for c in char_seq + (len_arr - len_seq) * " "], dtype="S" + str(len_arr)
    )


def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method

    `skip` specifies how many levels of stack to skip while getting caller
    name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.
    An empty string is returned if skipped levels exceed stack height.abs

    From https://gist.github.com/techtonik/2151727
    """

    stack = inspect.stack()
    start = 0 + skip

    if len(stack) < start + 1:
        return ""

    parentframe = stack[start][0]

    name = []

    if print_module:
        module = inspect.getmodule(parentframe)
        # `modname` can be None when frame is executed directly in console
        if module:
            name.append(module.__name__ + ".")

    # detect classname
    if "self" in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # there seems to be no way to detect static method call - it will
        # be just a function call

        name.append(parentframe.f_locals["self"].__class__.__name__ + "::")

    codename = parentframe.f_code.co_name
    if codename != "<module>":  # top level usually
        name.append(codename + "(): ")  # function or a method

    del parentframe
    return "".join(name)


def info(min_dbg_level, *message):
    """Print to console if `min_debug_level <= config["debug_level"]`

    The fuction determines automatically the name of caller and appends
    the message to it. Message can be a tuple of strings or objects
    which can be converted to string using `str()`.

    Args:
        min_dbg_level (int): Minimum debug level in config for printing
        message (tuple): Any argument or list of arguments that casts to str
    """

    # Would prefer here a global debug
    # if min_dbg_level <= config["debug_level"]:
    if min_dbg_level <= impy_config["debug_level"]:
        message = [str(m) for m in message]
        print(caller_name() + " ".join(message))


class OutputGrabber(object):
    """
    Class to capture the output produced by the console and
    store it as a string variable. This is provided for utlity
    to event generators written in C++.
    Source: https://stackoverflow.com/questions/24277488/
    in-python-how-to-capture-the-stdout-from-a-c-shared-library-to-a-variable
    """

    escape_char = r"\c"

    def __init__(self, stream=None, threaded=False):
        import sys

        self.origstream = stream
        self.threaded = threaded
        if self.origstream is None:
            self.origstream = sys.stdout
        self.origstreamfd = self.origstream.fileno()
        self.capturedtext = ""
        # Create a pipe so the stream can be captured:
        self.pipe_out, self.pipe_in = os.pipe()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()

    def start(self):
        """
        Start capturing the stream data.
        """
        import threading
        import time

        self.capturedtext = ""
        # Save a copy of the stream:
        self.streamfd = os.dup(self.origstreamfd)
        # Replace the original stream with our write pipe:
        os.dup2(self.pipe_in, self.origstreamfd)
        if self.threaded:
            # Start thread that will read the stream:
            self.workerThread = threading.Thread(target=self.readOutput)
            self.workerThread.start()
            # Make sure that the thread is running and os.read() has executed:
            time.sleep(0.01)

    def stop(self):
        """
        Stop capturing the stream data and save the text in `capturedtext`.
        """
        # Print the escape character to make the readOutput method stop:
        self.origstream.write(self.escape_char)
        # Flush the stream to make sure all our data goes in before
        # the escape character:
        self.origstream.flush()
        if self.threaded:
            # wait until the thread finishes so we are sure that
            # we have until the last character:
            self.workerThread.join()
        else:
            self.readOutput()
        # Close the pipe:
        os.close(self.pipe_in)
        os.close(self.pipe_out)
        # Restore the original stream:
        os.dup2(self.streamfd, self.origstreamfd)
        # Close the duplicate stream:
        os.close(self.streamfd)

    def readOutput(self):
        """
        Read the stream data (one byte at a time)
        and save the text in `capturedtext`.
        """
        while True:
            char = os.read(self.pipe_out, 1)
            if not char or self.escape_char in char:
                break
            self.capturedtext += char


# Functions to check and download dababase files on github


def _download_file(outfile, url):
    """Download a file from 'url' to 'outfile'"""
    fname = Path(url).name
    try:
        response = urllib.request.urlopen(url)
    except BaseException:
        raise ConnectionError(
            f"_download_file: probably something wrong with url = '{url}'"
        )
    total_size = response.getheader("content-length")

    min_blocksize = 4096
    if total_size:
        total_size = int(total_size)
        blocksize = max(min_blocksize, total_size // 100)
    else:
        blocksize = min_blocksize

    wrote = 0
    with open(outfile, "wb") as f:
        while True:
            data = response.read(blocksize)
            if not data:
                break
            f.write(data)
            wrote += len(data)
            if total_size:
                print(
                    f"Downloading {fname}: {wrote/total_size*100:.0f}% "
                    f"done ({wrote/(1024*1024):.0f} Mb) \r",
                    end=" ",
                )
            else:
                print(
                    f"Downloading {fname}: {wrote/(1024*1024):.0f} Mb downloaded \r",
                    end=" ",
                )
    print()
    if total_size and wrote != total_size:
        raise ConnectionError(f"{fname} has not been downloaded")
    return True


def _cached_data_dir(url):
    """Checks for existence of version file
    "model_name_vxxx.zip". Downloads and unpacks
    zip file from url in case the file is not found

    Args:
        url (str): url for zip file
    """

    base_dir = Path(__file__).parent.absolute() / "iamdata"
    base_dir.mkdir(parents=True, exist_ok=True)

    vname = Path(url).stem
    model_dir = base_dir / vname.split("_v")[0]
    version_file = model_dir / vname
    if not version_file.exists():
        zip_file = base_dir / Path(url).name
        temp_dir = Path(model_dir.parent / f".{model_dir.name}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        if model_dir.exists():
            shutil.move(model_dir, temp_dir)
        if _download_file(zip_file, url):
            if zipfile.is_zipfile(zip_file):
                with zipfile.ZipFile(zip_file, "r") as zf:
                    zf.extractall(base_dir.as_posix())
                zip_file.unlink()
                shutil.rmtree(temp_dir, ignore_errors=True)

        version_glob = vname.split("_v")[0]
        for vfile in model_dir.glob(f"{version_glob}_v*"):
            vfile.unlink
        with open(version_file, "w") as vf:
            vf.write(url)
    return str(model_dir) + "/"


class TaggedFloat:
    """Floating point type that is distinct from an ordinary float.

    TaggedFloat is a base class to inherit from. We use it to declare
    that certain numbers have special meaning, e.g.::

        class KineticEnergy(TaggedFloat):
            pass

    can be used to declare a float-like class which stores kinetic energies,
    as opposed to another float-like class which stores the total energy or
    the momentum. Functions with an energy parameter can react differently
    on a KineticEnergy or TotalEnergy.

    A tagged float only allows arithmetic with its own type or
    with type-less numbers (int, float).
    """

    __slots__ = "_value"

    def __init__(self, val):
        self._value = float(val)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._value!r})"

    def __float__(self):
        return self._value

    @classmethod
    def _reduce(cls, other):
        if isinstance(other, (int, float)):
            return other
        elif isinstance(other, cls):
            return other._value
        raise ValueError("{other!r} is not a number or {cls.__name__}")

    def __eq__(self, other):
        return self.__class__ is other.__class__ and self._value == other._value

    def __ne__(self, val):
        return not self == val

    def __mul__(self, val):
        return self.__class__(self._value * self._reduce(val))

    def __rmul__(self, val):
        return self * self._reduce(val)

    def __add__(self, val):
        return self.__class__(self._value + self._reduce(val))

    def __radd__(self, val):
        return self + self._reduce(val)

    def __truediv__(self, val):
        return self.__class__(self._value / self._reduce(val))

    def __rtruediv__(self, val):
        return self.__class__(self._reduce(val) / self._value)

    def __sub__(self, val):
        return self.__class__(self._value - self._reduce(val))

    def __rsub__(self, val):
        return self.__class__(self._reduce(val) - self._value)


# from Python-3.9 onwards, classmethod can be combined
# with property to replace this, which can then be removed
class classproperty:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


def _select_parents(mask, parents):
    # This algorithm is slow in pure Python and should be
    # speed up by compiling the logic.

    # attach parentless particles to beam particles,
    # unless those are also removed
    fallback = (0, 0)
    if mask[0] and mask[1]:
        fallback = (1, 2)

    n = len(parents)
    indices = np.arange(n)[mask] + 1
    result = parents[mask]
    mapping = {old: i + 1 for i, old in enumerate(indices)}

    n = len(result)
    for i in range(n):
        a = result[i, 0]
        if a == 0:
            continue
        p = mapping.get(a, -1)
        if p == -1:
            a, b = fallback
            result[i, 0] = a
            result[i, 1] = b
        elif p != a:
            q = 0
            b = result[i, 1]
            if b > 0:
                q = mapping.get(b, 0)
            result[i, 0] = p
            result[i, 1] = q
    return result


def select_parents(arg, parents):
    if parents is None:
        return None

    n = len(parents)

    if isinstance(arg, np.ndarray) and arg.dtype is bool:
        mask = arg
    else:
        mask = np.zeros(n, dtype=bool)
        mask[arg] = True

    with warnings.catch_warnings():
        # suppress numba safety warning that we can ignore
        warnings.simplefilter("ignore")
        return _select_parents(mask, parents)


try:
    # accelerate with numba if numba is available
    import numba as nb

    _select_parents = nb.njit(_select_parents)

except ModuleNotFoundError:
    pass
