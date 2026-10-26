#!/usr/bin/env bash
# Dùng SAU KHI đã merge PR dev→production: bash scripts/release.sh v0.1.1 "ghi chú"
set -euo pipefail
V="${1:?Cần số phiên bản, vd v0.1.1}"; NOTE="${2:?Cần ghi chú}"
[[ "$V" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "Sai dạng vMAJOR.MINOR.PATCH"; exit 1; }
git fetch origin production --tags
git tag -a "$V" origin/production -m "$NOTE"
git push origin "$V"
gh release create "$V" --verify-tag --title "$V" --notes "$NOTE"
echo "Đã tạo $V tại $(git rev-parse --short origin/production)"
