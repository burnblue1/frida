#!/bin/bash
# 串行编译 Android 全架构 (x86, x86_64, arm, arm64)，包含 server、gadget、inject
# 输出命名格式: rusda-server-{version}-android-{arch}.xz
# 用法: ./tools/build-android-all.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="${SRC_ROOT}/dist-android"
VERSION="17.6.2"

# 检查 NDK
if [ -z "$ANDROID_NDK_ROOT" ]; then
    echo "错误: 请设置 ANDROID_NDK_ROOT 环境变量"
    echo "  export ANDROID_NDK_ROOT=/path/to/ndk-r25"
    exit 1
fi

cd "$SRC_ROOT"

# 清理旧的输出
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# 单架构：configure + make + install
build_arch() {
    local arch=$1
    local build_dir="${SRC_ROOT}/build-android-${arch}"
    local prefix="${OUTPUT_DIR}/staging-${arch}"

    echo "[$arch] 开始配置..."
    rm -rf "$build_dir"
    mkdir -p "$build_dir"
    cd "$build_dir"

    ../configure \
        --prefix="$prefix" \
        --host="android-${arch}" \
        --enable-server \
        --enable-gadget \
        --enable-inject

    echo "[$arch] 开始编译..."
    make -j$(nproc)
    make install

    cd "$SRC_ROOT"
    echo "[$arch] 完成"
}

# 串行编译：避免多个 configure 同时解压/写入 deps 导致 SDK 不完整
echo "=== 串行编译 Android 全架构 ==="
for arch in x86 x86_64 arm arm64; do
    build_arch "$arch" || exit 1
done

echo ""
echo "=== 打包 (命名格式: rusda-*-{version}-android-{arch}.xz) ==="

# 按官方格式打包：单文件 xz 压缩，非 tar
for arch in x86 x86_64 arm arm64; do
    staging="${OUTPUT_DIR}/staging-${arch}"

    # rusda-server: rusda-server-17.6.2-android-arm.xz
    if [ -f "$staging/bin/rusda-server" ]; then
        echo "  rusda-server-${VERSION}-android-${arch}.xz"
        xz -c -T0 "$staging/bin/rusda-server" > "${OUTPUT_DIR}/rusda-server-${VERSION}-android-${arch}.xz"
    fi

    # rusda-inject: rusda-inject-17.6.2-android-arm.xz
    if [ -f "$staging/bin/rusda-inject" ]; then
        echo "  rusda-inject-${VERSION}-android-${arch}.xz"
        xz -c -T0 "$staging/bin/rusda-inject" > "${OUTPUT_DIR}/rusda-inject-${VERSION}-android-${arch}.xz"
    fi

    # rusda-gadget: rusda-gadget-17.6.2-android-arm.so.xz
    gadget_32="$staging/lib/rusda/32/rusda-gadget.so"
    gadget_64="$staging/lib/rusda/64/rusda-gadget.so"
    if [ -f "$gadget_32" ]; then
        echo "  rusda-gadget-${VERSION}-android-${arch}.so.xz"
        xz -c -T0 "$gadget_32" > "${OUTPUT_DIR}/rusda-gadget-${VERSION}-android-${arch}.so.xz"
    elif [ -f "$gadget_64" ]; then
        echo "  rusda-gadget-${VERSION}-android-${arch}.so.xz"
        xz -c -T0 "$gadget_64" > "${OUTPUT_DIR}/rusda-gadget-${VERSION}-android-${arch}.so.xz"
    fi
done

# 清理 staging
rm -rf "${OUTPUT_DIR}"/staging-*

echo ""
echo "=== 完成 ==="
echo "输出目录: $OUTPUT_DIR"
ls -lh "$OUTPUT_DIR"/*.xz 2>/dev/null || true
