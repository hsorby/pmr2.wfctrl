from unittest import TestCase

import os
from os.path import join
import tempfile
import shutil


class CoreTestCase(TestCase):

    def setUp(self):
        self.working_dir = tempfile.mkdtemp()
        self.workspace_dir = os.path.join(self.working_dir, 'workspace')
        os.mkdir(self.workspace_dir)

    def tearDown(self):
        shutil.rmtree(self.working_dir)

    def make_workspace(self):
        raise NotImplementedError


class CoreTests(object):
    """
    Core test methods.
    """

    def write_file(self, content='', name=None):
        """
        Write contents to file.  There are no safeties, use with care.

        name
            The name of the file.  It will be forced into the current
            working_dir if not already inside.
        """

        if name is None:
            filename = tempfile.mktemp(dir=self.workspace_dir)
        else:
            if not name.startswith(self.workspace_dir):
                filename = os.path.join(self.workspace_dir, name)
            else:
                filename = name

        with open(filename, mode='w') as fd:
            fd.write(content)

        return filename

    def test_create_workspace(self):
        wks = self.make_workspace()
        self.assertTrue(os.path.exists(self.workspace_dir))

    def test_add_files_simple(self):
        wks = self.make_workspace()
        fn = self.write_file('Test content')
        wks.add_file(fn)

        self.assertEqual(wks.get_tracked_subpaths(), [os.path.basename(fn)])
        wks.save()

    def test_add_files_multi(self):
        wks = self.make_workspace()
        fn1 = self.write_file('Test content1')
        fn2 = self.write_file('Test content2')
        fn3 = self.write_file('Test content3')
        wks.add_file(fn1)
        wks.add_file(fn2)
        wks.add_file(fn3)

        self.assertEqual(wks.get_tracked_subpaths(),
            [os.path.basename(f) for f in sorted([fn1, fn2, fn3])])
        wks.save()

    def test_add_files_nested(self):
        wks = self.make_workspace()
        os.mkdir(join(self.workspace_dir, 'testdir'))
        fn1 = self.write_file('Test content1', 'file1')
        fn2 = self.write_file('Test content2', join('testdir', 'file2'))
        # full path.
        fn3 = self.write_file('Test content3',
            join(self.workspace_dir, 'testdir', 'file3'))
        wks.add_file(fn1)
        wks.add_file(fn2)
        wks.add_file(fn3)

        self.assertEqual(wks.get_tracked_subpaths(),
            ['file1', join('testdir', 'file2'), join('testdir', 'file3')])
        wks.save()

    def test_add_files_outside_workspace(self):
        wks = self.make_workspace()
        fn1 = self.write_file('Failure', join(self.working_dir, 'badname'))
        self.assertRaises(ValueError, wks.add_file, fn1)
        self.assertEqual(wks.get_tracked_subpaths(), [])