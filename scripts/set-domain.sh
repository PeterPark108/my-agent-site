#!/usr/bin/env bash
# Dùng: scripts/set-domain.sh myagent.vn   (không có https://, không có dấu /)
# Cập nhật canonical / og / sitemap / robots / JSON-LD + js/config.js và tạo file CNAME.
set -euo pipefail
cd "$(dirname "$0")/.."
D="${1:?Thiếu tên miền, vd: scripts/set-domain.sh myagent.vn}"; D="${D#http*://}"; D="${D%/}"
OLD=$(grep -o "siteUrl: *'[^']*'" js/config.js | cut -d"'" -f2)
NEW="https://$D/"
[ "$OLD" = "$NEW" ] && { echo "Đã là $NEW"; exit 0; }
grep -rlF --include='*.html' --include='*.xml' --include='*.txt' --include='config.js' "$OLD" . | grep -v '^./.git/' | xargs sed -i "s#${OLD}#${NEW}#g"
echo "$D" > CNAME
echo "Đổi $OLD -> $NEW xong. Commit + push, rồi đặt Custom domain trong Settings > Pages."
