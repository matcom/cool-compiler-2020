class error:
    def __init__(self, error_type, row_and_col, message):
        self.error_type = error_type
        self.row_and_col = row_and_col
        self.message = message

    def __str__(self):
        return '(%d, %d) - %s: %s' %(self.row_and_col[0], self.row_and_col[1], self.error_type, self.message)

    __repr__ = __str__