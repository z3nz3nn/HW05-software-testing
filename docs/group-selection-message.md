# Group selection message

Send the following message to the group after confirming the workflow is not already taken:

```text
HW05

Mình xin nhận workflow E2E gồm 3 endpoint group sau (không trùng các endpoint mọi người đã chọn):

1. Auth-heavy    — POST   /api/register                    (đăng ký tài khoản)
2. Read-heavy    — GET    /api/admin/users                 (đọc danh sách và xác minh đúng user vừa tạo)
3. Transactional — DELETE /api/admin/users/:id             (xóa đúng user vừa tạo/cleanup)

Cả ba kịch bản Load, Stress và Spike sẽ chạy cùng workflow:
POST /api/register → GET /api/admin/users → DELETE /api/admin/users/:id.

Công cụ: JMeter 5.6.3 (non-GUI), CSV data-driven, raw JTL + HTML report.
```

> **HUMAN REVIEW REQUIRED:** The user must send this message and receive group confirmation; an AI cannot verify private group-chat selections.
