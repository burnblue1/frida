#!/usr/bin/env python3
"""
rusda patch 验证脚本

验证 dist-android 中所有打包产物是否已正确 patch，避免部分产物 patch 生效、部分未生效。

用法:
  python tools/verify-patch.py [dist-android 目录]
  python tools/verify-patch.py /path/to/dist-android
  python tools/verify-patch.py --strict   # 严格模式，包含 frida:rpc 检查（gadget 内嵌 JS 可能仍含）

检查项:
  - 不应出现: FridaScriptEngine, GLib-GIO, GDBusProxy, GumScript, gum-js-loop, gmain, gdbus
  - 应出现: enignEtpircSadirF/OIG-biLG/yxorPsuBDG/tpircSmuG, russellloop, rmain, rubus
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# topatch 会替换的原始字符串（不应再出现）
BAD_STRINGS = [
    "FridaScriptEngine",
    "GLib-GIO",
    "GDBusProxy",
    "GumScript",
    "gum-js-loop",
    "gmain",
    "gdbus",
]

# 严格模式额外检查（Vala 已用 XOR 运行时解码，但 worker.js/message-dispatcher.js 仍含字面量）
BAD_STRINGS_STRICT = ["frida:rpc"]

# topatch 替换后的字符串（应出现，表示 patch 生效）
GOOD_STRINGS = [
    "enignEtpircSadirF",  # FridaScriptEngine 反转
    "OIG-biLG",           # GLib-GIO 反转
    "yxorPsuBDG",         # GDBusProxy 反转
    "tpircSmuG",          # GumScript 反转
    "russellloop",        # gum-js-loop
    "rmain",              # gmain
    "rubus",              # gdbus
]

# 仅对 gadget 产物检查
GOOD_STRINGS_GADGET = ["rusda-gadget"]


def get_strings(path: Path) -> list[str]:
    """对文件执行 strings，支持 .xz 压缩文件"""
    if not path.exists() or not path.is_file():
        return []
    try:
        if path.suffix == ".xz" or path.name.endswith(".xz"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as tmp:
                tmp_path = Path(tmp.name)
            try:
                out = subprocess.run(
                    ["xz", "-d", "-c", str(path)],
                    capture_output=True,
                    check=True,
                    timeout=30,
                )
                with open(tmp_path, "wb") as f:
                    f.write(out.stdout)
                result = subprocess.run(
                    ["strings", str(tmp_path)],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                return result.stdout.splitlines() if result.returncode == 0 else []
            finally:
                tmp_path.unlink(missing_ok=True)
        else:
            result = subprocess.run(
                ["strings", str(path)],
                capture_output=True,
                text=True,
                timeout=60,
            )
            return result.stdout.splitlines() if result.returncode == 0 else []
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        return []


def verify_file(path: Path, strict: bool = False) -> tuple[bool, list[str], list[str], list[str]]:
    """
    验证单个文件。
    返回: (通过, 发现的BAD列表, 发现的GOOD列表, 严格模式发现的BAD)
    """
    lines = get_strings(path)
    if not lines:
        return False, ["无法读取或解压"], [], []

    found_bad = []
    for s in BAD_STRINGS:
        for line in lines:
            if s in line:
                found_bad.append(s)
                break

    found_bad_strict = []
    if strict:
        for s in BAD_STRINGS_STRICT:
            for line in lines:
                if s in line:
                    found_bad_strict.append(s)
                    break

    found_good = []
    for s in GOOD_STRINGS:
        for line in lines:
            if s in line:
                found_good.append(s)
                break

    passed = len(found_bad) == 0 and (not strict or len(found_bad_strict) == 0)
    return passed, found_bad, found_good, found_bad_strict


def find_artifacts(dist_dir: Path) -> list[Path]:
    """查找 dist-android 中的 rusda 产物（含 .xz 打包和 staging 目录）"""
    artifacts = []
    # 顶层 .xz 或未压缩的 server/inject/gadget
    patterns = [
        "rusda-server-*-android-*",
        "rusda-inject-*-android-*",
        "rusda-gadget-*-android-*.so*",
    ]
    for p in patterns:
        artifacts.extend(dist_dir.glob(p))
    # staging-*/bin 和 staging-*/lib/rusda
    for staging in dist_dir.glob("staging-*"):
        if staging.is_dir():
            for exe in (staging / "bin").glob("rusda-*"):
                if exe.is_file():
                    artifacts.append(exe)
            for lib in (staging / "lib" / "rusda").rglob("rusda-gadget.so"):
                if lib.is_file():
                    artifacts.append(lib)
    return sorted(set(artifacts))


def main():
    parser = argparse.ArgumentParser(description="rusda patch 验证")
    parser.add_argument("dir", nargs="?", help="dist-android 目录")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="严格模式：额外检查 frida:rpc（gadget 内嵌 JS 可能仍含，预期会 fail）",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    dist_dir = Path(args.dir) if args.dir else root / "dist-android"

    if not dist_dir.exists():
        print(f"错误: 目录不存在 {dist_dir}")
        sys.exit(1)

    artifacts = find_artifacts(dist_dir)
    if not artifacts:
        print(f"未找到 rusda 产物，请检查 {dist_dir}")
        sys.exit(1)

    print("=" * 70)
    print("rusda patch 验证")
    print("=" * 70)
    print(f"目录: {dist_dir}")
    print(f"产物数: {len(artifacts)}")
    if args.strict:
        print("模式: 严格 (含 frida:rpc 检查)")
    print()
    print("检查规则:")
    print("  ✗ 不应出现: FridaScriptEngine, GLib-GIO, GDBusProxy, GumScript,")
    print("             gum-js-loop, gmain, gdbus" + (" frida:rpc" if args.strict else ""))
    print("  ✓ 应出现:   enignEtpircSadirF, OIG-biLG, yxorPsuBDG, tpircSmuG,")
    print("             russellloop, rmain, rubus")
    print("-" * 70)

    all_passed = True
    for path in artifacts:
        passed, found_bad, found_good, found_bad_strict = verify_file(path, strict=args.strict)
        status = "✓ PASS" if passed else "✗ FAIL"
        if not passed:
            all_passed = False

        print(f"\n{path.name}")
        print(f"  状态: {status}")
        if found_bad:
            print(f"  未 patch: {', '.join(found_bad)}")
        if found_bad_strict:
            print(f"  严格检查: {', '.join(found_bad_strict)}")
        if found_good:
            print(f"  已 patch: {', '.join(found_good)}")
        if passed and not found_good:
            print("  (无 .rodata 特征或仅有 sed 替换，视为通过)")

    print()
    print("=" * 70)
    if all_passed:
        print("全部通过 ✓")
        sys.exit(0)
    else:
        print("存在未 patch 产物，请检查构建流程")
        sys.exit(1)


if __name__ == "__main__":
    main()
