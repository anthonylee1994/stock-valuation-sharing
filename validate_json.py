"""
驗證所有估值 JSON 檔案係咪符合 schema
"""

import json
from pathlib import Path
from jsonschema import validate, ValidationError


def validate_valuation_files():
    """驗證 data/valuation 目錄下所有 JSON 檔案"""
    valuation_dir = Path(__file__).parent / "data" / "valuation"
    schema_path = valuation_dir / "schema.json"

    # 讀取 schema
    with open(schema_path) as f:
        schema = json.load(f)

    # 獲取所有 JSON 檔案（除咗 schema.json）
    json_files = [f for f in valuation_dir.glob("*.json") if f.name != "schema.json"]

    print(f"🔍 開始驗證 {len(json_files)} 個 JSON 檔案...\n")

    all_valid = True
    for json_file in sorted(json_files):
        try:
            with open(json_file) as f:
                data = json.load(f)

            # 驗證
            validate(instance=data, schema=schema)
            print(f"✅ {json_file.name} - 驗證通過")

        except ValidationError as e:
            all_valid = False
            print(f"❌ {json_file.name} - 驗證失敗")
            print(f"   錯誤: {e.message}")
            print(f"   路徑: {' -> '.join(str(p) for p in e.path)}\n")

        except json.JSONDecodeError as e:
            all_valid = False
            print(f"❌ {json_file.name} - JSON 格式錯誤")
            print(f"   錯誤: {e}\n")

    print("\n" + "=" * 50)
    if all_valid:
        print("🎉 所有檔案驗證通過！")
    else:
        print("⚠️  部分檔案驗證失敗，請檢查上面嘅錯誤訊息")
    print("=" * 50)

    return all_valid


if __name__ == "__main__":
    validate_valuation_files()
