# Kịch bản video HW05 (8–10 phút, tiếng Việt)

> **HUMAN REVIEW / MANUAL ONLY:** Bạn phải tự quay màn hình và tự thuyết minh bằng giọng thật. Không dùng giọng AI. Đặt video YouTube ở chế độ **Unlisted**, sau đó thay mọi `[VIDEO_URL]` trong repo.

## Chuẩn bị trước khi quay

1. Mở repo bằng VS Code: `E:\HCMUS\Sem9\Software Testing\HW05\HW05-software-testing`.
2. Mở **Task Manager → Details**, tìm `node.exe`, bật cột PID, CPU, Memory. Thu nhỏ Task Manager chiếm nửa trái màn hình.
3. Mở **VS Code Terminal → PowerShell** ở nửa phải. Dòng nhắc phải đang ở thư mục repo.
4. Đóng các ứng dụng nặng, tắt thông báo, không để token/JWT hay thông tin cá nhân xuất hiện.
5. Mở sẵn các file: ba JMX, `analysis/*.md`, `evidence/hardware/hardware-report.md`, ba HTML report và `skills/eshop-performance-testing/SKILL.md`.
6. Các lệnh `video-*` dưới đây tạo artifact demo riêng trong `results/smoke`; chúng không ghi đè bốn kết quả chính.

## 0:00–0:45 — Danh tính, phạm vi và cấu hình

**Hình:** VS Code mở `README.md`, sau đó `evidence/hardware/hardware-report.md` và ảnh dxdiag do bạn tự chụp.

**Lời nói gợi ý:**

> Em là [HỌ TÊN], MSSV 23127373. Bài HW05 dùng Apache JMeter 5.6.3 non-GUI kiểm thử EShop chạy localhost. Workflow không trùng nhóm của em là đăng ký tài khoản, đọc danh sách admin để xác minh đúng user vừa tạo, rồi xóa đúng ID đó. Ba scenario Load, Stress, Spike đều dùng cùng workflow. Máy đo là ASUS ROG Zephyrus G14, Ryzen 7 5800HS 8 nhân 16 luồng, RAM 23,41 GB, Windows 11 Pro, Java 17.

**HUMAN REVIEW:** Sửa họ tên/MSSV và chỉ nói thông số sau khi đối chiếu dxdiag GUI.

## 0:45–1:40 — Test-plan design và human review

**Hình:** Mở một JMX trong JMeter GUI để thấy cây test; lần lượt trỏ vào CSV Data Set Config, JSR223 PreProcessor, POST register, JSON Extractor, GET assertion, DELETE, và listener. Không bấm chạy full test trong GUI.

**Lời nói:**

> CSV chỉ cung cấp name, password và domain. Mỗi vòng lặp tạo email UUID để tránh đụng dữ liệu. POST register trả ID, JSON Extractor lưu vào `registered_id`. GET không chỉ kiểm tra HTTP 200 mà parse JSON, bắt buộc ID và email nằm trên cùng một object. Thread Group để Continue nên dù assertion GET lỗi, DELETE vẫn được thử khi ID tồn tại. Load dùng Summary Report, Stress dùng Aggregate Report, Spike dùng View Results Tree; execution chính vẫn là non-GUI với raw JTL và HTML report.

> Gemini ban đầu đoán SQLITE_BUSY là bottleneck, đề xuất 50.000 email và thay file SQLite đang mở. Em bác bỏ sau khi đọc source: SUT dùng một connection, không enforce unique email, và reset DB khi backend restart. Em cũng thay substring assertion bằng JsonSlurper exact match.

## 1:40–2:30 — Demo non-GUI + resource cùng frame

**Hình:** Task Manager nửa trái, VS Code PowerShell nửa phải. Trong **VS Code Terminal (PowerShell)** gõ:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\run-scenario.ps1 -Scenario Load -Smoke -ArtifactSuffix video-load -JMeterProperty "load_threads=5;load_ramp=5;load_duration=25;load_think_base=50;load_think_range=50"
```

Trong lúc chạy, click `node.exe` trong Task Manager để CPU/Memory/PID nhìn rõ và giữ cả hai cửa sổ trong cùng frame.

**Lời nói:**

> Wrapper tự kiểm tra port 3000, khởi động backend sạch, lấy admin JWT ngoài vùng đo, khởi động monitor, rồi gọi JMeter `-n`. Monitor phải tạo CSV trong 5 giây; nếu không, run bị fail thay vì thiếu bằng chứng. Đây là demo ngắn. Bốn run chính đã chạy lần lượt để tránh cạnh tranh tài nguyên và được giữ đầy đủ trong `results` và `reports/html`.

## 2:30–3:25 — Load chính thức

**Hình:** Mở `reports/html/23127373_Load_20260814/index.html`, `analysis/load.md`, `analysis/load-resources.md`; vẫn để Task Manager hoặc ảnh same-frame bạn chụp ở một góc.

**Lời nói:**

> Load dùng 15 users, ramp 30 giây, giữ 300 giây. Kết quả hợp lệ có 19.311 endpoint samples, 0 lỗi, p95 8 ms và throughput 64,58 samples mỗi giây. Ba label có đúng 6.437 samples, nghĩa là mỗi register đều được read và cleanup. Resource monitor có 301 quan sát phủ 303,8 giây. Con số p95 dưới ngưỡng giả định 500 ms; đây là kết quả localhost, không phải SLA production.

## 3:25–4:25 — Stress staircase

**Hình:** `evidence/charts/stress-capacity.svg`, `analysis/stress.md`, Stress HTML dashboard.

**Lời nói:**

> Stress tạo bốn Thread Group chồng nhau, lần lượt 10, 20, 30 và 40 users, mỗi nấc 120 giây. Toàn bài có 139.140 samples, 0 lỗi, p95 95 ms. Khi tăng 20 lên 30 users, throughput tăng 312,35 lên 324,06 samples mỗi giây. Tăng tiếp lên 40 chỉ đạt 326,86, tức khoảng 0,9 phần trăm, nhưng p95 tăng từ 74 lên 109 ms, khoảng 47 phần trăm. Vì vậy em gọi khoảng 30 users là capacity knee hoặc saturation onset, không gọi là crash vì không có HTTP error. CPU Node p95 là 3,568 phần trăm toàn máy 16 logical processors.

## 4:25–5:15 — Spike và recovery

**Hình:** `evidence/charts/spike-recovery.svg`, Spike HTML dashboard.

**Lời nói:**

> Spike giữ baseline 10 users trong 420 giây và thêm 40 users đúng phút 2 đến phút 3. Baseline p95 là 10 ms; trong burst p95 lên 120 ms, throughput 324,06 samples mỗi giây, 0 lỗi. Ngay cửa sổ 60 giây sau burst, p95 trở lại 10 ms và throughput 137,09, gần baseline 139,22. Vì vậy recovery time quan sát được nhỏ hơn 60 giây.

## 5:15–6:10 — Soak và endurance threshold

**Hình:** `evidence/charts/soak-memory.svg`, `analysis/soak.md`, `analysis/soak-resources.md`.

**Lời nói:**

> Soak chạy đủ 15 phút ở 10 users, ramp 60 giây: 39.502 samples, 0 lỗi, p95 6 ms, throughput 43,94 samples mỗi giây. Working set tăng từ khoảng 66 lên 127 MB trong warm-up rồi plateau. Hồi quy tuyến tính năm phút cuối là cộng 0,03 MB mỗi phút cho working set và âm 0,025 MB mỗi phút cho private memory; handles từ 231 về 230. Dữ liệu không ủng hộ leak tuyến tính trong 15 phút, nhưng không chứng minh leak không thể xảy ra lâu hơn. Endurance threshold đã kiểm chứng trên máy này là 10 users, khoảng 43,94 endpoint samples mỗi giây, p95 6 ms, memory ceiling quan sát 128,10 MB.

## 6:10–7:05 — AI analysis + misinterpretation hunt

**Hình:** Cuộc chat Gemini Pro có prompt, file JTL đính kèm và follow-up; sau đó `AI-Audit-Report.md`.

**Lời nói:**

> Em tải raw JTL vào Gemini, yêu cầu tính samples, error, p95, capacity knee, recovery và optimization. Em không nhận output trực tiếp. Em đối chiếu bằng analyzer nearest-rank. [ĐỌC 1–2 SAI LỆCH THẬT TỪ PHẦN G-03/G-04 SAU KHI HOÀN TẤT UPLOAD]. Mỗi prompt có tên công cụ, timestamp, prompt, output và quyết định human review trong AI Audit. Khuyến nghị nào không gắn được với source hoặc measurement được đánh dấu hallucinated hoặc cần benchmark lại.

> **HUMAN REVIEW REQUIRED:** Không quay đoạn này cho tới khi G-03/G-04 trong AI Audit đã có output thật; tuyệt đối không đọc placeholder.

## 7:05–7:45 — Bug thật và Agent Skill

**Hình:** `evidence/issues/duplicate-email/reproduction.html`, GitHub Issue đã tạo, rồi `skills/eshop-performance-testing/SKILL.md`.

Trong **VS Code Terminal (PowerShell)** gõ:

```powershell
py skills\eshop-performance-testing\scripts\summarize_jtl.py results\23127373_Load_20260814.jtl
```

**Lời nói:**

> FR-01 yêu cầu email unique nhưng hai request body giống hệt đều trả HTTP 200 và tạo ID 3, ID 4. Đây là functional regression được tái hiện bằng localhost call và đưa lên GitHub Issue cùng screenshot. Agent Skill đóng gói quy trình validate JMX, chạy non-GUI, summarize raw JTL và kiểm tra evidence để tái dùng cho endpoint khác.

## 7:45–8:30 — Continuous model và kết luận

**Hình:** Mermaid flowchart trong `docs/continuous-performance-testing.md`.

**Lời nói:**

> Pipeline chỉ chạy Load khi API, database, auth, dependency hoặc test plan thay đổi; Stress/Spike chạy cho thay đổi rủi ro cao hoặc nightly, Soak chạy weekly. Gate kết hợp absolute SLO và regression hơn 20 phần trăm so với median năm baseline cùng hardware. Một regression được chạy lại một lần để giảm false alarm. Trade-off là chi phí runner, noise của shared hardware và nguy cơ baseline drift, nên baseline update phải review và raw artifacts phải được lưu.

> Kết luận: workflow đạt các SLO khởi đầu trên máy local, saturation bắt đầu khoảng 30 users, spike phục hồi dưới 60 giây, và soak 10 users ổn định 15 phút. Giới hạn chính của bằng chứng là môi trường co-located và thời lượng soak ngắn hơn production.

## Sau khi quay

- [ ] Video dài ít nhất 6:00, 1080p, nghe rõ tiếng Việt của chính bạn.
- [ ] Có tool + Task Manager/Resource Monitor trong cùng frame khi demo execution.
- [ ] Không lộ JWT, email cá nhân, mật khẩu, thông báo riêng tư.
- [ ] Có các số liệu Load/Stress/Spike/Soak đúng như raw JTL.
- [ ] Có Gemini prompt + follow-up thật, bug Issue và Agent Skill demo.
- [ ] Upload YouTube **Unlisted**, kiểm tra bằng cửa sổ ẩn danh, thay `[VIDEO_URL]` trong `README.md` và `Main-Report.md`.
