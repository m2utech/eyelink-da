from multipledispatch import dispatch

class QMatrixProjection(object):

    def qMatrixProjection(self, matrix, positions):
        self.originalMatrix = matrix
        self.positions = positions

    def qProjectionMatrix(self, projection, positions):
        self.originalMatrix = projection.originalMatrix
        self.positions = positions

    @dispatch(object)
    def getItemUtility(self, position):
        return self.originalMatrix.matrixItemUtility[position.row][position.column]

    @dispatch(int, int)
    def getItemUtility(self, row, column):
        return self.originalMatrix.matrixItemUtility[row][column]
