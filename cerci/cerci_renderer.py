from __future__ import print_function
from django.conf import settings
from django.test.client import Client
import mimetypes
import os
from django_medusa.renderers.base import (COMMON_MIME_MAPS,
                                          BaseStaticSiteRenderer)

__all__ = ('CerciStaticSiteRenderer', )


# Unfortunately split out from the class at the moment to allow rendering with
# several processes via `multiprocessing`.
# TODO: re-implement within the class if possible?
def _disk_render_path(args):
    client, path, view = args
    if not client:
        client = Client()
    if path:
        DEPLOY_DIR = settings.MEDUSA_DEPLOY_DIR
        realpath = path
        if path.startswith("/"):
            realpath = realpath[1:]

        if path.endswith("/"):
            needs_ext = True
        else:
            needs_ext = False

        output_dir = os.path.abspath(os.path.join(
            DEPLOY_DIR,
            os.path.dirname(realpath)
        ))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        outpath = os.path.join(DEPLOY_DIR, realpath)

        resp = client.get(path)
        if resp.status_code != 200:
            print('Page is unreachable: %s' % path)
        if needs_ext:
            mime = resp['Content-Type']
            mime = mime.split(';', 1)[0]

            # Check our override list above first.
            ext = COMMON_MIME_MAPS.get(
                mime,
                mimetypes.guess_extension(mime)
            )
            if ext:
                outpath += "index" + ext
            else:
                # Default to ".html"
                outpath += "index.html"
        else:
            outpath += '/index.html'
            if not os.path.exists(os.path.dirname(outpath)):
                os.makedirs(os.path.dirname(outpath))
        print(outpath)
        with open(outpath, 'wb') as f:
            f.write(resp.content)


class CerciStaticSiteRenderer(BaseStaticSiteRenderer):

    def render_path(self, path=None, view=None):
        _disk_render_path((self.client, path, view))

    def generate(self):
        if getattr(settings, "MEDUSA_MULTITHREAD", False):
            # Upload up to ten items at once via `multiprocessing`.
            from multiprocessing import Pool, cpu_count

            print("Generating with up to %d processes..." % cpu_count())
            pool = Pool(cpu_count())

            pool.map_async(
                _disk_render_path,
                ((None, path, None) for path in self.paths),
                chunksize=5
            )
            pool.close()
            pool.join()
        else:
            # Use standard, serial upload.
            self.client = Client()
            for path in self.paths:
                self.render_path(path=path)
