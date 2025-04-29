from typing import TypeVar

T = TypeVar("T")


class OutputBuffer[T]:
    def __init__(self):
        self._output_buffer: list[T] = []

    def get_output_buffer(self, clear=True) -> list[T]:
        output = self._output_buffer[:]
        if clear:
            self._output_buffer.clear()
        return output


class InputBuffer[T]:
    def __init__(self):
        self._input_buffer: list[T] = []

    def add_input_buffer(self, buffer: list[T]):
        self._input_buffer += buffer


class Buffer(OutputBuffer, InputBuffer): ...
