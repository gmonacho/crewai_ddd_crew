import json
from pathlib import Path
from typing import Any, Type
import ast
import logging

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class _PackageReader:

    def __init__(self, package_path: Path):
        self.logger = logging.getLogger(__name__)
        self._package_path = package_path

    def read_package_context(self) -> dict[str, Any]:
        return {"code_structure": self._extract_code_structure(self._package_path)}

    def _extract_code_structure(self, package_path: Path) -> dict[str, Any]:
        code_structure = {}
        for file_path in package_path.rglob("*"):
           if 'venv' not in str(file_path):
               if file_path.suffix == '.py':
                   relative_file_path = file_path.relative_to(package_path)
                   file_structure = self._analyze_python_file(file_path)
                   code_structure[str(relative_file_path)] = file_structure

        return code_structure

    @staticmethod
    def _analyze_python_file(file_path: Path) -> dict[str, Any]:
       with open(file_path, 'r') as f:
           return {
               "code": f.read()
           }

class PythonPackageContextReader(BaseTool):
    name: str = "Python Package Context Reader"
    description: str = (
        "Parse and analyse a python package"
    )
    project_path: Path = Field(description="The path of the package to anaylse")

    def _run(self) -> str:
        reader = _PackageReader(self.project_path)
        context = reader.read_package_context()
        return json.dumps(context)
