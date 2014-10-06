from elasticgit.tests.base import ModelBaseTest


class TestStorage(ModelBaseTest):

    def setUp(self):
        self.workspace = self.mk_workspace()
        self.index = self.workspace.index
        self.storage = self.workspace.storage

    def tearDown(self):
        if self.workspace.exists():
            self.workspace.destroy()

    def test_exists(self):
        self.assertFalse(self.storage.exists())

    def test_create(self):
        self.storage.create('Test Kees', 'kees@example.org')
        self.assertTrue(self.storage.exists())

    def test_destroy(self):
        self.storage.create('Test Kees', 'kees@example.org')
        self.assertTrue(self.storage.exists())
        self.storage.destroy()
        self.assertFalse(self.storage.exists())