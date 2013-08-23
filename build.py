__author__ = 'ynagai'

import htmlmin
import jinja2
import os
import shutil

BUILD_PATH = '_build'


class StaPy:
    def __init__(self):
        self._root = os.path.realpath(os.path.dirname(__name__))
        self._dst = os.path.join(self._root, BUILD_PATH)

    def build(self):
        self._prepare()
        self._copy_static()
        self._render_templates()

    def _prepare(self):
        if not os.path.exists(self._dst):
            os.mkdir(self._dst)

    def _copy_static(self):
        static_dir = os.path.join(self._root, 'static')
        for root, dirs, files in os.walk(static_dir):
            dst = self._dst + root.replace(static_dir, '')

            for name in dirs:
                dst_path = os.path.join(dst, name)
                if not os.path.exists(dst_path):
                    os.mkdir(dst_path)

            for name in files:
                src_path = os.path.join(root, name)
                dst_path = os.path.join(dst, name)
                if not os.path.exists(dst_path) or os.path.getmtime(dst_path) < os.path.getmtime(src_path):
                    shutil.copy2(src_path, dst_path)

            dst_files = os.listdir(dst)
            dst_dirs = [f for f in dst_files if os.path.isdir(os.path.join(dst, f))]
            dst_files = [f for f in dst_files if os.path.isfile(os.path.join(dst, f))]

            # removed dirs
            for name in set(dst_dirs) - set(dirs):
                os.removedirs(os.path.join(root, name))
            # removed files
            for name in set(dst_files) - set(files):
                if not name.endswith('.html'):
                    os.remove(os.path.join(root, name))

    def _render_templates(self):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(self._root, 'templates')))
        templates_dir = os.path.join(self._root, 'templates')
        for name in os.listdir(templates_dir):
            path = os.path.join(templates_dir, name)
            if os.path.isfile(path) and not name.startswith('_') and not name.endswith('~'):
                dst = os.path.join(self._dst, name)
                rendered = env.get_template(name).render()
                rendered = rendered.replace('=\"/static/', '=\"')
                rendered = htmlmin.minify(rendered)
                with open(dst, 'w', encoding='utf-8') as f:
                    f.write(rendered)


if __name__ == '__main__':
    StaPy().build()
