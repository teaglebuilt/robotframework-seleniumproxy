from SeleniumProxy.proxy.storage import RequestStorage
from datetime import datetime, timedelta
from http.client import HTTPMessage
from unittest.mock import Mock
from unittest import TestCase
from fnmatch import fnmatch
from io import BytesIO
import glob
import gzip
import os
import pickle
import shutil


class RequestStorageTest(TestCase):

    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_initialize(self):
        RequestStorage(base_dir=self.base_dir)
        storage_dir = glob.glob(os.path.join(self.base_dir, '.seleniumproxy', 'storage-*'))
        self.assertEqual(len(storage_dir), 1)
    
    def test_cleanup_removes_storage(self):
        storage = RequestStorage(base_dir=self.base_dir)
        storage.cleanup()
        self.assertFalse(os.listdir(self.base_dir))

    def test_cleanup_does_not_remove_parent_folder(self):
        # There is an existing storage folder
        os.makedirs(os.path.join(self.base_dir, '.seleniumproxy', 'teststorage'))
        storage = RequestStorage(base_dir=self.base_dir)
        storage.cleanup()

        # The existing storage folder is not cleaned up
        self.assertEqual(len(os.listdir(self.base_dir)), 1)
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, '.seleniumproxy', 'teststorage')))

    def test_initialize_clears_old_folders(self):
        old_dir = os.path.join(self.base_dir, '.seleniumproxy', 'storage-test1')
        new_dir = os.path.join(self.base_dir, '.seleniumproxy', 'storage-test2')
        os.makedirs(old_dir)
        os.makedirs(new_dir)
        one_day_ago = (datetime.now() - timedelta(days=1)).timestamp()
        os.utime(old_dir, times=(one_day_ago, one_day_ago))

        RequestStorage(base_dir=self.base_dir)

        self.assertFalse(os.path.exists(old_dir))
        self.assertTrue(os.path.exists(new_dir))

    def test_get_cert_dir(self):
        storage = RequestStorage(base_dir=self.base_dir)

        self.assertTrue(fnmatch(storage.get_cert_dir(),
                                os.path.join(self.base_dir, '.seleniumproxy', 'storage-*', 'certs')))

    def tearDown(self):
        shutil.rmtree(os.path.join(self.base_dir), ignore_errors=False)