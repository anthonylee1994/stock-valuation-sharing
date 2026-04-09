"""
驗證估值 JSON 檔案係咪符合 schema。
"""

import json
from dataclasses import dataclass

from jsonschema import ValidationError, validate

from stock_valuation.data import SCHEMA_PATH, VALUATION_DIR


@dataclass(frozen=True)
class ValidationIssue:
    filename: str
    message: str
    path: str
    issue_type: str


def collect_valuation_validation_issues() -> list[ValidationIssue]:
    """收集 data/valuation 目錄下所有 JSON 驗證問題。"""
    with SCHEMA_PATH.open(encoding="utf-8") as file:
        schema = json.load(file)

    json_files = sorted(path for path in VALUATION_DIR.glob("*.json") if path.name != "schema.json")
    issues: list[ValidationIssue] = []

    for json_file in json_files:
        try:
            with json_file.open(encoding="utf-8") as file:
                data = json.load(file)

            validate(instance=data, schema=schema)

        except ValidationError as error:
            issues.append(
                ValidationIssue(
                    filename=json_file.name,
                    message=error.message,
                    path=" -> ".join(str(path) for path in error.path) or "<root>",
                    issue_type="schema",
                )
            )

        except json.JSONDecodeError as error:
            issues.append(
                ValidationIssue(
                    filename=json_file.name,
                    message=str(error),
                    path="<json>",
                    issue_type="json",
                )
            )

    return issues


def validate_valuation_files() -> bool:
    """驗證 data/valuation 目錄下所有 JSON 檔案。"""
    json_files = sorted(path for path in VALUATION_DIR.glob("*.json") if path.name != "schema.json")
    issues = collect_valuation_validation_issues()

    print(f"🔍 開始驗證 {len(json_files)} 個 JSON 檔案...\n")

    if not issues:
        for json_file in json_files:
            print(f"✅ {json_file.name} - 驗證通過")
    else:
        invalid_files = {issue.filename for issue in issues}
        for json_file in json_files:
            if json_file.name not in invalid_files:
                print(f"✅ {json_file.name} - 驗證通過")

        for issue in issues:
            failure_label = "JSON 格式錯誤" if issue.issue_type == "json" else "驗證失敗"
            print(f"❌ {issue.filename} - {failure_label}")
            print(f"   錯誤: {issue.message}")
            print(f"   路徑: {issue.path}\n")

    print("\n" + "=" * 50)
    if not issues:
        print("🎉 所有檔案驗證通過！")
    else:
        print("⚠️  部分檔案驗證失敗，請檢查上面嘅錯誤訊息")
    print("=" * 50)

    return not issues
