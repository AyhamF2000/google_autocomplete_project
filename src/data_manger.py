class DataManager:
    line_contents = {}
    word_mappings = {}

    @classmethod
    def set_data(cls, line_data, word_data):
        cls.line_contents = line_data
        cls.word_mappings = word_data

    @classmethod
    def get_line_contents(cls):
        return cls.line_contents

    @classmethod
    def get_word_mappings(cls):
        return cls.word_mappings
