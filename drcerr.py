class DrcError(AttributeError):
    "DRC Semantic or Safety Error"

class UnmatchedVariableError(DrcError):
    "Predicates do not have matching arguments."

class ComparingConstantsError(DrcError):
    "Constants cannot be compared to other constants."

class ConstantAssignedAsFreeError(DrcError):
    "Constant in free variables list"

class TypeMatchingError(DrcError):
    "Types do not match"

class SafetyError(DrcError):
    "Unsafe Query"

class ColumnsError(DrcError):
    "Number of columns do not match"

class TableNameError(DrcError):
    "Table not found"
