---
title: "Microsoft: AI agent quét GitHub tìm khóa bị lộ"
date: 2026-11-07
topic: bao-mat
summary: "Ngày 5/11/2026, Microsoft Threat Intelligence cảnh báo nhóm tấn dùng khung AI agent (ARTEX) quét repo GitHub công khai tìm khóa, rồi xâm nhập cloud trong vài phút."
insight: "Doanh nghiệp nhỏ hay dán API key, token OAuth vào repo hoặc file cấu hình để “cho nhanh”. Chỉ xoá dòng đó trên GitHub chưa đủ — phải thu hồi và đổi khóa ngay, vì lịch sử commit và bản sao vẫn còn."
tags: [microsoft, github, bao-mat, ai, api-key]
sources:
  - name: Microsoft Security Blog – Threat actors use agentic AI tooling to find and abuse exposed secrets
    url: https://www.microsoft.com/en-us/security/blog/2026/11/05/threat-actors-use-agentic-ai-tooling-to-find-and-abuse-exposed-secrets/
    date: 2026-11-05
---
## Có gì mới

Ngày 5/11/2026, Microsoft Threat Intelligence công bố quan sát: một số nhóm tấn đang dùng **khung AI agent tấn công** (ví dụ ARTEX) để tìm khóa lộ trên GitHub công khai — mật khẩu ứng dụng, client secret OAuth, khóa API dịch vụ cloud và khóa gọi mô hình AI — rồi dùng luôn để xâm nhập tài nguyên đám mây.

Theo Microsoft, việc tìm credential trên repo công khai không mới, nhưng trước đây bị giới hạn bởi thời gian con người phải tìm repo, đọc mã và thử khóa. Công cụ agent giúp quét nhiều repo nhanh hơn, phân tích kết quả và tự chạy bước tiếp theo, giảm thao tác “tay trên bàn phím”. Trong ít nhất một vụ, Microsoft ghi nhận agent đi từ quét GitHub đến lấy dữ liệu khỏi Azure Key Vault **trong khoảng năm phút**.

Microsoft cũng theo dõi hoạt động lạm dụng credential ứng dụng hợp lệ từ khoảng 28/10/2026: đăng nhập service principal thành công từ một số địa chỉ IP, kể cả trường hợp credential ứng dụng đa tenant bị lộ ở phía nhà cung cấp rồi được dùng để vào nhiều tenant phía khách. Sau khi vào được, bên tấn công thăm dò tài nguyên, lấy thêm khóa (storage, App Service, chuỗi kết nối, kho AI), và trong một số tenant còn truy cập SharePoint/OneDrive hoặc gửi yêu cầu Microsoft Graph để tìm nội dung.

## Vì sao doanh nghiệp nhỏ cần chú ý

Nhiều shop, studio hay đội nhỏ vẫn đưa khóa vào file `.env` rồi commit nhầm, hoặc nhúng token trong script demo rồi đẩy repo public. Khi repo đã công khai, máy quét (kể cả agent) có thể thấy khóa gần như ngay. Xóa dòng trên bản mới **không** thu hồi khóa: lịch sử git, fork, mirror và bản cache vẫn có thể giữ bản sao.

Hậu quả không chỉ là “bị đọc mã”. Credential ứng dụng thường có quyền chương trình hóa tới cloud, kho bí mật, storage hoặc dịch vụ AI — đúng kiểu tài nguyên Microsoft thấy bị lạm dụng sau khi khóa lộ. Nếu doanh nghiệp đang dùng API AI trả phí theo lượt gọi, khóa bị lấy có thể đẩy chi phí bất thường trước khi phát hiện.

## Việc nên làm ngay

1. Rà repo GitHub (và bản fork/mirror nếu có): bật secret scanning / push protection khi nền tảng hỗ trợ; quét lại lịch sử commit, không chỉ nhánh hiện tại.
2. Mọi khóa từng lộ trên mạng công cộng: **coi như đã bị chiếm** — thu hồi hoặc xoay vòng ngay, rồi kiểm tra nhật ký đăng nhập ứng dụng / service principal xem có truy cập lạ không.
3. Không lưu client secret dài hạn trong mã nguồn. Ưu tiên biến môi trường trên máy chủ, kho bí mật có kiểm soát truy cập, hoặc cơ chế xác thực không cần secret cố định (managed identity / workload identity) khi nhà cung cấp hỗ trợ.
4. Áp quyền tối thiểu cho từng ứng dụng: chỉ đúng tài nguyên cần dùng; tách khóa theo môi trường (dev/prod) và theo dịch vụ để một khóa lộ không mở hết hệ thống.
5. Theo dõi tín hiệu bất thường: một IP đăng nhập nhiều service principal trong thời gian ngắn, lỗi secret sai/hết hạn xen kẽ thành công, hoặc đột biến chi phí API AI / cloud.

Tin này không yêu cầu doanh nghiệp nhỏ “mua thêm công cụ AI bảo mật” ngay. Việc thực tế nhất là dừng để khóa trong repo công khai, xoay vòng khóa đã lộ, và giữ thói quen kiểm tra quyền ứng dụng — vì tốc độ quét và khai thác bằng agent đang rút ngắn cửa sổ phản ứng từ ngày xuống phút.
