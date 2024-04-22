import sys
from JSONValidator import ResourceFieldValidation

if __name__ == '__main__':
    validator = ResourceFieldValidation()
    print(validator.validate(sys.argv[1]))
