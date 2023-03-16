import unittest

from assignment2 import *

from tester_base import TesterBase

class Tests(TesterBase):
    def testQ1ProvidedCases(self):
        roads = [(0,1,4),(1,2,2),(2,3,3),(3,4,1),(1,5,2),
            (5,6,5),(6,3,2),(6,4,3),(1,7,4),(7,8,2),
            (8,7,2),(7,3,2),(8,0,11),(4,3,1),(4,8,10)]
        cafes = [(5,10),(6,1),(7,5),(0,3),(8,4)]
        g = RoadGraph(roads,cafes)
        routingInputList = [(1,7),(7,8),(1,3),(1,4),(3,4)]

        expectedOutputList = [[1,7],[7, 8],[1, 5, 6, 3],[1, 5, 6, 4],[3, 4, 8, 7, 3, 4]]
        testList = [(routingInputList[i][0],routingInputList[i][1],expectedOutputList[i]) 
            for i in range(len(routingInputList))]

        for (start,end,output) in testList:
            with self.subTest(i=(start,end,output)):
                self.assertEqual(g.routing(start,end),output)
    def testQ1CustomCase1(self):
        roads = [
            (0,1,1),(0,5,9),(0,11,2),
            (1,2,1),(1,3,1),
            (2,6,8),

            (4,10,1),
            (5,0,1),(5,4,1),(5,6,3),
            (6,5,1),(6,7,10),
            (7,5,1),
            (8,7,4),(8,9,1),(8,10,1),
            (9,8,1),
            (10,5,10),(10,8,1),
            (11,4,1),
        ]
        cafes = [(3,1),(5,20),(6,4),(9,2),(11,1)]
        g = RoadGraph(roads,cafes)

        routingInputList = [(7,1),(1,7),(8,10),(1,1),
                            (0,0),(6,6),(5,5),(9,3)]
        expectedOutputList = [[7,5,6,5,0,1],[1,2,6,5,4,10,8,7],[8,9,8,10],[1,2,6,5,0,1],
                              [0,11,4,10,8,7,5,0],[6],[5,6,5],[9,8,7,5,0,1,3]]
        testList = [(routingInputList[i][0],routingInputList[i][1],expectedOutputList[i]) 
            for i in range(len(routingInputList))]
        for (start,end,output) in testList:
            with self.subTest(i=(start,end,output)):
                self.assertEqual(g.routing(start,end),output)

    # ----------------------------------------------------------------------------------------------
    def testQ2ProvidedCase(self):
        downhillScores = [(0, 6, -500), (1, 4, 100), (1, 2, 300),
                (6, 3, -100), (6, 1, 200), (3, 4, 400), (3, 1, 400),
                (5, 6, 700), (5, 1, 1000), (4, 2, 100)]
        start = 6 
        finish = 2 
        self.assertEqual(optimalRoute(downhillScores,start,finish),[6,3,1,2])

    def testQ2CustomCase1(self):
        downhillScores = [
            # layer 1
            (9,10,50),
            # layer 2
            (0,1,100),(0,3,-200),
            (10,5,50),(10,15,150),
            # layer 3
            (1,2,50),(1,3,0),(1,6,100),
            (5,6,0),(5,11,-50),(5,12,100),
            (15,12,-200),(15,16,0),
            # layer 4
            (2,3,50),(2,7,100),
            (6,7,-50),(6,8,200),
            (12,13,300),
            (16,13,50),(16,17,200),
            # layer 5
            (3,4,100),
            (7,4,200),(7,8,100),
            (13,8,50),(13,14,100),
            (17,14,100)
            # layer 6
        ]

        testList = [(9,10,[9,10]),(9,12,[9,10,5,12]),(0,3,[0,1,2,3]),(10,13,[10,5,12,13]),
                    (15,13,[15,12,13]),(15,14,[15,16,17,14]),(9,14,[9,10,5,12,13,14]),
                    (1,7,[1,2,7]),(10,7,[10,5,6,7]),(0,8,[0,1,6,8]),(9,8,[9,10,5,12,13,8]),
                    (11,11,[11]),(9,4,[9,10,5,6,7,4]),(10,3,None),(2,1,None)]
        for (start,finish,output) in testList:
            with self.subTest(i=(start,finish,output)):
                self.assertEqual(optimalRoute(downhillScores,start,finish),output)
    def testQ2CustomCase2(self):
        downhillScores = [(0,1,0),(0,2,50),(2,3,50),(3,4,50),(4,5,50),(5,1,50),(1,6,50),(6,7,50)]
        start = 0
        finish = 7 
        self.assertEqual(optimalRoute(downhillScores,start,finish),[0,2,3,4,5,1,6,7])
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    unittest.TextTestRunner(verbosity=0).run(suite)


