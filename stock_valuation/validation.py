"""
驗證估值 JSON 檔案係咪符合 schema。
"""

import json

from jsonschema import ValidationError, validate

from stock_valuation.data import SCHEMA_PATH, VALUATION_DIR


def validate_valuation_files() -> bool:
    """驗證 data/valuation 目錄下所有 JSON 檔案。"""
    with SCHEMA_PATH.open(encoding="utf-8") as file:
        schema = json.load(file)

    json_files = sorted(path for path in VALUATION_DIR.glob("*.json") if path.name != "schema.json")

    print(f"🔍 開始驗證 {len(json_files)} 個 JSON 檔案...\n")

    all_valid = True
    for json_file in json_files:
        try:
            with json_file.open(encoding="utf-8") as file:
                data = json.load(file)

            validate(instance=data, schema=schema)
            print(f"✅ {json_file.name} - 驗證通過")

        except ValidationError as error:
            all_valid = False
            print(f"❌ {json_file.name} - 驗證失敗")
            print(f"   錯誤: {error.message}")
            print(f"   路徑: {' -> '.join(str(path) for path in error.path)}\n")

        except json.JSONDecodeError as error:
            all_valid = False
            print(f"❌ {json_file.name} - JSON 格式錯誤")
            print(f"   錯誤: {error}\n")

    print("\n" + "=" * 50)
    if all_valid:
        print("🎉 所有檔案驗證通過！")
    else:
        print("⚠️  部分檔案驗證失敗，請檢查上面嘅錯誤訊息")
    print("=" * 50)

    return all_valid
