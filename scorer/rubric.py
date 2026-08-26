from dataclasses import dataclass
import yaml


@dataclass
class Dimension:
    name: str
    description: str
    anchors: dict[int, str]


@dataclass
class Rubric:
    task: str
    dimensions: list[Dimension]
    judge_model: str

    def dimension_names(self) -> list[str]:
        return [d.name for d in self.dimensions]


def load_rubric(path: str) -> Rubric:
    with open(path) as f:
        raw = yaml.safe_load(f)
    dims = [
        Dimension(name=d["name"], description=d["description"], anchors=d["anchors"])
        for d in raw["dimensions"]
    ]
    return Rubric(task=raw["task"], dimensions=dims, judge_model=raw.get("judge_model", "gpt-4o"))
