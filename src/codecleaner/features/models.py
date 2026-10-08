from dataclasses import dataclass


@dataclass(frozen=True)
class FileFeatures:
    file: str
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    comment_ratio: float
    blank_line_ratio: float
    comment_repetition: float
    duplicate_line_ratio: float
    duplicate_block_signal: float
    boilerplate_density: float
    generated_phrase_density: float
    code_density: float

    def to_dict(self) -> dict:
        return {
            "file": self.file,
            "total_lines": self.total_lines,
            "code_lines": self.code_lines,
            "comment_lines": self.comment_lines,
            "blank_lines": self.blank_lines,
            "comment_ratio": self.comment_ratio,
            "blank_line_ratio": self.blank_line_ratio,
            "comment_repetition": self.comment_repetition,
            "duplicate_line_ratio": self.duplicate_line_ratio,
            "duplicate_block_signal": self.duplicate_block_signal,
            "boilerplate_density": self.boilerplate_density,
            "generated_phrase_density": self.generated_phrase_density,
            "code_density": self.code_density,
        }
