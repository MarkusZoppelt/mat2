import subprocess
import json
import zipfile
import tempfile
import shutil
import os

from . import abstract, parser_factory

class OfficeParser(abstract.AbstractParser):
    mimetypes = {
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation'
    }
    files_to_keep = {'_rels/.rels', 'word/_rels/document.xml.rels'}

    def get_meta(self):
        metadata = {}
        zipin = zipfile.ZipFile(self.filename)
        for item in zipin.namelist():
            if item.startswith('docProps/'):
                metadata[item] = 'harmful content'
        zipin.close()
        return metadata

    def remove_all(self):
        zin = zipfile.ZipFile(self.filename, 'r')
        zout = zipfile.ZipFile(self.output_filename, 'w')
        temp_folder = tempfile.mkdtemp()

        for item in zin.infolist():
            if item.is_dir():
                continue
            elif item.filename.startswith('docProps/'):
                if not item.filename.endswith('.rels'):
                    continue  # don't keep metadata files
            if item.filename in self.files_to_keep:
                zout.writestr(item, zin.read(item))
                continue

            zin.extract(member=item, path=temp_folder)
            tmp_parser = parser_factory.get_parser(os.path.join(temp_folder, item.filename))
            if tmp_parser is None:
                print("%s isn't supported" % item.filename)
                continue
            tmp_parser.remove_all()
            zout.write(tmp_parser.output_filename, item.filename)
        shutil.rmtree(temp_folder)
        zout.close()
        zin.close()
        return True