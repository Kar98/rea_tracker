import unittest
import os
from tracker.rea_parser import ReaParser, Article


def get_files_in_dir(folder):
    files = os.listdir(folder)
    tmplist = []
    for f in files:
        tmplist.append(f)
    return tmplist


@unittest.skip("Debug functions")
class TestAppUtilFunctions(unittest.TestCase):
    def test_reset_files(self):
        folder_path = '../pages/buy/'
        files = get_files_in_dir(folder_path)
        for f in files:
            if '-processed.htm' in f:
                os.rename(folder_path+f, folder_path+f.replace('-processed.htm', '.htm'))
        assert(True)


class TestAppFunctions(unittest.TestCase):
    def test_json_audit_format(self):
        audit_path = '../output/buy_audit.txt'
        list1 = ['1 Fake st', 'Faker', '100,000', '2', '1', '100', '10/10/2010', '10/10/2010']
        list2 = ['1 Fake st', 'Faker', '120,000', '2', '1', '100', '10/10/2010', '15/10/2010']
        p1 = ReaParser()
        p1.articles.append(Article(*list1))
        p1.audit = []
        p2 = ReaParser()
        p2.articles.append(Article(*list2))

        p1.merge(p2)

        dic_assert = [{"Address": "1 Fake st,Faker", "Prices": [{"Price": "100,000", "Date": "10/10/2010"}, {"Price": "120,000", "Date": "15/10/2010"}]}]
        self.assertEqual(p1.audit, dic_assert)
