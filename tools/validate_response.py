#!/usr/bin/env python3
"""对照 04_decision_response_schema.json 校验 DecisionResponse 的最小实现。

本机无 jsonschema 库，故按 Schema 中实际用到的关键字自行实现：
type / enum / const / required / additionalProperties / properties /
items / maxItems / minItems / minLength / maxLength / uniqueItems / allOf-if-then。
只覆盖本 Schema 使用到的子集；不声称通用 JSON Schema 兼容。

用法: python3 tools/validate_response.py <response.json> [schema.json]
"""
import json
import sys

TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


def check_type(value, expected):
    if isinstance(expected, list):
        return any(check_type(value, e) for e in expected)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    py = TYPES[expected]
    if expected in ("string", "array", "object", "boolean"):
        return isinstance(value, py)
    return isinstance(value, py)


def validate(value, schema, path, errors):
    if "type" in schema and not check_type(value, schema["type"]):
        errors.append(f"{path}: 期望类型 {schema['type']}，实际 {type(value).__name__}")
        return
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: 应等于常量 {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} 不在枚举 {schema['enum']}")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: 长度 {len(value)} < minLength {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{path}: 长度 {len(value)} > maxLength {schema['maxLength']}")
    if isinstance(value, list):
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path}: 元素 {len(value)} > maxItems {schema['maxItems']}")
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: 元素 {len(value)} < minItems {schema['minItems']}")
        if schema.get("uniqueItems"):
            seen = []
            for item in value:
                if item in seen:
                    errors.append(f"{path}: uniqueItems 冲突 {item!r}")
                seen.append(item)
        if "items" in schema:
            for i, item in enumerate(value):
                validate(item, schema["items"], f"{path}[{i}]", errors)
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: 缺少必填字段 {key}")
        props = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    errors.append(f"{path}: 出现 Schema 未定义的字段 {key}")
        for key, sub in props.items():
            if key in value:
                validate(value[key], sub, f"{path}.{key}", errors)
    for clause in schema.get("allOf", []):
        cond = clause.get("if", {})
        ok = True
        for key, sub in cond.get("properties", {}).items():
            if isinstance(value, dict) and key in value:
                if "const" in sub and value[key] != sub["const"]:
                    ok = False
            elif isinstance(value, dict):
                ok = False
        if ok:
            then = clause.get("then", {})
            merged = {k: v for k, v in then.get("properties", {}).items()}
            for key, sub in merged.items():
                if isinstance(value, dict) and key in value:
                    validate(value[key], sub, f"{path}.{key}", errors)


def main():
    resp_path = sys.argv[1]
    schema_path = sys.argv[2] if len(sys.argv) > 2 else "imports/live-inputs/04_decision_response_schema.json"
    with open(schema_path, encoding="utf-8") as fh:
        schema = json.load(fh)
    with open(resp_path, encoding="utf-8") as fh:
        resp = json.load(fh)
    errors = []
    validate(resp, schema, "$", errors)
    mode = resp.get("response_mode")
    print(f"response_mode = {mode}")
    print(f"blocked 约束: root_causes={len(resp.get('root_causes', []))} "
          f"people={len(resp.get('people', []))} actions={len(resp.get('actions', []))}")
    print(f"answer_text 字数 = {len(resp.get('answer_text', ''))}")
    if errors:
        print(f"FAIL: {len(errors)} 处不符合")
        for err in errors:
            print("  -", err)
        sys.exit(1)
    print("PASS: 结构校验通过（手写子集实现，非 jsonschema 库）")


if __name__ == "__main__":
    main()
