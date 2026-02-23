from abc import ABC, abstractmethod
from pathlib import Path
from typing import Final


class BaseFileReader(ABC):
    """ファイル読み込みの基底クラス"""

    def __init__(self, file_path: str | Path):
        self.file_path: Final = Path(file_path)
        self.validate()

    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """許可する拡張子のリスト"""

    @abstractmethod
    def load(self) -> list[str]:
        """ファイルを文字列リストとして返す"""

    def validate(self) -> None:
        """ファイルの検証"""
        self._validate_extension()
        self._validate_file_readable()

    def _validate_file_readable(self) -> None:
        """ファイルが開けるか確認"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"指定されたパスにファイルが存在しません: {self.file_path}")
        if not self.file_path.is_file():
            raise IsADirectoryError(f"指定されたパスがディレクトリです: {self.file_path}")

        # ファイルオープンチェック
        try:
            with self.file_path.open("r", encoding="utf-8"):
                pass
        except (PermissionError, OSError) as e:
            raise PermissionError(f"ファイルにアクセスできません: {self.file_path}") from e

    def _validate_extension(self) -> None:
        """許可された拡張子か確認"""
        actual_extension = self.file_path.suffix.lower()
        if actual_extension not in self.supported_extensions:
            raise ValueError(f"不正な拡張子です: {actual_extension}")
