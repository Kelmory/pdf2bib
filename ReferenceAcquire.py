import re


def flatten(arr):
    for a in arr:
        if isinstance(a, list):
            yield from flatten(a)
        else:
            yield a


class ReferenceAcq:
    def __init__(self, text):
        self._references = []
        self._confidence = {}
        self._reference_pattern = r"^参考文献.*\n$"
        self._ref_split_pattern = r"\n\d{1,2}\."
        self._text = text

    def get_reference(self):
        ref_buffers = []
        for i in range(len(self._text)):
            if re.match(self._reference_pattern, self._text[i]):
                ref_buffers = self._text[i + 1:]
                break

        single_refs = []
        for ref in ref_buffers:
            single_refs.append(re.split(self._ref_split_pattern, ref))
        single_refs = list(flatten(single_refs))

        for ref in single_refs:
            ref = ref.replace('-\n', '')
            ref = ref.replace('\n', ' ')
            ref = ref.split(': ', maxsplit=1)[1]
            ref = ref.split('. ', maxsplit=1)[0]
            self._references.append(ref)
        return self._references
