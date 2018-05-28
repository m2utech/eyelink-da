from multipledispatch import dispatch

class QMatrixProjection(object):

    def qMatrixProjection(self, matrix, positions):
        self.originalMatrix = matrix
        self.positions = positions

    def qProjectionMatrix(self, projection, positions):
        self.originalMatrix = projection.originalMatrix
        self.positions = positions

    def getItemNames(self):
        return self.originalMatrix.itemNames

    def getLocalSequenceUtility(self, position):
        return self.originalMatrix.matrixItemRemainingUtility[position.row][position.column]

    @dispatch(object)
    def getItemUtility(self, position):
        return self.originalMatrix.matrixItemUtility[position.row][position.column]

    @dispatch(int, int)
    def getItemUtility(self, row, column):
        return self.originalMatrix.matrixItemUtility[row][column]

    def getRemainingUtility(self, row, column):
        return self.originalMatrix.matrixItemRemainingUtility[row][column]