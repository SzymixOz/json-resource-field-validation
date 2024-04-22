import os
import unittest
from JSONValidator import ResourceFieldValidation


class TestResourceFieldValidation(unittest.TestCase):
    @classmethod
    def save_json(cls, path, json):
        with open(path, 'w') as file:
            file.write(json)

    def test_single_asterisk(self):
        validator = ResourceFieldValidation()
        input_json = '''{
            "Resource": "*" 
            }'''
        self.save_json('test_file.json', input_json)
        self.assertFalse(validator.validate('test_file.json'), input_json)
        os.remove('test_file.json')

    def test_multiple_asterisks(self):
        validator = ResourceFieldValidation()
        input_json = '''{
            "Resource": "**" 
            }'''
        self.save_json('test_file.json', input_json)
        self.assertTrue(validator.validate('test_file.json'), input_json)
        os.remove('test_file.json')

    def test_no_asterisk(self):
        validator = ResourceFieldValidation()
        input_json = '''{
            "Resource": "arn:aws:s3:::my-bucket/my-object" 
            }'''
        self.save_json('test_file.json', input_json)
        self.assertTrue(validator.validate('test_file.json'), input_json)
        os.remove('test_file.json')

    def test_empty_resource(self):
        validator = ResourceFieldValidation()
        input_json = '''{
            "Resource": "" 
            }'''
        self.save_json('test_file.json', input_json)
        self.assertTrue(validator.validate('test_file.json'), input_json)
        os.remove('test_file.json')

    def test_null_resource(self):
        validator = ResourceFieldValidation()
        input_json = '''{
            "Resource": null 
            }'''
        self.save_json('test_file.json', input_json)
        self.assertTrue(validator.validate('test_file.json'), input_json)
        os.remove('test_file.json')

    def test_invalid_resource_type(self):
        validator = ResourceFieldValidation()
        input_json = '''{
            "Resource": 123 
            }'''
        self.save_json('test_file.json', input_json)
        self.assertTrue(validator.validate('test_file.json'), input_json)
        os.remove('test_file.json')

    def test_no_resource_field(self):
        validator = ResourceFieldValidation()
        input_json = '''{
            "NotResource": "*" 
            }'''
        self.save_json('test_file.json', input_json)
        self.assertTrue(validator.validate('test_file.json'), input_json)
        os.remove('test_file.json')

    def test_1(self):
        validator = ResourceFieldValidation()
        self.assertFalse(validator.validate('test_1.json'))    
    
    def test_2(self):
        validator = ResourceFieldValidation()
        self.assertTrue(validator.validate('test_2.json'))


if __name__ == '__main__':    
    # unittest.main(defaultTest='TestResourceFieldValidation.test_single_asterisk')
    unittest.main()