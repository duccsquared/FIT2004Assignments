import unittest

from assignment1 import *

from tester_base import TesterBase

class Tests(TesterBase):
    def testAnalysisProvidedCases(self):
        results = [["AAB", "AAB", 35], ["AAB", "BBA", 49], ["BAB", "BAB", 42],
            ["AAA", "AAA", 38], ["BAB", "BAB", 36], ["BAB", "BAB", 36],
            ["ABA", "BBA", 57], ["BBB", "BBA", 32], ["BBA", "BBB", 49],
            ["BBA", "ABB", 55], ["AAB", "AAA", 58], ["ABA", "AAA", 46],
            ["ABA", "ABB", 44], ["BBB", "BAB", 32], ["AAA", "AAB", 36],
            ["ABA", "BBB", 48], ["BBB", "ABA", 33], ["AAB", "BBA", 30],
            ["ABB", "BBB", 68], ["BAB", "BBB", 52]]
        expectedOutput1 = [[["ABB", "AAB", 70],
            ["ABB", "BBB", 68],
            ["AAB", "BBB", 67],
            ["AAB", "AAB", 65],
            ["AAB", "AAA", 64],
            ["ABB", "ABB", 64],
            ["AAA", "AAA", 62],
            ["AAB", "AAA", 58],
            ["ABB", "ABB", 58],
            ["AAB", "ABB", 57]],
            [["AAB", "AAA", 64], ["ABB", "ABB", 64]]]
        expectedOutput2 = [[["ABB", "AAB", 70],
            ["ABB", "BBB", 68],
            ["AAB", "BBB", 67],
            ["AAB", "AAB", 65],
            ["AAB", "AAA", 64],
            ["ABB", "ABB", 64],
            ["AAA", "AAA", 62],
            ["AAB", "AAA", 58],
            ["ABB", "ABB", 58],
            ["AAB", "ABB", 57]],
            [["AAB", "AAA", 64], ["ABB", "ABB", 64]]]
        expectedOutput3 = [[["ABB", "AAB", 70],
            ["ABB", "BBB", 68],
            ["AAB", "BBB", 67],
            ["AAB", "AAB", 65],
            ["AAB", "AAA", 64],
            ["ABB", "ABB", 64],
            ["AAA", "AAA", 62],
            ["AAB", "AAA", 58],
            ["ABB", "ABB", 58],
            ["AAB", "ABB", 57]],
            []]
        expectedOutput4 = [[["ABB", "AAB", 70],
            ["ABB", "BBB", 68],
            ["AAB", "BBB", 67],
            ["AAB", "AAB", 65],
            ["AAB", "AAA", 64],
            ["ABB", "ABB", 64],
            ["AAA", "AAA", 62],
            ["AAB", "AAA", 58],
            ["ABB", "ABB", 58],
            ["AAB", "ABB", 57]],
            [["AAB", "ABB", 30]]]
        testList = [(results,2,64,expectedOutput1),(results,2,63,expectedOutput2),
            (results,2,71,expectedOutput3),(results,2,0,expectedOutput4)]
        for (results, roster, score, expected) in testList:
            with self.subTest(i=("results len %d" % len(results),roster, score)):
                self.assertEqual(analyze(results, roster, score),expected)
    def testAnalysisRandomizedCases(self):
        inputs1 = [[['C', 'A', 54], ['T', 'E', 47], ['S', 'S', 83], ['R', 'C', 57], ['L', 'S', 13], 
            ['C', 'E', 53], ['L', 'F', 79], ['F', 'L', 91]], 
            20, 70]
        expectedOutput1 = [[['F', 'L', 91],['S', 'L', 87],['S', 'S', 83],['L', 'F', 79],['R', 'C', 57],
            ['C', 'A', 54],['C', 'E', 53],  ['E', 'T', 53],['E', 'C', 47],['T', 'E', 47]],
            [['L', 'F', 79]]]
        inputs2 = [[['FFHBF', 'BGEED', 79], ['BBCEG', 'DFAGG', 52], ['AGDCD', 'CDBEC', 51], ['FCFFA', 'EECEF', 3], 
            ['EAAEE', 'GDECG', 89], ['CDFGG', 'ACAAD', 59], ['CAHFE', 'EDHGG', 45], ['BFGGE', 'BBBBE', 65], 
            ['CDGEB', 'GBEHC', 52], ['CHCAE', 'EEABH', 95], ['AEGHF', 'BFBBB', 46], ['CCHAA', 'GBGGH', 43], 
            ['BGBAE', 'EFFEH', 7], ['BDEHC', 'GDCEC', 78], ['FAECF', 'EDFHH', 42], ['DCDFH', 'FHEFA', 29], 
            ['FCDBG', 'ADEFH', 95], ['FEBBC', 'HAEHH', 43], ['AFEHA', 'HGFFH', 10], ['CEBBH', 'CFFBA', 75]],
            8,90]
        expectedOutput2 = [[['CEEEF', 'ACFFF', 97],['ACCEH', 'ABEEH', 95],['BCDFG', 'ADEFH', 95],['EEFFH', 'ABBEG', 93],['FFGHH', 'AAEFH', 90],
            ['AAEEE', 'CDEGG', 89],['BFFFH', 'BDEEG', 79],['BCDEH', 'CCDEG', 78],['BBCEH', 'ABCFF', 75],['AEFFH', 'CDDFH', 71]],
            [['FFGHH', 'AAEFH', 90]]]
        inputs3 = [[['BMDQ', 'JFMC', 2], ['OIKH', 'RKFM', 30], ['DRIP', 'ABMK', 59], ['DPKS', 'AHJD', 29], ['DMEJ', 'ADPL', 18], 
            ['CLAA', 'MNKK', 96], ['EAFI', 'IILC', 88], ['CKPR', 'GRHF', 0], ['LBQC', 'DQTQ', 99], ['LJPR', 'IQEI', 95], 
            ['OTHS', 'RDHP', 94], ['PHBQ', 'GIEM', 87]],20,32]
        expectedOutput3 = [[['FGHR', 'CKPR', 100],['BCLQ', 'DQQT', 99],['CFJM', 'BDMQ', 98],['AACL', 'KKMN', 96],
            ['JLPR', 'EIIQ', 95],['HOST', 'DHPR', 94],['AEFI', 'CIIL', 88],['BHPQ', 'EGIM', 87],
            ['ADLP', 'DEJM', 82],['ADHJ', 'DKPS', 71]],
            [['ABKM', 'DIPR', 41]]]
        inputs4 = [[['EPE', 'HPO', 76], ['HKC', 'MBC', 0], ['MLE', 'ACC', 58], ['FLC', 'ONB', 67], 
            ['KIK', 'GNM', 84], ['ONC', 'GNG', 81]],16,60]
        expectedOutput4 = [[['BCM', 'CHK', 100],['IKK', 'GMN', 84],['CNO', 'GGN', 81],['EEP', 'HOP', 76],
            ['CFL', 'BNO', 67],['ELM', 'ACC', 58],['ACC', 'ELM', 42],['BNO', 'CFL', 33],
            ['HOP', 'EEP', 24],['GGN', 'CNO', 19]],
            [['CFL', 'BNO', 67]]]
        testList = [(inputs1[0],inputs1[1],inputs1[2],expectedOutput1),
            (inputs2[0],inputs2[1],inputs2[2],expectedOutput2),
            (inputs3[0],inputs3[1],inputs3[2],expectedOutput3),
            (inputs4[0],inputs4[1],inputs4[2],expectedOutput4)]
        for (results, roster, score, expected) in testList:
            with self.subTest(i=("results len %d" % len(results),roster, score)):
                self.assertEqual(analyze(results, roster, score),expected)
    def testAnalysisEdgeCases(self):
        results1 = [['CBB', 'ACC', 46], ['AAB', 'DBC', 72], ['DDC', 'DAA', 2], ['ABD', 'DDB', 67]]
        inputs1a = [results1,4,50]
        inputs1b = [results1,4,0]
        inputs1c = [results1,4,100]
        topTen1 = [['AAD', 'CDD', 98],['AAB', 'BCD', 72],['ABD', 'BDD', 67],['ACC', 'BBC', 54],
            ['BBC', 'ACC', 46],['BDD', 'ABD', 33],['BCD', 'AAB', 28], ['CDD', 'AAD', 2]] 
        match1a = [['ACC', 'BBC', 54]]
        match1b = [['CDD', 'AAD', 2]]
        match1c = []
        results2 = [['CBB', 'ACC', 50], ['AAB', 'DBC', 50], ['DDC', 'DAA', 50], ['ABD', 'DDB', 50]]
        inputs2a = [results2,4,50]
        inputs2b = [results2,4,0]
        inputs2c = [results2,4,100]
        topTen2 = [['AAB', 'BCD', 50],['AAD', 'CDD', 50],['ABD', 'BDD', 50],['ACC', 'BBC', 50],
            ['BBC', 'ACC', 50],['BCD', 'AAB', 50],['BDD', 'ABD', 50],['CDD', 'AAD', 50]]
        match2a = topTen2
        match2b = topTen2
        match2c = []
        results3 = [['AAA', 'AAA', 46], ['AAA', 'AAA', 72], ['AAA', 'AAA', 2], ['AAA', 'AAA', 67]]
        inputs3a = [results3,1,50]
        inputs3b = [results3,1,0]
        inputs3c = [results3,1,100]
        topTen3 = [['AAA', 'AAA', 98],['AAA', 'AAA', 72],['AAA', 'AAA', 67],['AAA', 'AAA', 54],
            ['AAA', 'AAA', 46],['AAA', 'AAA', 33],['AAA', 'AAA', 28],['AAA', 'AAA', 2]]
        match3a = [['AAA', 'AAA', 54]]
        match3b = [['AAA', 'AAA', 2]]
        match3c = []
        results4 = [["A","B",0]]
        inputs4a = [results4,3,50]
        inputs4b = [results4,3,0]
        inputs4c = [results4,3,100]
        topTen4 = [["B","A",100],["A","B",0]]
        match4a = [["B","A",100]]
        match4b = [["A","B",0]]
        match4c = [["B","A",100]]
        testList = [(inputs1a[0],inputs1a[1],inputs1a[2],[topTen1,match1a]),
            (inputs1b[0],inputs1b[1],inputs1b[2],[topTen1,match1b]),
            (inputs1c[0],inputs1c[1],inputs1c[2],[topTen1,match1c]),
            (inputs2a[0],inputs2a[1],inputs2a[2],[topTen2,match2a]),
            (inputs2b[0],inputs2b[1],inputs2b[2],[topTen2,match2b]),
            (inputs2c[0],inputs2c[1],inputs2c[2],[topTen2,match2c]),
            (inputs3a[0],inputs3a[1],inputs3a[2],[topTen3,match3a]),
            (inputs3b[0],inputs3b[1],inputs3b[2],[topTen3,match3b]),
            (inputs3c[0],inputs3c[1],inputs3c[2],[topTen3,match3c]),
            (inputs4a[0],inputs4a[1],inputs4a[2],[topTen4,match4a]),
            (inputs4b[0],inputs4b[1],inputs4b[2],[topTen4,match4b]),
            (inputs4c[0],inputs4c[1],inputs4c[2],[topTen4,match4c])]
        for (results, roster, score, expected) in testList:
            with self.subTest(i=("results len %d" % len(results),roster, score)):
                self.assertEqual(analyze(results, roster, score),expected)
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    unittest.TextTestRunner(verbosity=0).run(suite)

