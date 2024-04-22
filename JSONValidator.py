import re

class ResourceFieldValidation:
    def __init__(self):
        self.json = None
        self.length = 0
        self.resource_result = True

    def validate(self, path):
        if not self.open_json(path):
            return False
        try:
            index = 0
            index += self.whitespace_matcher(index)
            if self.json[index] == '{':
                self.object_validator(index + 1)
            return self.resource_result
        except Exception as e:
            print(f"Error: {e}")
            return True

    def open_json(self, path):
        try:
            with open(path, 'r') as file:
                self.json = file.read()
                self.length = len(self.json)
            return True
        except FileNotFoundError:
            print(f"Error: File {path} not found")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    
    def whitespace_matcher(self, index):
        i = 0
        while index + 1 < self.length and re.match(r'\s', self.json[index + i]):
            i += 1
        return i
    
    def string_matcher(self, index):
        index += 1
        while index + 1 < self.length and self.json[index] != '"':
            index += 1
        index += 1
        return index
    
    def number_matcher(self, index):
        if self.json[index] == '-':
            index += 1
        while index + 1 < self.length and re.match(r'\d', self.json[index]):
            index += 1
        if self.json[index] == '.':
            index += 1
            while index + 1 < self.length and re.match(r'\d', self.json[index]):
                index += 1
        return index
    
    def boolean_matcher(self, index):
        if self.json[index:index+4] == "true":
            index += 4
        elif self.json[index:index+5] == "false":
            index += 5
        return index
    
    def null_matcher(self, index):
        if self.json[index:index+4] == "null":
            index += 4
        return index
    

    def value_matcher(self, index, resource_flag):
        if resource_flag:
            if self.json[index] == '"':
                index += 1
                if self.json[index] == '*' and self.json[index + 1] == '"':
                    self.resource_result = False
                    index += 2
                else:
                    self.resource_result = True
                    while self.json[index] != '"':
                        index += 1
                    index += 1
                return index
            else:
                self.resource_result = True

        # Check if the value is a string
        if self.json[index] == '"':
            index = self.string_matcher(index)

        # Check if the value is an object
        elif self.json[index] == '{':
            index = self.object_validator(index + 1)

        # Check if the value is an array
        elif self.json[index] == '[':
            index = self.array_validator(index + 1)
            
        # Check if the value is a number, int or float
        elif re.match(r'\d', self.json[index]) or self.json[index] == '-':
            index = self.number_matcher(index)

        # Check if the value is a boolean
        elif self.json[index] == 't' or self.json[index] == 'f':
           index = self.boolean_matcher(index)

        # Check if the value is null
        elif self.json[index] == 'n':
            index = self.null_matcher(index)

        # Error
        else:
            raise Exception("Error: Invalid value")
        index += self.whitespace_matcher(index)
        return index
    

    def object_validator(self, index):
        while True:
            resource_flag = False
            index += self.whitespace_matcher(index)
            if self.json[index] == '}':
                return index + 1
            if self.json[index] == '"':
                index += 1
                if index + 8 < self.length and self.json[index:index+8] == "Resource":
                    index += 8
                    resource_flag = True
                else:
                    while self.json[index] != '"':
                        index += 1

                index += 1
                index += self.whitespace_matcher(index)

                if self.json[index] != ':':
                    raise Exception("Error: Expected ':'")
                else:
                    index += 1
                    index += self.whitespace_matcher(index)

                index = self.value_matcher(index, resource_flag)

                index += self.whitespace_matcher(index)
                
                if self.json[index] == ',':
                    index += 1
                    index += self.whitespace_matcher(index)
                elif self.json[index] != '}':
                    raise Exception("Error: Expected ',' or '}'")
            else:
                raise Exception("Error: Expected '}' or '\"'")
            

    def array_validator(self, index):
        while True:
            index += self.whitespace_matcher(index)
            if self.json[index] == ']':
                return index + 1
            index = self.value_matcher(index, False)
            if self.json[index] == ',':
                index += 1
                index += self.whitespace_matcher(index)
            elif self.json[index] != ']':
                raise Exception("Error: Expected ',' or ']'")