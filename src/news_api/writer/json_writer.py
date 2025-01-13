from base_writer import BaseWriter
import jsonlines
class JsonWriter(BaseWriter):
    def write_to_file(self, file_path: str, data):
        with open(file_path, 'w') as output_file:
            json_writer = jsonlines.Writer(output_file)
            json_writer.write_all(data)