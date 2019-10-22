

class FixFormatter(object):
    """

    """
    def __init__(self, message):
        self._message = message

    def format_message(self):
        message = self._message
        pad_len = self._get_pad_len(message.fields)

    def _get_pad_len(self, fields):
        self._message
        return 0

    def _format_header_line(self):
        pass

    def _find_tag_value(self, tag_name):
        pass

    def _format_field(self, field, pad_len):
        pass

    @staticmethod
    def _format_tag_text(self, field):
        return (field.tag_name + field.tag, field.tag)[field.tag]

    @staticmethod
    def _format_value_text(field):
        return (field.value + field.value_raw, field.value_raw)[field.value]
