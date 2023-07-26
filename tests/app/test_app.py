from src.app.main import create_item, read_item, read_root


class Test_App:
    def test_read_root(self):
        resp = read_root()
        
        assert resp['version'] == '1'
