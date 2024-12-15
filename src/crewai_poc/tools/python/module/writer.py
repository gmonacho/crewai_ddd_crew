import json
from pathlib import Path
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class _ModuleWriter:

    def __init__(self, package_path: Path):
        self._package_path = package_path

    def write_module(self, relative_file_path: Path, code: str) -> None:
        full_path = self._package_path / relative_file_path
        if "domain" in relative_file_path.parts:
            raise ValueError(f"Invalid path {full_path}")

        full_path = self._package_path / relative_file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, 'w') as f:
            f.write(code)


class PythonModuleWriterInput(BaseModel):
    relative_file_path: str = Field(description="the path of the file to write")
    code: str = Field(description="the python code to write in the file")

class PythonModuleWriter(BaseTool):
    name: str = "Python Module Writer"
    description: str = (
        "Write a python module"
    )
    project_path: Path = Field(description="The path of the package where the python module can be writed")
    args_schema: Type[BaseModel] = PythonModuleWriterInput

    def _run(self, relative_file_path: str, code: str) -> str:
        writer = _ModuleWriter(self.project_path)
        writer.write_module(Path(relative_file_path), code)
        return "Module has been writed correctly"
