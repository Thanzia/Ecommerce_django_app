import json
import unicodedata

# 1. Read original data as UTF-8 bytes
with open("data.json", "rb") as f:
    raw_data = f.read()

# 2. Decode with errors ignored (removes invalid bytes)
text = raw_data.decode("utf-8", errors="ignore")

# 3. Load JSON
data = json.loads(text)

# 4. Normalize all string fields (NFKD form keeps special characters safe)
def normalize(obj):
    if isinstance(obj, str):
        return unicodedata.normalize("NFKD", obj)
    elif isinstance(obj, list):
        return [normalize(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items()}
    else:
        return obj

normalized_data = normalize(data)

# 5. Save cleaned JSON
with open("data_fixed.json", "w", encoding="utf-8") as f:
    json.dump(normalized_data, f, indent=4, ensure_ascii=False)

print("✅ Fixed JSON saved as data_fixed.json")
