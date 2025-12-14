class ReadFileCommand:

    def __init__(self, filenames: list[str]):
        self._filenames = filenames

    def get_filenames(self) -> str:
        return self._filenames