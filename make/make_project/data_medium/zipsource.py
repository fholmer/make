import io
import zipfile
import pathlib
from .local import Local
from ...template import root_exclude
from ...errors import Abort

def make_zipobj(source, zip_sub_path):
    content = io.BytesIO(open(source, 'rb').read())
    zipobj = zipfile.ZipFile(content)

    if zip_sub_path:
        path = zip_sub_path
    else:
        path = '/'

    return pathlib.PosixPath(path), zipobj


class LocalTargetAndZipSource(Local):
    os_sep = "/"
    os_sep_dbl = "//"

    def __init__(self, zip_source, zip_sub_path):
        self.root, self.zip = make_zipobj(zip_source, zip_sub_path)

    def exists(self, path):
        path_str = str(path)
        return path_str in self.zip.namelist()

    def read_text(self, source):
        zippath = "/".join(source.parts)
        return self.zip.read(zippath).decode()

    def read_bytes(self, source):
        zippath = "/".join(source.parts)
        return self.zip.read(zippath)

    def copy(self, source, target):
        zippath = "/".join(source.parts)
        self.zip.extract(zippath, str(target))

    def ensure_source(self):
        source = str(self.root)
        if not source.endswith("/"):
            source += "/"
        if not source in self.zip.namelist() and not source == "/":
            raise Abort("Source %s does not exists" % source)

    def ensure_target(self):
        if self.root in self.zip.namelist():
            raise Abort("Target %s already exists" % self.root)

    def iter_filenames(self, source):
        """
            Walk through all files and yield one of the following:

            * (1, rootdir, dirname, None)
            * (2, rootdir, dirname, filename)

        """
        zipobject = self.zip

        source_str = str(source)
        root_index = len(source_str) + 1

        exclude = []
        #for exc in root_exclude:
        #    exclude.extend(glob.glob(str(source.joinpath(exc))))

        for path in zipobject.filelist:

            full_root = path.filename
            if not full_root.startswith(source_str):
                continue

            root = full_root[root_index:]

            skip = False
            for exc in exclude:
                if full_root.startswith(exc):
                    skip = True

            if skip:
                continue

            if path.is_dir():
                yield 1, root.strip("/"), None
            else:
                parent, _sep, fn = root.rpartition("/")
                yield 2, parent, fn