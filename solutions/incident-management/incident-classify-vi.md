# Ma Trận Phân Loại Sự Cố

> Ma trận phân loại sự cố toàn diện theo mức độ ưu tiên và danh mục.
> Định nghĩa các mức ưu tiên, chỉ tiêu SLA, quy trình leo thang và tiêu chí sự cố nghiêm trọng.
>
> **Cách sử dụng**: L1 sử dụng cây quyết định trong [classification.md](classification.md) để xác định mức ưu tiên, sau đó tham khảo ma trận này để biết chỉ tiêu phản hồi, quy trình leo thang và yêu cầu xử lý.
>
> Tài liệu liên quan: [`classification.md`](classification.md) -- [`incident-knowledge-base.md`](incident-knowledge-base.md) -- [`swimlane-flow.md`](swimlane-flow.md) -- [`scenarios.md`](scenarios.md)

---

## Tóm Tắt Tổng Quan

Tài liệu này cung cấp ma trận tham chiếu vận hành cho việc phân loại sự cố tại TCLife. Ma trận ánh xạ mọi tổ hợp của **Mức ưu tiên (P1--P4)** và **Danh mục (HW, SW, SEC, CLD, DB, ACC, OTH)** với các chỉ báo cụ thể, ngưỡng thời gian ngừng hoạt động, chỉ tiêu SLA, quy trình leo thang và các hành động phản hồi ban đầu.

Ma trận được thiết kế cho nền tảng bảo hiểm nhân thọ vận hành trên AWS, phục vụ ba nhóm người dùng: chủ hợp đồng bảo hiểm (kênh số 24/7), sales/môi giới (hệ thống báo giá và đề xuất), và nhân viên nội bộ (thẩm định, bồi thường, tính toán actuarial, back-office). Các quyết định phân loại phản ánh tính chất quản lý chặt chẽ của ngành bảo hiểm nhân thọ, nơi tính chính xác và khả dụng của dữ liệu mang hệ quả tài chính và pháp lý.

---

## 1. Định Nghĩa

### 1.1 Các Mức Ưu Tiên

| Mức ưu tiên | Tên | Định nghĩa |
|----------|------|-----------|
| **P1** | Nghiêm trọng | Toàn bộ hệ thống Tier 1 hoặc Tier 2 ngừng hoạt động, vi phạm dữ liệu đã xác nhận hoặc nghi ngờ, sai lệch dữ liệu tài chính ảnh hưởng khách hàng, hoặc bất kỳ sự kiện nào ngăn cản hoạt động kinh doanh cốt lõi (phát hành hợp đồng, chi trả quyền lợi bảo hiểm, thu phí bảo hiểm). Doanh nghiệp không thể hoạt động bình thường. |
| **P2** | Cao | Suy giảm đáng kể hệ thống Tier 1 hoặc Tier 2, chức năng kinh doanh chính không khả dụng nhưng có giải pháp tạm thời, hoặc sự kiện an ninh đã được kiểm soát. Nhiều nhóm người dùng bị ảnh hưởng và năng suất kinh doanh giảm đáng kể. |
| **P3** | Trung bình | Ảnh hưởng một phần đến chức năng không quan trọng hoặc nhóm người dùng hạn chế. Có giải pháp tạm thời và hoạt động kinh doanh tiếp tục với bất tiện nhỏ. Vấn đề đơn lẻ với phạm vi ảnh hưởng đã xác nhận là nhỏ. |
| **P4** | Thấp | Lỗi giao diện, bất tiện nhỏ, lỗi tài liệu, hoặc vấn đề không có tác động kinh doanh đo lường được. Hoạt động bình thường không bị ảnh hưởng. |

### 1.2 Danh Mục Sự Cố

| Mã | Danh mục | Phạm vi | Ví dụ |
|------|----------|-------|---------|
| **HW** | Phần cứng | Lỗi máy chủ vật lý hoặc ảo, lưu trữ, thiết bị ngoại vi | EC2 host suy giảm, EBS volume lỗi, máy in/máy quét tại chi nhánh lỗi, lỗi phần cứng máy trạm |
| **SW** | Phần mềm (Ứng dụng) | Ứng dụng crash, lỗi logic, lỗi tính toán, lỗi giao diện, lỗi quy trình | Tính sai phí bảo hiểm, lỗi duyệt bồi thường tự động, ứng dụng OOM, ngoại lệ không xử lý, batch cho kết quả sai |
| **SEC** | An ninh bảo mật | Sự kiện liên quan đến tính bảo mật, toàn vẹn hoặc khả dụng có yếu tố an ninh | Vi phạm dữ liệu, lộ thông tin đăng nhập, ransomware, DDoS, truy cập trái phép, khai thác phishing, bypass WAF |
| **CLD** | Hạ tầng đám mây | Dịch vụ quản lý AWS, mạng, DNS, cân bằng tải, serverless | AWS regional suy giảm, mất kết nối VPC, Route 53 lỗi, ALB cấu hình sai, Lambda throttling, S3 lỗi truy cập |
| **DB** | Cơ sở dữ liệu | Lỗi database engine, replication, sai lệch dữ liệu, cạn kiệt connection pool, lỗi backup | RDS crash, DynamoDB throttling, replication lag, cạn kiệt connection pool, backup job lỗi, hết dung lượng |
| **ACC** | Truy cập / Định danh | Xác thực, phân quyền, IAM, SSO, MFA, chứng chỉ số | SSO ngừng hoạt động, khóa tài khoản hàng loạt, IAM policy cấu hình sai, SSL certificate hết hạn, MFA service lỗi |
| **OTH** | Khác | Tích hợp bên thứ ba, công việc định kỳ, phụ thuộc bên ngoài, chưa phân loại | Cổng thanh toán lỗi, timeout API tái bảo hiểm, lỗi batch scheduler, lỗi ETL pipeline, hệ thống vendor ngừng hoạt động |

### 1.3 Phân Tầng Hệ Thống

| Tầng | Phân loại | Hệ thống | Mục tiêu khả dụng | Nhóm người dùng |
|------|---------------|---------|-------------------|------------|
| **Tier 1** | Hướng khách hàng | Cổng khách hàng, ứng dụng di động, thanh toán trực tuyến, tự phục vụ, onboarding số | 99.9% (24/7) | Chủ hợp đồng / Khách hàng |
| **Tier 1** | Hướng Sales | Sales portal, công cụ báo giá, nộp đề xuất, dashboard hoa hồng, e-application | 99.5% (giờ mở rộng: 7h--22h) | Sales / Môi giới |
| **Tier 1** | Bảo Hiểm Cốt Lõi | Hệ thống quản trị hợp đồng (PAS), xử lý bồi thường, billing engine | 99.5% (giờ mở rộng + giám sát/trực 24/7) | Tất cả (nền tảng) |
| **Tier 2** | Nội Bộ - Hỗ Trợ Kinh Doanh | Workbench thẩm định, hệ thống actuarial, báo cáo tuân thủ | 99.5% (giờ hành chính: 8h--18h T2--T7) | Nhân viên nội bộ |
| **Tier 3** | Back-Office / Batch | Xử lý batch đêm, tạo báo cáo pháp quy, ETL data warehouse, batch tính hoa hồng, phân bổ phí bảo hiểm, lưu trữ tài liệu | Hoàn thành batch trước 6:00 sáng hàng ngày | Nội bộ / Pháp quy |

---

## 2. Quy Tắc Tự Động Nâng Mức Ưu Tiên

Một số danh mục mang rủi ro vốn có có thể tự động nâng mức ưu tiên bất kể đánh giá ban đầu.

| Điều kiện | Mức ưu tiên tối thiểu | Lý do |
|-----------|-----------------|-----------|
| **SEC** -- Vi phạm dữ liệu đã xác nhận liên quan PII (chủ hợp đồng, người thụ hưởng, người được bảo hiểm) | P1 | Nghĩa vụ báo cáo pháp quy, rủi ro uy tín, trách nhiệm pháp lý tiềm ẩn |
| **SEC** -- Lộ thông tin đăng nhập hệ thống production đã xác nhận | P1 | Mối đe dọa trực tiếp đến tính toàn vẹn và khả dụng dữ liệu |
| **SEC** -- Tấn công DDoS đang làm suy giảm dịch vụ | P1 | Ảnh hưởng khả dụng các hệ thống hướng khách hàng |
| **DB** -- Nghi ngờ sai lệch dữ liệu trong bảng tài chính (phí bảo hiểm, bồi thường, giá trị hợp đồng) | P1 | Tính toàn vẹn dữ liệu tài chính là điều kiện kích hoạt P1 theo chính sách phân loại |
| **DB** -- Database chính không phản hồi / failover đã kích hoạt | P1 | Các hệ thống cốt lõi phụ thuộc vào khả dụng database |
| **SW** -- Lỗi tính toán ảnh hưởng giá trị tài chính của chủ hợp đồng (giá trị hoàn lại, phí bảo hiểm, số tiền bồi thường) | P1 | Tính chính xác dữ liệu tài chính -- hệ quả pháp quy và niềm tin khách hàng |
| **ACC** -- Lỗi xác thực hàng loạt (>10% người dùng không thể đăng nhập) | P1 | Tương đương ngừng hoạt động toàn bộ đối với người dùng bị ảnh hưởng |
| **CLD** -- Suy giảm dịch vụ AWS theo vùng ảnh hưởng nhiều hệ thống cốt lõi | P1 | Ảnh hưởng đa hệ thống cần đánh giá kích hoạt DR |
| **OTH** -- Cổng thanh toán lỗi (tất cả kênh thanh toán ngừng hoạt động) | P1 | Dừng thu phí bảo hiểm |
| **Mọi danh mục** -- Hệ thống báo cáo pháp quy không khả dụng trong 48 giờ trước hạn nộp | P2 tối thiểu | Rủi ro tuân thủ pháp quy |
| **Mọi danh mục** -- Lỗi xử lý batch phân bổ phí bảo hiểm, tính hoa hồng, hoặc feed pháp quy | P2 tối thiểu | Tác động tài chính và pháp quy xuôi dòng |

---

## 3. Ma Trận Phân Loại

### 3.1 P1 -- Nghiêm Trọng

**Chỉ báo chung**: Dịch vụ hoàn toàn không khả dụng cho hệ thống Tier 1 hoặc Tier 2. Tất cả hoặc hầu hết người dùng của hệ thống bị ảnh hưởng không thể thực hiện chức năng chính. Dữ liệu tài chính đang hoặc có thể không chính xác. Vi phạm an ninh đã xác nhận. Nghĩa vụ pháp quy được kích hoạt.

**Ngưỡng thời gian ngừng**: Không chấp nhận thời gian ngừng ngoài kế hoạch cho hệ thống Tier 1. Tối đa 2 giờ để kiểm soát và khôi phục dịch vụ (dù ở mức suy giảm). Giải quyết hoàn toàn trong 24 giờ.

**Sự cố nghiêm trọng**: CÓ -- tất cả sự cố P1 được tuyên bố là Sự Cố Nghiêm Trọng (Major Incident).

**MTTA (Thời gian trung bình để xác nhận)**: 15 phút (24/7 cho Tier 1; giờ hành chính cho Tier 2 trừ khi có trực ngoài giờ).

**MTTR mục tiêu (Kiểm soát)**: 2 giờ. **MTTR mục tiêu (Giải quyết hoàn toàn)**: 24 giờ.

| Danh mục | Mô tả tác động | Mức khẩn cấp | Tầng hệ thống | Leo thang | Phản hồi ban đầu |
|----------|-------------------|---------|--------------|------------|---------------------------|
| **HW** | Lỗi máy chủ gây ngừng hoạt động toàn bộ nền tảng bảo hiểm. Sales không thể báo giá, khách hàng không thể truy cập cổng thông tin, hoặc xử lý bồi thường bị dừng. | Ngay lập tức. Mỗi phút ngừng hoạt động là mất doanh thu và niềm tin khách hàng. | Tier 1 (cổng thông tin/hệ thống sales) hoặc Tier 2 (PAS, bồi thường) tùy thuộc hệ thống nào chạy trên host bị ảnh hưởng. | 0 phút: Kỹ sư trực tự động nhận cảnh báo. 15 phút: CTO/Trưởng phòng CNTT được thông báo. 30 phút: IC kích hoạt, phòng chỉ huy mở. 1 giờ: CEO được báo cáo nếu ảnh hưởng khách hàng. | 1. Xác nhận phạm vi (hệ thống nào bị ảnh hưởng). 2. Chuyển đổi sang instance dự phòng/AZ. 3. IC điều phối phản hồi. 4. Cập nhật trạng thái mỗi 30 phút. 5. Đánh giá sau sự cố bắt buộc. |
| **SW** | Lỗi ứng dụng gây tính toán tài chính sai (phí bảo hiểm, bồi thường, giá trị hoàn lại) trên nhiều hợp đồng, HOẶC ứng dụng crash hoàn toàn ngăn cản chức năng kinh doanh cốt lõi. Phát hiện sai lệch dữ liệu âm thầm ảnh hưởng hồ sơ chủ hợp đồng. | Ngay lập tức. Lỗi dữ liệu tài chính tích lũy theo thời gian -- mỗi giờ chậm trễ tăng chi phí khắc phục. | Tier 1 (PAS, billing, claims engine là bảo hiểm cốt lõi) với tác động xuôi dòng Tier 1 (khách hàng thấy giá trị sai trên cổng). Tier 3 nếu kết quả batch bị sai. | 0 phút: Dev trực nhận cảnh báo. 15 phút: CTO được thông báo. 30 phút: IC kích hoạt. Nếu dữ liệu tài chính bị ảnh hưởng: Trưởng phòng Tài chính và Actuarial được thông báo trong 1 giờ. | 1. DỪNG ghi/xử lý dữ liệu nếu nghi ngờ sai lệch. 2. Xác định phạm vi ảnh hưởng (bao nhiêu hợp đồng/khách hàng). 3. Nếu liên quan triển khai: rollback ngay. 4. Nếu sai lệch dữ liệu: cô lập bản ghi bị ảnh hưởng, giữ lại output xuôi dòng. 5. Thông báo Tài chính. 6. Giữ lại báo cáo pháp quy sử dụng dữ liệu bị ảnh hưởng. |
| **SEC** | Vi phạm dữ liệu đã xác nhận làm lộ PII của chủ hợp đồng (tên, CMND/CCCD, dữ liệu sức khỏe, hồ sơ tài chính). Phát hiện ransomware. Lộ thông tin đăng nhập database production hoặc tài khoản admin. Đang bị khai thác tích cực. | Ngay lập tức. Đồng hồ pháp quy bắt đầu tính. Kẻ tấn công có thể vẫn đang hoạt động -- kiểm soát cần nhanh chóng. | Tất cả tầng có thể bị ảnh hưởng. Hệ thống Tier 1 có thể cần ngắt để kiểm soát. | 0 phút: Trưởng an ninh nhận cảnh báo. 15 phút: CTO + Pháp lý được thông báo. 30 phút: CEO được báo cáo. 1 giờ: Đánh giá nghĩa vụ thông báo pháp quy (cơ quan bảo vệ dữ liệu, cơ quan quản lý bảo hiểm). Kích hoạt đội phản hồi sự cố bên ngoài nếu cần. | 1. Cô lập hệ thống bị xâm nhập (phân đoạn mạng). 2. Bảo toàn bằng chứng pháp y (KHÔNG khởi động lại hoặc xóa). 3. Thu hồi thông tin đăng nhập bị lộ. 4. Kích hoạt playbook sự cố an ninh. 5. Đánh giá nghĩa vụ báo cáo pháp quy. 6. Liên hệ cố vấn pháp lý. 7. KHÔNG thông báo ra bên ngoài cho đến khi pháp lý tư vấn. |
| **CLD** | AWS regional outage hoặc lỗi multi-AZ ảnh hưởng nền tảng bảo hiểm cốt lõi. Nhiều hệ thống ngừng đồng thời. Có thể cần kích hoạt DR. | Ngay lập tức. Hạ tầng đám mây là nền tảng -- không gì hoạt động cho đến khi giải quyết. | Tất cả tầng. Hệ thống Tier 1 và Tier 2 chia sẻ hạ tầng đám mây. | 0 phút: Infra trực nhận cảnh báo. 15 phút: CTO được thông báo. 30 phút: IC kích hoạt. 1 giờ: Đánh giá kích hoạt DR (chuyển đổi sang vùng phụ nếu vượt RTO). Mở case AWS Enterprise Support (Severity 1). | 1. Kiểm tra AWS Health Dashboard. 2. Xác minh phạm vi (AZ/dịch vụ nào bị ảnh hưởng). 3. Kích hoạt multi-AZ failover nếu có. 4. Nếu regional: khởi động kế hoạch DR (pilot light/warm standby). 5. Mở case hỗ trợ AWS (Critical). 6. Theo dõi AWS status để biết ETA. 7. Bật chế độ bảo trì trên ứng dụng hướng khách hàng. |
| **DB** | Database production chính không thể truy cập hoặc xác nhận sai lệch dữ liệu trong bảng tài chính. RDS failover thất bại. Connection pool cạn kiệt trên tất cả instance ứng dụng. | Ngay lập tức. Database là phụ thuộc quan trọng nhất -- tất cả logic kinh doanh cần nó. | Tier 1 (PAS, bồi thường, billing đều phụ thuộc DB) với tác động lan truyền toàn bộ hệ thống Tier 1. | 0 phút: DBA trực nhận cảnh báo. 15 phút: CTO được thông báo. 30 phút: IC kích hoạt. Nếu sai lệch dữ liệu: Actuarial và Tài chính được thông báo. | 1. Thử RDS failover sang standby. 2. Nếu failover thất bại: đánh giá phương án point-in-time recovery. 3. Nếu sai lệch: DỪNG tất cả ghi dữ liệu ngay lập tức. 4. Xác định trạng thái tốt cuối cùng (backup/snapshot). 5. Xác định khoảng mất dữ liệu. 6. Chuyển ứng dụng sang chế độ chỉ đọc nếu có thể. |
| **ACC** | Lỗi xác thực hoàn toàn -- SSO/IAM ngừng hoạt động ngăn tất cả người dùng đăng nhập. SSL certificate hết hạn trên domain production. Khóa tài khoản hàng loạt ảnh hưởng sales trong giờ hành chính. | Ngay lập tức. Nếu không ai đăng nhập được, hệ thống thực tế đã ngừng dù hạ tầng vẫn chạy. | Tier 1 (cổng khách hàng và sales portal) và Tier 2 (hệ thống nội bộ) -- tất cả phụ thuộc xác thực. | 0 phút: Infra trực nhận cảnh báo. 15 phút: CTO được thông báo. 30 phút: IC kích hoạt. Nếu liên quan certificate: khắc phục ngay (không cần điều tra). | 1. Xác định nguyên nhân (SSO provider, IAM policy, certificate, MFA service). 2. Nếu certificate hết hạn: triển khai certificate mới ngay. 3. Nếu SSO: kiểm tra trạng thái provider, chuyển sang auth dự phòng nếu có. 4. Nếu thay đổi IAM policy: revert ngay. 5. Thông báo sales và nhân viên nội bộ với ETA. |
| **OTH** | Cổng thanh toán lỗi hoàn toàn -- tất cả kênh thu phí bảo hiểm ngừng. Lỗi tích hợp tái bảo hiểm trong cửa sổ gia hạn hiệp ước. Hệ thống feed pháp quy ngừng trong 24 giờ trước hạn nộp. | Ngay lập tức. Thu phí bảo hiểm bị dừng hoặc hạn pháp quy bị đe dọa. | Tier 1 (thanh toán ảnh hưởng khách hàng/sales) hoặc Tier 3 (feed pháp quy) với rủi ro P1 pháp quy. | 0 phút: Trực nhận cảnh báo. 15 phút: Trưởng phòng CNTT được thông báo. 30 phút: IC kích hoạt. Liên hệ hỗ trợ vendor. Nếu pháp quy: Cán bộ tuân thủ được thông báo. | 1. Liên hệ hỗ trợ vendor/bên thứ ba ngay. 2. Kích hoạt kênh dự phòng nếu có (cổng thanh toán backup, nộp thủ công). 3. Bật cơ chế xếp hàng/thử lại. 4. Thông báo người dùng bị ảnh hưởng (banner cổng, thông báo sales). 5. Theo dõi trạng thái vendor để biết ETA. 6. Nếu pháp quy: đánh giá phương án gia hạn. |

---

### 3.2 P2 -- Cao

**Chỉ báo chung**: Suy giảm đáng kể hệ thống Tier 1 hoặc Tier 2. Chức năng kinh doanh chính không khả dụng nhưng hệ thống vẫn hoạt động một phần. Nhiều người dùng bị ảnh hưởng trong giờ hành chính. Hiệu năng suy giảm nghiêm trọng đủ để cản trở tốc độ làm việc bình thường. Lỗi xử lý batch có tác động tài chính xuôi dòng.

**Ngưỡng thời gian ngừng**: Tối đa 4 giờ để kiểm soát. Giải quyết hoàn toàn trong 5 ngày làm việc.

**Sự cố nghiêm trọng**: CÓ ĐIỀU KIỆN -- tuyên bố Sự Cố Nghiêm Trọng nếu: (a) suy giảm kéo dài hơn 2 giờ trong giờ hành chính, (b) hơn 30% nhóm người dùng bị ảnh hưởng, hoặc (c) tác động tài chính/pháp quy được phát hiện trong quá trình điều tra.

**MTTA**: 30 phút (giờ hành chính; 1 giờ ngoài giờ nếu có trực).

**MTTR mục tiêu (Kiểm soát)**: 4 giờ. **MTTR mục tiêu (Giải quyết hoàn toàn)**: 5 ngày làm việc.

| Danh mục | Mô tả tác động | Mức khẩn cấp | Tầng hệ thống | Leo thang | Phản hồi ban đầu |
|----------|-------------------|---------|--------------|------------|---------------------------|
| **HW** | Suy giảm năng lực tính toán một phần -- hệ thống chạy nhưng ở công suất giảm. Failover sang secondary thành công nhưng chạy trên single instance (không có dự phòng). I/O lưu trữ suy giảm làm chậm giao dịch. | Cao. Mất dự phòng -- lỗi thứ hai sẽ gây P1. | Tier 1 hoặc Tier 2 chạy trên phần cứng suy giảm. | 0 phút: Kỹ sư trực được thông báo. 30 phút: Trưởng phòng CNTT được thông báo. 2 giờ: Leo thang CTO nếu không có hướng giải quyết. | 1. Xác nhận trạng thái dự phòng. 2. Cấp phát instance thay thế. 3. Di chuyển workload. 4. Khôi phục dự phòng. 5. Xác nhận hiệu năng. |
| **SW** | Tính năng chính không khả dụng (VD: sales không thể nộp đề xuất mới, nhưng có thể xem hợp đồng hiện có). Ứng dụng crash gián đoạn (5--30% request). Suy giảm hiệu năng sau triển khai -- trang tải chậm gấp 10 lần. Batch hoàn thành nhưng output sai cho một dòng sản phẩm. | Cao. Năng suất kinh doanh giảm nhưng không dừng. Rò rỉ doanh thu hoặc xử lý bị chậm. | Tier 1 (trải nghiệm sales/khách hàng suy giảm) hoặc Tier 2 (chức năng một phần không khả dụng) hoặc Tier 3 (output batch sai một phần). | 0 phút: Dev trực được thông báo. 30 phút: Trưởng phòng CNTT được thông báo. 1 giờ: Team lead leo thang nếu chưa xác định nguyên nhân. 4 giờ: CTO nếu chưa kiểm soát. | 1. Nếu sau triển khai: đánh giá rollback (rollback trước nếu crash gián đoạn). 2. Xác định chức năng và phạm vi người dùng bị ảnh hưởng. 3. Áp dụng giải pháp tạm thời nếu có. 4. Thông báo nhóm người dùng bị ảnh hưởng. 5. Nếu output batch sai: giữ lại xử lý xuôi dòng cho dòng sản phẩm bị ảnh hưởng. |
| **SEC** | Nghi ngờ nhưng chưa xác nhận sự kiện an ninh. GuardDuty phát hiện mẫu truy cập bất thường. Lộ một tài khoản (không phải admin). WAF chặn lưu lượng tấn công tăng cao nhưng dịch vụ suy giảm. Phát hiện chiến dịch phishing nhắm vào nhân viên. | Cao. Có thể leo thang P1 nếu xác nhận. Điều tra cần nhanh -- kẻ tấn công hành động nhanh. | Khác nhau. Sự kiện an ninh có thể ảnh hưởng mọi tầng. | 0 phút: Trưởng an ninh được thông báo. 30 phút: Trưởng phòng CNTT được thông báo. 1 giờ: CTO nếu phạm vi mở rộng. | 1. Điều tra và xác định phạm vi (có thật không? đã kiểm soát chưa?). 2. Cô lập tài khoản nghi ngờ bị xâm nhập. 3. Xem xét phát hiện GuardDuty/CloudTrail. 4. Đặt lại thông tin đăng nhập tài khoản bị ảnh hưởng. 5. Nếu xác nhận vi phạm: LEO THANG P1 ngay lập tức. |
| **CLD** | Một dịch vụ AWS suy giảm (VD: Lambda latency tăng, S3 lỗi gián đoạn). Một AZ gặp vấn đề nhưng triển khai multi-AZ hấp thụ tác động. CloudFront edge suy giảm ảnh hưởng một số vùng. | Cao. Dịch vụ suy giảm và khả năng chịu lỗi single-AZ đang bị tiêu hao -- lỗi AZ thứ hai sẽ gây P1. | Tier 1 (trải nghiệm khách hàng suy giảm) hoặc Tier 2 (hệ thống nội bộ chậm hơn). | 0 phút: Infra trực được thông báo. 30 phút: Trưởng phòng CNTT được thông báo. 2 giờ: Leo thang nếu AWS không có ETA. | 1. Kiểm tra AWS Health Dashboard. 2. Xác minh multi-AZ failover đang hấp thụ lưu lượng. 3. Chuyển hướng lưu lượng khỏi AZ/edge suy giảm. 4. Mở case hỗ trợ AWS (High). 5. Theo dõi và chuẩn bị kích hoạt DR nếu suy giảm lan rộng. |
| **DB** | Database replication lag vượt ngưỡng (read replica lỗi thời). Connection pool sử dụng 80%+. Backup job thất bại (RPO bị đe dọa). Một read replica ngừng (công suất giảm nhưng vẫn hoạt động). | Cao. Khả dụng hoặc bảo vệ dữ liệu suy giảm. Lỗi thứ hai sẽ gây P1. | Tier 2 (ứng dụng truy vấn chậm hơn) với tác động Tier 1 tiềm ẩn nếu lag gây hiển thị dữ liệu cũ. | 0 phút: DBA trực được thông báo. 30 phút: Trưởng phòng CNTT được thông báo. 2 giờ: Leo thang nếu khoảng cách replication tăng. | 1. Điều tra nguyên nhân replication lag (truy vấn chạy lâu, đột biến ghi, mạng). 2. Kill truy vấn chạy lâu nếu an toàn. 3. Backup thất bại: kích hoạt backup thủ công ngay. 4. Scale read replica nếu vấn đề công suất. 5. Theo dõi xu hướng connection pool. |
| **ACC** | SSO lỗi gián đoạn (một số người dùng bị ảnh hưởng, một số không). MFA service suy giảm -- người dùng bị chậm. Cấp tài khoản mới bị lỗi (người dùng hiện tại không ảnh hưởng). Certificate sắp hết hạn trong 7 ngày (chưa hết hạn). | Cao. Không phải tất cả người dùng bị chặn, nhưng hệ thống xác thực không đáng tin cậy. Có thể xấu đi. | Tier 1 và Tier 2 (lỗi đăng nhập gián đoạn trên các hệ thống). | 0 phút: Infra trực được thông báo. 30 phút: Trưởng phòng CNTT được thông báo. 2 giờ: Leo thang nếu không ổn định. | 1. Xác định mẫu (người dùng nào, IdP nào, thời điểm). 2. Kiểm tra trạng thái SSO provider. 3. Khởi động lại thành phần auth nếu áp dụng được. 4. Certificate sắp hết hạn: bắt đầu gia hạn ngay. 5. Thông báo giải pháp tạm thời cho người dùng bị ảnh hưởng (thử lại, trình duyệt khác, xóa cache). |
| **OTH** | Cổng thanh toán lỗi gián đoạn (60--70% tỷ lệ thành công). API bên thứ ba phản hồi chậm gây timeout trong công cụ báo giá sales. Batch scheduler chạy trễ -- xử lý xuôi dòng bị chậm nhưng chưa trượt hạn. Batch tính hoa hồng thất bại (chi trả sales bị đe dọa). | Cao. Chức năng kinh doanh suy giảm, doanh thu hoặc sự hài lòng sales bị ảnh hưởng. Có thể có áp lực hạn chót. | Tier 1 (thanh toán/báo giá suy giảm cho sales/khách hàng) hoặc Tier 3 (batch bị chậm). | 0 phút: Trực được thông báo. 30 phút: Trưởng phòng CNTT được thông báo. Nếu batch hoa hồng: thông báo bộ phận vận hành sales. 2 giờ: Leo thang nếu vendor không phản hồi. | 1. Liên hệ vendor/bên thứ ba. 2. Triển khai logic thử lại hoặc fallback thủ công. 3. Batch thất bại: đánh giá cửa sổ chạy lại (có thể hoàn thành trước 6h sáng không?). 4. Thông báo đơn vị kinh doanh bị ảnh hưởng. 5. Thanh toán: chuyển sang gateway dự phòng nếu có. |

---

### 3.3 P3 -- Trung Bình

**Chỉ báo chung**: Ảnh hưởng một phần đến chức năng không quan trọng. Có giải pháp tạm thời đã biết. Nhóm người dùng hạn chế bị ảnh hưởng (một đội, một dòng sản phẩm, một vùng). Không có dữ liệu tài chính bị đe dọa. Dịch vụ hoạt động nhưng bất tiện.

**Ngưỡng thời gian ngừng**: Suy giảm chấp nhận được đến 1 ngày làm việc. Giải quyết hoàn toàn trong 10 ngày làm việc.

**Sự cố nghiêm trọng**: KHÔNG -- trừ khi điều tra phát hiện tác động tài chính/dữ liệu ẩn (khi đó phân loại lại).

**MTTA**: 2 giờ làm việc.

**MTTR mục tiêu (Kiểm soát)**: 1 ngày làm việc. **MTTR mục tiêu (Giải quyết hoàn toàn)**: 10 ngày làm việc.

| Danh mục | Mô tả tác động | Mức khẩn cấp | Tầng hệ thống | Leo thang | Phản hồi ban đầu |
|----------|-------------------|---------|--------------|------------|---------------------------|
| **HW** | Lỗi thiết bị ngoại vi không quan trọng (máy in, máy quét tại chi nhánh). Vấn đề máy trạm ảnh hưởng cá nhân. Server non-production suy giảm. | Bình thường. Người dùng có thể sử dụng thiết bị/máy trạm thay thế. | Tier 2 (máy trạm cá nhân) hoặc hạ tầng hỗ trợ. | 2 giờ: Team lead nếu không có tiến triển. 1 ngày làm việc: Trưởng phòng CNTT nếu chưa giải quyết. | 1. Cung cấp thiết bị thay thế. 2. Ghi nhận ticket hỗ trợ phần cứng. 3. Lên lịch thay thế/sửa chữa. |
| **SW** | Một báo cáo hiển thị sai định dạng. Một tính năng không quan trọng bị lỗi (VD: xem trước tài liệu hợp đồng lỗi nhưng tải về vẫn được). Lỗi hiển thị UI trên trình duyệt cụ thể. Lỗi trường dữ liệu phi tài chính. | Bình thường. Kinh doanh tiếp tục với bất tiện nhỏ. | Tier 2 (lỗi nhỏ công cụ nội bộ) hoặc Tier 1 (vấn đề giao diện/không chặn hướng khách hàng). | 2 giờ: Team lead nếu không có tiến triển. 4 giờ: Dev lead nếu cần hỗ trợ chẩn đoán. | 1. Ghi nhận vấn đề với bước tái tạo. 2. Xác nhận giải pháp tạm thời hoạt động và thông báo người dùng bị ảnh hưởng. 3. Đưa vào sprint phát triển để sửa. |
| **SEC** | Báo cáo email phishing nhưng không lộ thông tin đăng nhập. Phát hiện lỗ hổng cần vá (không bị khai thác tích cực). Hoạt động đáng ngờ trên một tài khoản (đã kiểm soát). | Vừa phải. Cần xử lý kịp thời nhưng không có mối đe dọa đang hoạt động. | Mọi tầng (vá lỗ hổng) hoặc tài khoản cá nhân. | 4 giờ: Trưởng an ninh xem xét. 1 ngày làm việc: Lên lịch vá. | 1. Chặn/cách ly email phishing. 2. Cảnh báo người dùng bị ảnh hưởng. 3. Lỗ hổng: đánh giá mức độ nghiêm trọng (CVSS), lên lịch cửa sổ vá. 4. Theo dõi chỉ báo leo thang. |
| **CLD** | Vấn đề môi trường non-production (staging, dev). Cảnh báo CloudWatch cho metric không quan trọng. S3 lifecycle policy không thực thi (không tác động ngay). | Bình thường. Không tác động production. Vấn đề vệ sinh vận hành. | Tier 3 hoặc non-production. | 4 giờ: Team lead biết. 1 ngày làm việc: Đội infra lên lịch sửa. | 1. Xác nhận không tác động production. 2. Ghi nhận và lên lịch khắc phục. 3. Theo dõi mẫu (có thể chỉ báo vấn đề đang phát sinh). |
| **DB** | Truy vấn chậm ảnh hưởng một báo cáo không quan trọng. Vấn đề database non-production. Cần tối ưu truy vấn (hiệu năng dưới tối ưu nhưng trong SLA). Replication delay nhỏ trên read replica chỉ dùng cho báo cáo. | Bình thường. Vận hành production không bị ảnh hưởng. | Tier 3 (báo cáo/analytics) hoặc non-production. | 4 giờ: DBA biết. 1 ngày làm việc: Lên lịch tối ưu. | 1. Xác nhận production không bị ảnh hưởng. 2. Xác định truy vấn chậm. 3. Áp dụng tối ưu index hoặc truy vấn nhanh nếu rủi ro thấp. 4. Lên lịch sửa chính thức. |
| **ACC** | Một người dùng không thể đăng nhập (vấn đề tài khoản cụ thể). Cấp tài khoản mới bị chậm nhưng không bị chặn. Cấu hình sai quyền/vai trò ảnh hưởng chức năng không quan trọng cho cá nhân. | Bình thường. Bất tiện cá nhân, không hệ thống. | Tài khoản người dùng cá nhân. | 2 giờ: L1 dự kiến giải quyết. 4 giờ: Leo thang nếu nghi ngờ nguyên nhân hệ thống. | 1. Kiểm tra trạng thái tài khoản (khóa, hết hạn, MFA). 2. Đặt lại thông tin đăng nhập nếu cần. 3. Nếu xuất hiện mẫu (nhiều cá nhân): đánh giá lại thành P2. |
| **OTH** | Tích hợp bên thứ ba không quan trọng lỗi (VD: feed dữ liệu analytics). Công việc định kỳ cho báo cáo không khẩn cấp chạy trễ. Cảnh báo API vendor sắp ngừng hỗ trợ phiên bản. Dịch vụ thông báo email bị chậm. | Bình thường. Không có chức năng kinh doanh bị chặn. | Tier 3 (analytics, feed không quan trọng). | 4 giờ: Team lead biết. 1 ngày làm việc: Liên hệ vendor nếu cần. | 1. Xác nhận không tác động kinh doanh xuôi dòng. 2. Áp dụng giải pháp tạm thời nếu có. 3. Liên hệ vendor nếu phụ thuộc bên ngoài. 4. Lên lịch sửa. |

---

### 3.4 P4 -- Thấp

**Chỉ báo chung**: Vấn đề giao diện, lỗi UI nhỏ, lỗi tài liệu, yêu cầu tính năng bị báo nhầm là sự cố, hoặc vấn đề không có tác động đo lường được đến người dùng hoặc kinh doanh. Các mục "sửa thì tốt" không ảnh hưởng khả năng làm việc của bất kỳ ai.

**Ngưỡng thời gian ngừng**: Không áp dụng -- không có thời gian ngừng hoặc suy giảm liên quan.

**Sự cố nghiêm trọng**: KHÔNG.

**MTTA**: Ngày làm việc tiếp theo.

**MTTR mục tiêu (Giải quyết hoàn toàn)**: 15 ngày làm việc (hoặc lên lịch vào sprint phát triển tiếp theo).

| Danh mục | Mô tả tác động | Mức khẩn cấp | Tầng hệ thống | Leo thang | Phản hồi ban đầu |
|----------|-------------------|---------|--------------|------------|---------------------------|
| **HW** | Vấn đề phần cứng giao diện (VD: bàn phím kẹt, hiệu chỉnh màu màn hình). Yêu cầu thiết bị dự phòng. | Thấp. Không ảnh hưởng khả năng làm việc. | Hạ tầng hỗ trợ. | Không trừ khi tái phát 3+ lần. | 1. Ghi nhận yêu cầu. 2. Lên lịch thay thế trong chu kỳ mua sắm tiếp theo. |
| **SW** | Font sai trên một màn hình. Nội dung tooltip không chính xác. Lỗi căn chỉnh nhỏ trong PDF tạo ra. Năm bản quyền lỗi thời ở footer. Tính năng hoạt động đúng nhưng nhãn gây nhầm lẫn. | Thấp. Giao diện. Không ảnh hưởng logic kinh doanh. | Tier 1 hoặc Tier 2 (lớp giao diện). | Không. Thêm vào backlog phát triển. | 1. Ghi nhận với ảnh chụp màn hình. 2. Thêm vào backlog, ưu tiên trong sprint planning. |
| **SEC** | Thông báo an ninh thông tin không áp dụng. Kết quả dương tính giả từ security scanner. Thông báo vá định kỳ. | Thấp. Không có mối đe dọa. | Không áp dụng. | Không. Theo dõi cho hồ sơ tuân thủ. | 1. Ghi nhận cho audit trail. 2. Đóng hoặc lên lịch hành động thường xuyên. |
| **CLD** | Thông báo dọn dẹp tài nguyên không sử dụng. Khuyến nghị tối ưu chi phí. Vi phạm tagging trên tài nguyên non-production. | Thấp. Vệ sinh vận hành. | Non-production hoặc quản lý chi phí. | Không. Xem xét trong chu kỳ FinOps tiếp theo. | 1. Ghi nhận để theo dõi. 2. Lên lịch trong đợt rà soát vận hành tiếp theo. |
| **DB** | Tài liệu schema lỗi thời nhỏ. Khuyến nghị index không quan trọng. Cần dọn dẹp database test. | Thấp. Không tác động vận hành. | Non-production hoặc tài liệu. | Không. Lên lịch trong cửa sổ bảo trì. | 1. Ghi nhận. 2. Thêm vào backlog bảo trì DBA. |
| **ACC** | Một người dùng yêu cầu thêm quyền không khẩn cấp. Tên hiển thị không chính xác trong directory. | Thấp. Yêu cầu dịch vụ bị chuyển nhầm thành sự cố. | Người dùng cá nhân. | Không. Phân loại lại thành Service Request nếu áp dụng. | 1. Phân loại lại thành Service Request nếu phù hợp. 2. Xử lý qua quy trình quản lý truy cập bình thường. |
| **OTH** | Thông báo vendor không quan trọng. Lỗi định dạng log nhỏ. Yêu cầu dọn dẹp dữ liệu test. | Thấp. Không tác động kinh doanh. | Non-production hoặc vệ sinh vận hành. | Không. | 1. Ghi nhận. 2. Lên lịch trong cửa sổ bảo trì hoặc sprint tiếp theo. |

---

## 4. Tiêu Chí Tuyên Bố Sự Cố Nghiêm Trọng

**Sự Cố Nghiêm Trọng (Major Incident)** kích hoạt toàn bộ cơ cấu chỉ huy sự cố: Incident Commander (IC), phòng chỉ huy, thông báo trạng thái định kỳ, chuỗi thông báo ban lãnh đạo, và Đánh Giá Sau Sự Cố bắt buộc.

### Tuyên Bố Tự Động (Không Cần Phán Đoán)

| Tiêu chí | Áp dụng khi |
|-----------|-------------|
| Tất cả sự cố P1 | Luôn là Sự Cố Nghiêm Trọng |
| Vi phạm dữ liệu đã xác nhận liên quan PII | Bất kể đánh giá mức ưu tiên ban đầu |
| Sai lệch dữ liệu tài chính đã xác nhận | Giá trị tài chính chủ hợp đồng, tính toán phí bảo hiểm, số tiền bồi thường |
| Ngừng hoạt động hoàn toàn hệ thống Tier 1 | Cổng khách hàng, sales portal, xử lý thanh toán |
| Kích hoạt DR | Bất kỳ sự cố nào yêu cầu failover sang vùng phụ |
| Nghĩa vụ báo cáo pháp quy được kích hoạt | Sự kiện yêu cầu thông báo cơ quan quản lý bảo hiểm hoặc cơ quan bảo vệ dữ liệu |

### Tuyên Bố Có Điều Kiện (Phán Đoán của IC hoặc Trưởng phòng CNTT)

| Tiêu chí | Tuyên bố Nghiêm Trọng nếu... |
|-----------|-------------------|
| Thời lượng sự cố P2 | Suy giảm kéo dài hơn 2 giờ trong giờ hành chính |
| Phạm vi tác động người dùng P2 | Hơn 30% nhóm người dùng bị ảnh hưởng |
| P2 có yếu tố tài chính | Điều tra phát hiện dữ liệu tài chính có thể bị ảnh hưởng (phân loại lại thành P1) |
| Sự cố P3 với phạm vi mở rộng | Phạm vi ảnh hưởng lớn hơn đánh giá ban đầu (phân loại lại) |
| Bất kỳ sự cố nào trong cửa sổ nộp pháp quy | Trong 48 giờ trước hạn báo cáo pháp quy |
| Rủi ro uy tín | Chú ý mạng xã hội / báo chí, hoặc lượng khiếu nại khách hàng tăng đột biến |

---

## 5. Tóm Tắt SLA Theo Mức Ưu Tiên

| Chỉ số | P1 Nghiêm trọng | P2 Cao | P3 Trung bình | P4 Thấp |
|--------|------------|---------|-----------|--------|
| **MTTA** | 15 phút | 30 phút | 2 giờ làm việc | Ngày làm việc tiếp theo |
| **Cập nhật đầu tiên** | 30 phút | 1 giờ | Khi phân loại | Khi phân loại |
| **Tần suất cập nhật trạng thái** | Mỗi 30 phút | Mỗi 1 giờ | Theo yêu cầu | Theo yêu cầu |
| **Mục tiêu kiểm soát** | 2 giờ | 4 giờ | 1 ngày làm việc | Không áp dụng |
| **Mục tiêu giải quyết hoàn toàn** | 24 giờ | 5 ngày làm việc | 10 ngày làm việc | 15 ngày làm việc |
| **Đồng hồ SLA** | 24/7 (giờ thực) | Giờ hành chính (8h--18h T2--T7) | Giờ hành chính | Giờ hành chính |
| **Đánh giá sau sự cố** | Bắt buộc (trong 48 giờ) | Bắt buộc (trong 5 ngày làm việc) | Ghi chú đơn giản trong ticket (trong 5 ngày làm việc) | Không yêu cầu (trừ khi tái phát 3+ lần) |
| **Cập nhật Knowledge Base** | Bắt buộc | Bắt buộc | Nếu có khả năng tái phát | Chỉ khi xuất hiện mẫu |

### Xử Lý Giờ Hành Chính vs Ngoài Giờ

| Mức ưu tiên | Giờ hành chính (8h--18h T2--T7) | Ngoài giờ (đêm, Chủ nhật, ngày lễ) |
|----------|-----------------------------------|----------------------------------------|
| **P1** | Phản hồi toàn lực. Toàn bộ nhân sự. IC kích hoạt. Phòng chỉ huy. Ban lãnh đạo được thông báo. | Kỹ sư trực phản hồi. IC kích hoạt từ xa. Ban lãnh đạo được thông báo qua điện thoại. Cùng mục tiêu kiểm soát. |
| **P2** | Phản hồi toàn lực. Đội trực cộng leo thang chuyên gia. | Kỹ sư trực đánh giá. Nếu tác động Tier 1: phản hồi toàn lực. Nếu chỉ Tier 2: kiểm soát và lên lịch sửa ngày làm việc tiếp theo trừ khi suy giảm đang xấu đi. |
| **P3** | Kỹ sư được phân công làm trong giờ hành chính. | Không phản hồi ngoài giờ. Ghi nhận cho ngày làm việc tiếp theo. |
| **P4** | Backlog. Lên lịch vào sprint. | Không phản hồi ngoài giờ. |

---

## 6. Ma Trận Leo Thang

### Leo Thang Theo Mức Ưu Tiên và Thời Gian

| Thời gian trôi qua | Hành động P1 | Hành động P2 | Hành động P3 | Hành động P4 |
|-------------|-----------|-----------|-----------|-----------|
| **0 phút** | Kỹ sư trực tự động nhận cảnh báo | Kỹ sư trực được thông báo | -- | -- |
| **15 phút** | CTO/Trưởng phòng CNTT được thông báo. IC được phân công. | -- | -- | -- |
| **30 phút** | IC kích hoạt. Phòng chỉ huy mở. Cập nhật trạng thái đầu tiên. | Trưởng phòng CNTT được thông báo | -- | -- |
| **1 giờ** | CEO được báo cáo (nếu hướng khách hàng hoặc pháp quy). Cuộc họp bridge ban lãnh đạo nếu cần. | Team lead leo thang nếu chưa xác định nguyên nhân | -- | -- |
| **2 giờ** | Nếu chưa kiểm soát: đánh giá lại phương pháp. Xem xét kích hoạt DR. Leo thang chuyên gia bên ngoài/vendor. | -- | Team lead nếu không có tiến triển | -- |
| **4 giờ** | Nếu chưa giải quyết: leo thang cấp điều hành. Leo thang CEO-đối-CEO với vendor nếu do vendor gây ra. | CTO được thông báo nếu chưa kiểm soát. Đánh giá lại: có nên là P1 không? | -- | -- |
| **8 giờ** | Phản hồi liên tục với luân chuyển nhân sự. Thông báo Hội đồng quản trị nếu dữ liệu khách hàng bị xâm phạm. | Trưởng phòng CNTT xem xét lại. Đánh giá nhu cầu tài nguyên. | -- | -- |
| **1 ngày làm việc** | Vẫn chưa giải quyết: quy trình quản lý khủng hoảng. | -- | Trưởng phòng CNTT nếu chưa giải quyết | Team lead nếu tái phát |

### Leo Thang Theo Vai Trò

| Vai trò | Liên hệ khi | Phương thức liên hệ |
|------|--------------|----------------|
| **Kỹ sư trực** | Tất cả sự cố P1, P2. Phản hồi kỹ thuật ban đầu. | Cảnh báo tự động (PagerDuty/OpsGenie) + điện thoại |
| **Team Lead** | P2 nếu chưa xác định nguyên nhân trong 1 giờ. P3 nếu không có tiến triển trong 2 giờ. Hướng dẫn kỹ thuật. | Chat + điện thoại |
| **Trưởng phòng CNTT** | Tất cả P1 lúc 15 phút. P2 lúc 30 phút. P3 lúc 1 ngày làm việc nếu chưa giải quyết. Quyết định tài nguyên. | Điện thoại + chat |
| **DBA trực** | Tất cả sự cố danh mục DB mức P1/P2. Liên quan DB trong các danh mục khác. | Cảnh báo tự động + điện thoại |
| **Trưởng an ninh** | Tất cả sự cố danh mục SEC. Bất kỳ sự cố nào có yếu tố an ninh. | Điện thoại (P1 ngay) + chat |
| **CTO** | P1 lúc 15 phút. P2 lúc 4 giờ nếu chưa kiểm soát. Quyết định kích hoạt DR. | Điện thoại |
| **CEO** | P1 lúc 1 giờ nếu hướng khách hàng hoặc pháp quy. Vi phạm dữ liệu liên quan PII. | Điện thoại (qua CTO) |
| **Cán bộ tuân thủ** | Bất kỳ sự cố nào có hệ quả báo cáo pháp quy. Vi phạm dữ liệu. Sai lệch dữ liệu tài chính. | Điện thoại (P1) + email (P2) |
| **Hỗ trợ Vendor** | Lỗi phụ thuộc bên ngoài. Leo thang L3 cho sản phẩm vendor. | Cổng hỗ trợ vendor + điện thoại. Liên hệ đã sắp xếp trước cho vendor quan trọng. |

---

## 7. Yêu Cầu Truyền Thông

| Mức ưu tiên | Truyền thông nội bộ | Truyền thông khách hàng | Truyền thông Sales | Truyền thông pháp quy |
|----------|----------------------|----------------------|--------------------|-----------------------|
| **P1** | Kênh phòng chỉ huy. Cập nhật mỗi 30 phút. Cuộc họp bridge ban lãnh đạo. Email toàn bộ cho sự cố kéo dài (>2 giờ). | Banner bảo trì trên cổng. SMS/email cho sự cố hệ thống thanh toán. Dịch vụ khách hàng được brief với talking points. | Hotline Sales được brief. Banner sales portal. SMS broadcast cho sự cố hệ thống. Cung cấp hướng dẫn xử lý offline. | Đánh giá trong 1 giờ. Thông báo nếu vi phạm dữ liệu (PII), ngừng hoạt động kéo dài (>4 giờ hướng khách hàng), hoặc lỗi giao dịch tài chính vượt ngưỡng. |
| **P2** | Cập nhật kênh sự cố. Cập nhật mỗi 1 giờ. Đơn vị kinh doanh bị ảnh hưởng được thông báo. | Banner cổng nếu tính năng hướng khách hàng suy giảm. Cập nhật FAQ nếu khách hàng nhìn thấy. | Thông báo sales nếu tính năng hướng sales bị ảnh hưởng. Giải pháp tạm thời được truyền đạt. | Đánh giá nếu có xu hướng đạt ngưỡng pháp quy. Không thông báo chủ động trừ khi đạt ngưỡng. |
| **P3** | Kênh đội. Người dùng bị ảnh hưởng được thông báo trực tiếp. | Không truyền thông bên ngoài. | Không truyền thông trừ khi sales bị ảnh hưởng cụ thể. | Không. |
| **P4** | Chỉ cập nhật ticket. | Không. | Không. | Không. |

---

## 8. Các Kịch Bản Đặc Thù Bảo Hiểm và Phân Loại

Các kịch bản này minh họa cách ma trận áp dụng cho các tình huống vận hành bảo hiểm nhân thọ phổ biến. Xem các ví dụ phân tích chi tiết tại [scenarios.md](scenarios.md).

### Tier 1 -- Kịch Bản Hướng Khách Hàng

| Kịch bản | Danh mục | Mức ưu tiên | Nghiêm trọng? | Lưu ý quan trọng |
|----------|----------|----------|--------|-------------------|
| Cổng khách hàng ngừng hoàn toàn | CLD/HW | P1 | Có | Khách hàng không thể truy cập hợp đồng, nộp yêu cầu bồi thường, hoặc thanh toán. Tác động doanh thu và niềm tin. |
| Thanh toán phí bảo hiểm trực tuyến lỗi cho tất cả khách hàng | OTH | P1 | Có | Cổng thanh toán lỗi dừng thu phí. Kích hoạt gateway dự phòng. |
| Ứng dụng di động khách hàng crash khi khởi động | SW | P1 | Có | Tầm nhìn cao. Đánh giá app store sẽ phản ánh trong vài giờ. |
| Cổng khách hàng chậm (15 giây mỗi trang) | CLD/SW | P2 | Có điều kiện | Suy giảm nhưng hoạt động. P1 nếu đúng cao điểm đăng ký/gia hạn. |
| Lỗi nộp yêu cầu bồi thường điện tử cho một sản phẩm | SW | P2 | Không | Giải pháp tạm: tổng đài có thể nộp. Theo dõi khối lượng. |
| Tài liệu hợp đồng tải về hiển thị sai tên người thụ hưởng | SW | P1 | Có | Vấn đề toàn vẹn dữ liệu -- có thể chỉ hiển thị hoặc sai lệch dữ liệu. Điều tra ngay. |

### Tier 1 -- Kịch Bản Hướng Đại Lý

| Kịch bản | Danh mục | Mức ưu tiên | Nghiêm trọng? | Lưu ý quan trọng |
|----------|----------|----------|--------|-------------------|
| Sales portal ngừng trong mùa đăng ký mở | CLD/HW | P1 | Có | Cửa sổ doanh thu quan trọng. Mỗi giờ ngừng là mất doanh số. |
| Công cụ báo giá trả phí bảo hiểm sai | SW | P1 | Có | Sales báo giá sai cho khách hàng. Dừng ngay. Rủi ro tài chính và pháp quy. |
| Dashboard hoa hồng Sales không khả dụng | SW | P2 | Không | Sales bức xúc nhưng vẫn có thể bán. Sửa trong ngày làm việc. |
| Nộp đề xuất lỗi gián đoạn | SW | P2 | Có điều kiện | Nếu >30% tỷ lệ lỗi trong giờ hành chính: tuyên bố Nghiêm Trọng. |
| SSO Sales lỗi cho một chi nhánh cụ thể | ACC | P2 | Không | Phạm vi hạn chế. Cung cấp thông tin đăng nhập tạm thời làm giải pháp. |
| Sales portal chậm vào buổi tối | CLD/SW | P3 | Không | Sales làm việc buổi tối nhưng lượng thấp hơn. Lên lịch sửa ngày mai. |

### Tier 2 -- Kịch Bản Kinh Doanh Nội Bộ

| Kịch bản | Danh mục | Mức ưu tiên | Nghiêm trọng? | Lưu ý quan trọng |
|----------|----------|----------|--------|-------------------|
| Hệ thống quản trị hợp đồng cốt lõi (PAS) ngừng | CLD/HW/SW | P1 | Có | Tất cả thẩm định, phục vụ hợp đồng và xử lý bồi thường bị dừng. |
| Claims engine cho kết quả tự động phê duyệt sai | SW | P1 | Có | Chi trả bồi thường sai. Tổn thất tài chính và rủi ro pháp quy. Dừng tự động phê duyệt ngay. |
| Underwriting workbench không khả dụng | SW | P2 | Có điều kiện | Xử lý kinh doanh mới bị chậm. Nghiêm trọng nếu hàng đợi vượt 4 giờ trong cao điểm. |
| Billing engine không tạo được thông báo phí bảo hiểm hàng tháng | SW/OTH | P2 | Không | Thu phí bảo hiểm bị đe dọa. Phải giải quyết trước chu kỳ thu tiếp theo. |
| Hệ thống tính toán actuarial chậm | DB/SW | P3 | Không | Actuarial bị chậm nhưng không tác động khách hàng. Giải pháp: chạy tính toán ngoài cao điểm. |
| Công cụ báo cáo tuân thủ lỗi định dạng | SW | P3 | Không | Nội dung báo cáo đúng, định dạng sai. Có thể sửa thủ công. |

### Tier 3 -- Kịch Bản Batch/Back-Office

| Kịch bản | Danh mục | Mức ưu tiên | Nghiêm trọng? | Lưu ý quan trọng |
|----------|----------|----------|--------|-------------------|
| Batch phân bổ phí bảo hiểm đêm thất bại | OTH/DB | P2 | Có điều kiện | Phải hoàn thành trước 6h sáng. Nghiêm trọng nếu cửa sổ chạy lại không đủ. |
| Batch tính hoa hồng cho số tiền sai | SW | P1 | Có | Sai lệch dữ liệu tài chính. Chi trả sales bị đe dọa. Giữ lại đợt thanh toán. |
| Tạo báo cáo pháp quy thất bại, hạn nộp trong 3 ngày | OTH/SW | P2 | Không | Áp lực hạn chót. Leo thang nếu không giải quyết trong 24 giờ. |
| Tạo báo cáo pháp quy thất bại, hạn nộp ngày mai | OTH/SW | P1 | Có | Hạn pháp quy cận kề. Toàn lực khắc phục. |
| Data warehouse ETL chậm 4 giờ | OTH/DB | P3 | Không | Analytics bị chậm nhưng không tác động vận hành. |
| Batch lưu trữ tài liệu thất bại | OTH | P3 | Không | Không tác động ngay. Lên lịch chạy lại. Theo dõi tái phát. |

---

## 9. Hướng Dẫn Phân Loại Lại Mức Ưu Tiên

Mức ưu tiên không cố định. Phải được đánh giá lại khi có thông tin mới.

### Kích Hoạt Nâng Mức (Tăng Ưu Tiên)

| Hiện tại | Nâng lên | Khi nào |
|---------|-----------|------|
| P2 | P1 | Suy giảm trở thành ngừng hoàn toàn. Phát hiện tác động dữ liệu tài chính. Thời lượng vượt 2 giờ trong giờ hành chính. Phạm vi lớn hơn đánh giá ban đầu. |
| P3 | P2 | Phạm vi ảnh hưởng lớn hơn dự kiến (nhiều người dùng/hệ thống hơn). Tác động giờ hành chính được xác nhận. Giải pháp tạm thời thất bại. |
| P3 | P1 | Điều tra phát hiện sai lệch dữ liệu tài chính. Hạn pháp quy bị đe dọa. |
| P4 | P3 | Xuất hiện mẫu (3+ lần xảy ra). Nguyên nhân cơ bản gợi ý vấn đề hệ thống lớn hơn. |

### Kích Hoạt Giảm Mức (Giảm Ưu Tiên)

| Hiện tại | Giảm xuống | Khi nào |
|---------|-------------|------|
| P1 | P2 | Dịch vụ khôi phục ở trạng thái suy giảm nhưng sử dụng được (đã kiểm soát). Phạm vi xác nhận nhỏ hơn lo ngại. |
| P2 | P3 | Giải pháp tạm thời hiệu quả đã triển khai. Tác động hạn chế ở nhóm người dùng nhỏ. |
| P3 | P4 | Xác nhận chỉ là vấn đề giao diện. Không tác động kinh doanh. |

### Thẩm Quyền Phân Loại Lại

| Hành động | Ai có thể thực hiện |
|--------|--------------|
| Nâng lên P1 | Bất kỳ ai (bất kỳ thành viên đội nào đều có thể leo thang P1 -- ưu tiên thận trọng) |
| Nâng lên P2 | L1 trực, Team Lead, IC, Trưởng phòng CNTT |
| Giảm từ P1 | Chỉ IC hoặc Trưởng phòng CNTT (với lý do được ghi nhận) |
| Giảm từ P2 | IC, Team Lead, hoặc Trưởng phòng CNTT |
| Giảm P3/P4 | Kỹ sư được phân công với Team Lead biết |

---

## 10. Tham Chiếu Nhanh Báo Cáo Pháp Quy

Một số điều kiện sự cố có thể kích hoạt nghĩa vụ báo cáo bắt buộc đến cơ quan quản lý bảo hiểm hoặc cơ quan bảo vệ dữ liệu. Đây là checklist tham chiếu nhanh -- quy trình chi tiết do bộ phận Tuân thủ duy trì.

| Điều kiện kích hoạt | Nghĩa vụ báo cáo | Thời hạn | Chịu trách nhiệm |
|------------------|---------------------|----------|-------------|
| Vi phạm dữ liệu cá nhân (PII của chủ hợp đồng, người được bảo hiểm, người thụ hưởng bị lộ hoặc mất) | Thông báo cơ quan bảo vệ dữ liệu. Có thể thông báo cá nhân bị ảnh hưởng. | Đánh giá trong 1 giờ. Báo cáo trong 72 giờ sau xác nhận (hoặc theo quy định địa phương). | Cán bộ tuân thủ + Pháp lý |
| Giao dịch tài chính xử lý sai vượt ngưỡng quy định | Thông báo cơ quan quản lý bảo hiểm | Theo yêu cầu pháp quy (đánh giá trong 24 giờ) | Cán bộ tuân thủ + Tài chính |
| Hệ thống hướng khách hàng cốt lõi không khả dụng >4 giờ trong giờ hành chính | Thông báo cơ quan quản lý bảo hiểm (nếu quy định địa phương yêu cầu) | Trong 24 giờ sau khi đóng sự cố | Cán bộ tuân thủ + Trưởng phòng CNTT |
| Sự kiện ảnh hưởng quyền lợi chủ hợp đồng (chậm chi trả bồi thường, giá trị hợp đồng sai phát hành cho khách hàng) | Thông báo cơ quan quản lý bảo hiểm | Theo yêu cầu pháp quy | Cán bộ tuân thủ |
| Sự cố an ninh mạng có tính chất nghiêm trọng | Cơ quan quản lý bảo hiểm và cơ quan có thẩm quyền liên quan | Đánh giá trong 1 giờ. Báo cáo theo thời hạn pháp quy. | Trưởng an ninh + Tuân thủ + Pháp lý |

**Lưu ý**: Thời hạn và ngưỡng báo cáo cụ thể phải được xác nhận theo quy định bảo hiểm và bảo vệ dữ liệu Việt Nam hiện hành. Bảng này cung cấp khung -- bộ phận Tuân thủ phải điền ngưỡng chính xác và thông tin liên hệ.

---

## 11. Tham Chiếu Chéo: Tác Động Danh Mục Đến Phân Loại Ưu Tiên

Bảng này cho thấy xu hướng ảnh hưởng của mỗi danh mục đến mức ưu tiên. Không thay thế cây quyết định trong [classification.md](classification.md) -- cung cấp hướng dẫn cho các trường hợp ranh giới.

| Danh mục | Xu hướng nâng mức ưu tiên | Lý do |
|----------|-------|-----------|
| **SEC** | Áp lực nâng mạnh | Sự cố an ninh có phạm vi ảnh hưởng khó dự đoán và hệ quả pháp quy. Phạm vi chưa rõ nên đối xử như trường hợp xấu nhất cho đến khi xác nhận ngược lại. |
| **DB** | Áp lực nâng vừa-đến-mạnh | Vấn đề database ảnh hưởng tất cả ứng dụng. Sai lệch dữ liệu không thể đảo ngược nếu không có backup. |
| **ACC** | Áp lực nâng vừa phải | Lỗi xác thực có tác động rộng -- tương đương ngừng hoạt động dù hệ thống vẫn chạy. |
| **CLD** | Tùy phạm vi | Suy giảm đơn dịch vụ có thể là P2/P3. Vấn đề đa dịch vụ hoặc regional là P1. |
| **SW** | Tùy tác động dữ liệu | Lỗi giao diện là P4. Lỗi tính toán ảnh hưởng dữ liệu tài chính là P1. Phạm vi rộng. |
| **HW** | Tùy dự phòng | Nếu dự phòng hấp thụ lỗi: P2. Nếu điểm lỗi đơn: P1. |
| **OTH** | Tùy mức độ quan trọng phụ thuộc | Cổng thanh toán: P1. Feed analytics: P3. Khác nhau tùy vai trò bên thứ ba trong chuỗi giá trị. |

---

## 12. Ghi Chú Vận Hành

### Cho L1 / Service Desk

- **Khi nghi ngờ, leo thang lên, không xuống.** Luôn tốt hơn khi tuyên bố mức ưu tiên cao hơn rồi hạ xuống so với đánh giá thấp và mất thời gian phản hồi. Không ai bị trách vì P1 giả. Người ta bị trách vì bỏ lỡ P1 thật.
- **Kiểm tra Knowledge Base trước.** Nếu có kịch bản đã biết khớp, sử dụng mức ưu tiên và phản hồi đã ghi nhận. Không phát minh lại quy trình phân loại.
- **Sự cố ứng dụng phức tạp.** Nếu hạ tầng trông bình thường nhưng có vấn đề, và không có KB match, gán mức ưu tiên sơ bộ và kết nối đội kỹ thuật trong 30 phút. Không tự chẩn đoán logic ứng dụng.
- **"Lỗi do vendor" không phải là giải pháp.** Chúng ta sở hữu dịch vụ với người dùng. Leo thang vendor VÀ kích hoạt kế hoạch dự phòng đồng thời.

### Cho Incident Commander

- **P1/P2: Kiểm soát trước, điều tra sau.** Rollback triển khai, failover sang standby, bật chế độ bảo trì -- rồi tìm nguyên nhân gốc.
- **Quản lý truyền thông chủ động.** Chỉ định một người cho tất cả cập nhật bên ngoài. Kỹ sư không nên bị kéo vào cuộc họp trạng thái trong phản hồi tích cực.
- **Theo dõi phạm vi mở rộng.** P2 suy giảm 3 giờ trong giờ hành chính có thể cần phân loại lại P1. Đánh giá lại tại mỗi cập nhật trạng thái.
- **Ghi nhận mọi thứ.** Mọi quyết định, hành động, mốc thời gian. Phục vụ Đánh Giá Sau Sự Cố và xây dựng kiến thức tổ chức.

### Cho Ban Lãnh Đạo

- **Tin tưởng phân loại.** Ma trận tồn tại để nhân viên trực có thể đưa ra quyết định ưu tiên lúc 3 giờ sáng mà không cần gọi ban lãnh đạo. Nếu đội liên tục phân loại sai, sửa ma trận và đào tạo -- không thêm cửa phê duyệt.
- **Sự cố P3/P4 không cần sự chú ý của bạn.** Bộ máy phòng chỉ huy đầy đủ dành cho P1 và P2 có điều kiện. Leo thang quá mức gây kiệt sức đội và giảm giá trị tuyên bố Sự Cố Nghiêm Trọng.
- **Đánh Giá Sau Sự Cố là đầu tư, không phải chi phí.** Mỗi hành động RCA ngăn chặn sự cố tương lai tiết kiệm gấp bội thời gian đầu tư. Bảo vệ thời gian của đội để thực hiện đúng cách.

---

## Phụ Lục A: Thuật Ngữ

| Thuật ngữ | Định nghĩa |
|------|-----------|
| **MTTA** | Mean Time to Acknowledge -- thời gian từ phát hiện sự cố đến phản hồi đầu tiên của con người |
| **MTTR** | Mean Time to Resolve -- thời gian từ phát hiện đến khôi phục dịch vụ (kiểm soát) hoặc sửa nguyên nhân gốc hoàn toàn (giải quyết hoàn toàn) |
| **Kiểm soát (Containment)** | Dịch vụ khôi phục ở trạng thái sử dụng được, dù có thể suy giảm. Đã cầm máu. |
| **Giải quyết hoàn toàn (Full Resolution)** | Nguyên nhân gốc đã sửa, dữ liệu đã khắc phục, giám sát xác nhận ổn định. Sự cố thực sự kết thúc. |
| **Phạm vi ảnh hưởng (Blast Radius)** | Phạm vi tác động: bao nhiêu người dùng, hợp đồng, giao dịch hoặc hệ thống bị ảnh hưởng |
| **IC** | Incident Commander -- điều phối phản hồi cho P1/P2. Quản lý con người và truyền thông, không phải debug kỹ thuật. |
| **Phòng chỉ huy (War Room)** | Kênh truyền thông chuyên dụng (Slack/Teams) cho phản hồi sự cố P1/P2 đang hoạt động. Nguồn thông tin duy nhất trong sự cố. |
| **Sự Cố Nghiêm Trọng (Major Incident)** | Sự cố kích hoạt cơ cấu phản hồi đầy đủ: IC, phòng chỉ huy, thông báo ban lãnh đạo, Đánh Giá Sau Sự Cố bắt buộc. Tất cả P1 và P2 đủ điều kiện. |
| **RCA** | Root Cause Analysis -- điều tra "tại sao" trong Đánh Giá Sau Sự Cố |
| **PII** | Personally Identifiable Information -- thông tin định danh cá nhân: tên, số CMND/CCCD, dữ liệu sức khỏe, hồ sơ tài chính, thông tin người thụ hưởng |
| **RPO** | Recovery Point Objective -- mức mất dữ liệu tối đa chấp nhận được tính theo thời gian (VD: RPO 1 giờ nghĩa là có thể mất tối đa 1 giờ dữ liệu) |
| **RTO** | Recovery Time Objective -- thời gian ngừng tối đa chấp nhận được trước khi dịch vụ phải được khôi phục |
| **SLI** | Service Level Indicator -- chỉ số đo lường sức khỏe dịch vụ (VD: tỷ lệ lỗi, latency P99) |
| **KB** | Knowledge Base -- thư viện kịch bản sự cố đã biết và phản hồi đã ghi nhận, xây dựng từ RCA |

---

## Phụ Lục B: Lịch Sử Phiên Bản

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---------|------|--------|--------|
| 1.0 | 2026-03-19 | tcl-ito | Ma trận phân loại toàn diện ban đầu |

---

## Phụ Lục C: Đánh Giá CIO và Góc Nhìn Kinh Doanh

> **Người đánh giá**: tcl-cio (Giám đốc Công nghệ Thông tin)
> **Ngày đánh giá**: 2026-03-19
> **Phạm vi**: Đánh giá toàn bộ incident-classify.md v1.0, đánh giá theo yêu cầu kinh doanh, nghĩa vụ pháp quy, trải nghiệm người dùng cuối và chiến lược.

---

### C.1 Kết Luận Đánh Giá

**PHÊ DUYỆT CÓ LƯU Ý**

Ma trận phân loại kỹ thuật rất vững chắc. Lưới danh mục-theo-ưu tiên rất toàn diện, quy tắc tự động nâng mức hợp lý, các kịch bản đặc thù bảo hiểm thực tế, và hướng dẫn phân loại lại thể hiện sự trưởng thành vận hành. Đây là bước tiến đáng kể so với ma trận mức độ nghiêm trọng đơn giản hơn trong `classification.md`.

Tuy nhiên, tài liệu được viết chủ yếu từ **góc nhìn vận hành kỹ thuật**. Để thực sự vận hành được cho công ty bảo hiểm nhân thọ, cần bổ sung từ góc nhìn **người dùng cuối, rủi ro kinh doanh và pháp quy**. Các phần sau cung cấp bổ sung đó.

**Điểm mạnh:**
- Ma trận 7 danh mục x 4 mức ưu tiên với chỉ báo cụ thể từng ô -- thực thi được, không lý thuyết
- Phân tầng hệ thống (Tier 1-3) là bổ sung xuất sắc trước đây thiếu trong classification.md
- Quy tắc tự động nâng mức (Phần 2) được hiệu chỉnh tốt cho vận hành bảo hiểm
- Hướng dẫn phân loại lại với ma trận thẩm quyền ngăn chặn cả phân loại quá cao và phân loại thấp nguy hiểm
- Kịch bản đặc thù bảo hiểm (Phần 8) kết nối trực tiếp giữa ITIL chung và thực tế bảo hiểm nhân thọ

**Lưu ý (chi tiết bên dưới):**
- H1: Thiếu mô tả tác động người dùng cuối -- đội vận hành cần hiểu trực quan mỗi mức ưu tiên có nghĩa gì với người thật
- H2: Thiếu định lượng rủi ro kinh doanh -- không có khung tác động tài chính, quyết định ưu tiên vẫn trừu tượng
- M1: Ma trận truyền thông có nhưng mỏng về thời gian và đối tượng cụ thể
- M2: Không có ngưỡng leo thang CIO/CTO/HĐQT rõ ràng từ phía kinh doanh

---

### C.2 Góc Nhìn Tác Động Người Dùng Cuối

Với mỗi mức ưu tiên, đây là trải nghiệm thực của con người. Đội vận hành phải thấm nhuần điều này -- sự cố không phải ticket trừu tượng; đó là một người không thể làm việc hoặc truy cập hợp đồng.

#### P1 -- Nghiêm Trọng: Người Dùng Trải Nghiệm Gì

| Bên liên quan | Trải nghiệm | Không thể làm gì |
|---|---|---|
| **Chủ hợp đồng** | Cổng hiển thị lỗi hoặc loading vô tận. Thanh toán thất bại. "Dịch vụ không khả dụng" trên app di động. Không có xác nhận nộp yêu cầu bồi thường. Không truy cập được tài liệu hợp đồng. Có thể nhận bảng sao kê hoặc thông báo phí sai. | Không thể đóng phí (nguy cơ mất hiệu lực). Không thể nộp hoặc theo dõi bồi thường. Không thể xem chi tiết hoặc tải tài liệu hợp đồng. Không thể cập nhật người thụ hưởng hoặc thông tin liên hệ. |
| **Sales / Kênh phân phối** | Hệ thống báo giá và nộp hồ sơ cốt lõi ngừng hoặc cho số sai. Không thể tạo minh họa. Không thể nộp kinh doanh mới. Sales tại chi nhánh có khách hàng đang chờ mà không có hệ thống phục vụ. | Không thể báo giá hợp đồng mới. Không thể nộp đơn. Không thể xử lý gia hạn. Không thể demo sản phẩm. Doanh thu dừng hoàn toàn. |
| **Nhân viên nội bộ** | Thẩm định viên không xử lý được đơn chờ. Cán bộ bồi thường không thể phê duyệt. Tài chính không chạy được phân bổ phí hoặc đối soát. Quản lý vận hành nhận tràn ngập cuộc gọi từ sales. | Không thể xử lý công việc phụ thuộc hệ thống bị ảnh hưởng. Giải pháp thủ công có thể không tồn tại cho chức năng cốt lõi như tính toán hoặc thanh toán. |

**Chi phí con người của P1**: Sales với khách hàng ngồi đối diện, sẵn sàng mua hợp đồng, phải nói "hệ thống đang lỗi, xin quay lại hôm khác." Chủ hợp đồng thanh toán phí thất bại lo lắng hợp đồng mất hiệu lực. Cán bộ bồi thường không thể chi trả quyền lợi tử vong cho gia đình đang đau buồn.

#### P2 -- Cao: Người Dùng Trải Nghiệm Gì

| Bên liên quan | Trải nghiệm | Không thể làm gì |
|---|---|---|
| **Chủ hợp đồng** | Một số chức năng bị lỗi -- đăng nhập được nhưng không thanh toán được. Cổng rất chậm. Một số trang hoạt động, một số không. App di động hoạt động một phần. | Không hoàn thành được giao dịch cụ thể. Trải nghiệm suy giảm. Có thể tìm giải pháp (gọi tổng đài, đến chi nhánh) nhưng bất tiện. |
| **Sales / Kênh phân phối** | Tính năng chính không khả dụng -- không tạo được minh họa cho một dòng sản phẩm, hoặc nộp kinh doanh mới chậm đến mức không dùng được trong giờ cao điểm. Các chức năng khác hoạt động. | Năng suất giảm nghiêm trọng. Một số sản phẩm hoặc kênh bị chặn. Sales có thể mất doanh số vì khách hàng không chờ. |
| **Nhân viên nội bộ** | Chức năng chính suy giảm -- batch thất bại cho một dòng sản phẩm, hoặc báo cáo sai một phần. Có giải pháp tạm thời nhưng tốn thời gian. Xử lý thủ công tăng rủi ro lỗi. | Không hoàn thành đầy đủ khối lượng công việc. Giải pháp thủ công tăng rủi ro lỗi. Có thể cần làm thêm giờ để xử lý tồn đọng khi hệ thống phục hồi. |

#### P3 -- Trung Bình: Người Dùng Trải Nghiệm Gì

| Bên liên quan | Trải nghiệm | Không thể làm gì |
|---|---|---|
| **Chủ hợp đồng** | Bất tiện nhỏ -- định dạng báo cáo sai, một trang tải chậm, tính năng không quan trọng không khả dụng. Giao dịch cốt lõi hoạt động. | Một hành động ít sử dụng không khả dụng. Có giải pháp tạm (VD: gọi tổng đài thay vì tự phục vụ cho một chức năng cụ thể). |
| **Sales / Kênh phân phối** | Lỗi hệ thống nhỏ. Vẫn bán hợp đồng và nộp đơn được. Một công cụ hỗ trợ không hoạt động (báo cáo hoa hồng, hiển thị danh sách khách hàng). | Không truy cập được một chức năng hỗ trợ. Quy trình bán hàng cốt lõi không bị ảnh hưởng. |
| **Nhân viên nội bộ** | Công cụ hoặc báo cáo không hoạt động đúng. Giải pháp tạm thời đơn giản. Tác động công việc hàng ngày hạn chế. | Một nhiệm vụ cụ thể cần giải pháp tạm. Không tác động xử lý quan trọng. |

#### P4 -- Thấp: Người Dùng Trải Nghiệm Gì

| Bên liên quan | Trải nghiệm | Không thể làm gì |
|---|---|---|
| **Chủ hợp đồng** | Có thể không nhận thấy. Vấn đề giao diện hoặc edge case ảnh hưởng rất ít người dùng. | Không có gì đáng kể. |
| **Sales / Kênh phân phối** | Vấn đề giao diện hoặc phiền toái nhỏ. Không ảnh hưởng khả năng bán hoặc phục vụ khách hàng. | Không có gì đáng kể. |
| **Nhân viên nội bộ** | Lỗi hiển thị hoặc định dạng nhỏ. Có thể không báo cáo trừ khi được hỏi. | Không có gì đáng kể. |

---

### C.3 Đánh Giá Rủi Ro Kinh Doanh

#### P1 -- Nghiêm Trọng: Rủi Ro Kinh Doanh

| Loại rủi ro | Mô tả | Tác động có thể định lượng |
|---|---|---|
| **Mất doanh thu** | Dừng bán hợp đồng. Thu phí thất bại. Xử lý gia hạn dừng. Mỗi giờ P1 trong giờ hành chính giảm trực tiếp thu nhập phí bảo hiểm. | Ước tính: tổng thu phí hàng ngày / giờ hành chính = doanh thu mỗi giờ bị đe dọa. Với công ty bảo hiểm cỡ vừa, có thể 500 triệu - 2 tỷ VND/giờ. |
| **Phạt pháp quy** | Khung pháp quy bảo hiểm Việt Nam yêu cầu báo cáo kịp thời, dữ liệu tài chính chính xác, và bảo vệ chủ hợp đồng. Ngừng hoạt động kéo dài, vi phạm dữ liệu, hoặc tính toán tài chính sai có thể kích hoạt chế tài, phạt, hoặc tăng cường giám sát. | Phạt khác nhau theo quy định. Tăng cường giám sát (kiểm toán bổ sung, yêu cầu báo cáo) có chi phí vận hành liên tục. |
| **Tổn hại uy tín** | Chủ hợp đồng không truy cập được dịch vụ mất niềm tin. Sales không bán được mất lòng tin vào nền tảng. Tin lan nhanh qua mạng lưới sales. Trên kênh số, mạng xã hội khuếch đại trải nghiệm tiêu cực. | Tỷ lệ rời bỏ khách hàng khó đo lường thời gian thực nhưng tích lũy. Sales mất doanh số do ngừng hệ thống sẽ nhớ khi thảo luận gia hạn hợp đồng. |
| **Vi phạm SLA với đối tác phân phối** | Đối tác bancassurance, thỏa thuận đại lý, và hợp đồng môi giới thường có cam kết khả dụng dịch vụ. Ngừng hoạt động kéo dài có thể kích hoạt phạt SLA hoặc cho đối tác cơ sở đàm phán lại. | Tùy hợp đồng cụ thể. Quan hệ bancassurance bị đe dọa nếu độ tin cậy nền tảng kém -- ngân hàng đối tác có thể giảm ưu tiên hoặc chuyển sang đối thủ. |
| **Quyền lợi chủ hợp đồng** | Nếu chủ hợp đồng không đóng phí do lỗi hệ thống và hợp đồng mất hiệu lực, công ty có thể có nghĩa vụ pháp lý khôi phục không phạt. Nếu yêu cầu bồi thường không nộp được trong cửa sổ quy định do hệ thống không khả dụng, công ty chịu rủi ro. | Chi phí pháp lý và tuân thủ. Tiềm ẩn khiếu nại cá nhân lên cơ quan quản lý. |
| **Sai lệch báo cáo tài chính** | Tính toán sai (phí, dự phòng, giá trị hoàn lại) không phát hiện có thể dẫn đến sai báo cáo tài chính, lỗi dự phòng actuarial, và báo cáo pháp quy sai. | Chi phí điều chỉnh. Phát hiện kiểm toán. Điều tra pháp quy. |

#### P2 -- Cao: Rủi Ro Kinh Doanh

| Loại rủi ro | Mô tả |
|---|---|
| **Mất doanh thu một phần** | Một kênh hoặc dòng sản phẩm bị ảnh hưởng. Tác động doanh thu thực nhưng có giới hạn. |
| **Suy giảm trải nghiệm khách hàng** | Khách hàng và sales có thể xử lý nhưng với ma sát. Điểm hài lòng giảm. |
| **Chi phí vận hành** | Làm thêm giờ nhân viên, giải pháp thủ công, sửa lỗi sau phục hồi. |
| **Vi phạm SLA** | SLA nội bộ với đơn vị kinh doanh có thể bị vi phạm. Ngưỡng SLA bên ngoài có thể bị tiệm cận. |
| **Tích lũy tồn đọng** | Xử lý bị chậm tạo hàng đợi phải giải quyết sau phục hồi, thường dưới áp lực thời gian (cuối tháng, hạn pháp quy). |

#### P3 -- Trung Bình: Rủi Ro Kinh Doanh

| Loại rủi ro | Mô tả |
|---|---|
| **Xói mòn chất lượng** | Sự cố P3 tái phát không được giải quyết báo hiệu vấn đề chất lượng hệ thống. |
| **Bức xúc nhân viên** | Giải pháp tạm thời kéo dài ngày hoặc tuần làm giảm năng suất và tinh thần. |
| **Leo thang ẩn** | P3 không được giải quyết có thể âm thầm trở thành P2 khi giải pháp tạm thời thất bại hoặc hạn chót đến gần. |

#### P4 -- Thấp: Rủi Ro Kinh Doanh

| Loại rủi ro | Mô tả |
|---|---|
| **Tín hiệu nợ kỹ thuật** | Vấn đề P4 tích lũy cho thấy thiếu đầu tư vào chất lượng. |
| **Tính chuyên nghiệp** | Lỗi giao diện trên hệ thống hướng khách hàng (cổng, bảng sao kê, tài liệu) phản ánh xấu thương hiệu công ty. |

---

### C.4 Yêu Cầu Truyền Thông -- Bổ Sung CIO

#### Ma Trận Truyền Thông Mở Rộng

| Mức ưu tiên | Đối tượng | Kênh | Thời gian | Nội dung | Chịu trách nhiệm |
|---|---|---|---|---|---|
| **P1** | Phòng chỉ huy điều hành (CTO, CIO, lãnh đạo kinh doanh) | Cuộc họp bridge / kênh phòng chỉ huy chuyên dụng | Trong **15 phút** sau tuyên bố P1 | Hệ thống bị ảnh hưởng, phạm vi tác động, thời gian kiểm soát ước tính, ai dẫn đầu phản hồi | Incident Commander |
| **P1** | Cơ quan quản lý (nếu đủ điều kiện) | Thông báo văn bản chính thức theo kênh pháp quy | Trong **24 giờ** (hoặc theo quy định cụ thể) | Bản chất sự cố, tác động đến chủ hợp đồng, trạng thái khắc phục, dự kiến giải quyết | Cán bộ tuân thủ |
| **P1** | Chủ hợp đồng / Khách hàng | Banner cổng, SMS (nếu ảnh hưởng hệ thống thanh toán), cập nhật script tổng đài | Trong **30 phút** | Điều gì bị ảnh hưởng, thời gian khôi phục dự kiến, kênh thay thế | IC + Marketing/Truyền thông |
| **P1** | Sales / Kênh phân phối | Hệ thống thông báo Sales, WhatsApp/Zalo broadcast, email | Trong **30 phút** | Điều gì ngừng, giải pháp tạm nếu có, khi nào cập nhật tiếp | IC + Quản lý kênh |
| **P1** | Đối tác phân phối (bancassurance, môi giới) | Liên hệ đối tác chuyên dụng, email, điện thoại | Trong **1 giờ** | Tác động đến vận hành đối tác, giải pháp tạm, dự kiến giải quyết | Quản lý kênh + IC |
| **P2** | Đơn vị kinh doanh bị ảnh hưởng | Email hoặc kênh Teams | Trong **1 giờ** | Điều gì bị ảnh hưởng, giải pháp tạm có, thời gian cập nhật tiếp | IC hoặc L1 cao cấp |
| **P2** | Sales (nếu hệ thống hướng sales bị ảnh hưởng) | Kênh thông báo Sales | Trong **1 giờ** | Điều gì bị ảnh hưởng, giải pháp tạm, dự kiến giải quyết | Quản lý kênh |

#### Các Lỗi Truyền Thông Cần Tránh

| Lỗi | Tại sao có hại | Thay vào đó |
|---|---|---|
| "Chúng tôi đang điều tra" không có follow-up | Các bên liên quan nghĩ bạn đã quên. Sales gọi trực tiếp CNTT, gây gián đoạn phản hồi. | Đặt thời gian cập nhật cụ thể và tuân thủ. |
| Thuật ngữ kỹ thuật trong truyền thông khách hàng/sales | "DB connection pool cạn kiệt" không có nghĩa gì với sales đang có khách chờ. | "Hệ thống hợp đồng tạm thời không khả dụng. Chúng tôi dự kiến khôi phục trong [thời gian]." |
| Không truyền thông cho đến khi giải quyết | Sự im lặng tệ hơn tin xấu. Mọi người giả định điều tồi tệ nhất. | Truyền thông sớm, ngay cả khi chưa có đầy đủ thông tin. |
| Đổ lỗi vendor trong truyền thông khách hàng | "Nhà cung cấp thanh toán đang gặp vấn đề" có thể đúng nhưng xói mòn niềm tin vào thương hiệu bạn. | "Chúng tôi nhận biết vấn đề với xử lý thanh toán và đang làm việc để giải quyết." Sở hữu dịch vụ. |
| Gửi chi tiết kỹ thuật cho đối tượng phi kỹ thuật | Gửi RCA kỹ thuật cho sales hoặc lãnh đạo. | Tùy chỉnh thông điệp theo đối tượng. Chi tiết kỹ thuật cho đội kỹ thuật. Tác động và timeline cho kinh doanh. |

---

### C.5 Khuyến Nghị KPI/SLA -- Góc Nhìn CIO

#### Mục Tiêu MTTA Hướng Tới

Chỉ tiêu SLA trong Phần 5 là mục tiêu hợp đồng -- tiêu chuẩn tối thiểu chấp nhận được. Từ góc nhìn CIO, mục tiêu vận hành hướng tới nên chặt hơn:

| Mức ưu tiên | Mục tiêu SLA (Phần 5) | Mục tiêu vận hành CIO | Lý do |
|---|---|---|---|
| **P1** | 15 phút | **< 10 phút** (24/7) | P1 không được xác nhận hơn 10 phút là lỗi quy trình. Với công ty bảo hiểm, mỗi phút P1 chưa xác nhận là khách hàng âm thầm thất bại giao dịch. 15 phút chấp nhận cho hợp đồng; 10 phút là mục tiêu vận hành. |
| **P2** | 30 phút | **< 15 phút** (giờ hành chính) | Sự cố P2 ảnh hưởng chức năng đáng kể. Trong giờ hành chính khi nhân viên sẵn sàng, 30 phút quá lâu cho xác nhận đầu tiên. |
| **P3** | 2 giờ làm việc | **< 1 giờ** (giờ hành chính) | Xác nhận nhanh cho người báo biết vấn đề đã được ghi nhận. Giữ SLA giải quyết 2 ngày làm việc nhưng siết xác nhận. |
| **P4** | Ngày làm việc tiếp theo | Không thay đổi | Mục tiêu hiện tại phù hợp. |

#### Cơ Quan Quản Lý và Kiểm Toán Sẽ Hỏi Gì

Cơ quan quản lý không hỏi MTTR trừu tượng. Họ hỏi câu hỏi cụ thể mà khung KPI phải trả lời:

1. "Dịch vụ chủ hợp đồng không khả dụng bao lâu trong sự cố này?" -- Ánh xạ MTTR kiểm soát.
2. "Khi nào phát hiện lỗi dữ liệu, và khi nào được sửa?" -- Ánh xạ MTTD (phát hiện) + MTTR.
3. "Làm sao đảm bảo không tái phát?" -- Ánh xạ hành động RCA và tỷ lệ hoàn thành.
4. "Thành tích của bạn?" -- Ánh xạ tuân thủ SLA và xu hướng khối lượng sự cố.
5. "Chủ hợp đồng bị ảnh hưởng có được thông báo không?" -- Ánh xạ yêu cầu truyền thông.

Xây dựng báo cáo để trả lời trực tiếp các câu hỏi này.

#### KPI Bổ Sung Cần Theo Dõi

| KPI | Định nghĩa | Tần suất báo cáo | Mục tiêu |
|---|---|---|---|
| **Phát hiện bởi giám sát vs Báo cáo bởi người dùng** | Tỷ lệ sự cố phát hiện bởi giám sát vs báo cáo bởi người dùng | Hàng quý (CIO) | > 70% phát hiện bởi giám sát. Đây là chỉ số trưởng thành vận hành quan trọng nhất. |
| **Tỷ lệ tái phát** | % sự cố có cùng nguyên nhân gốc với sự cố trước | Hàng quý (ban lãnh đạo) | < 15% -- đo lường hiệu quả RCA |
| **Tỷ lệ hoàn thành RCA** | % sự cố P1/P2 có RCA hoàn thành trong thời hạn cam kết | Hàng tháng (ban lãnh đạo) | 100% cho P1, > 90% cho P2 |
| **Tỷ lệ đóng hành động** | % hành động RCA hoàn thành trong thời hạn cam kết | Hàng quý (ban lãnh đạo) | > 80% -- dưới mức này, quy trình RCA chỉ là hình thức |
| **Số sự cố kích hoạt pháp quy** | Số sự cố kích hoạt thông báo pháp quy | Hàng quý (HĐQT) | Xu hướng: không hoặc giảm |

---

### C.6 Leo Thang Từ Phía Kinh Doanh

#### Ngưỡng CIO/CTO Tham Gia Trực Tiếp

Với tư cách CIO, tôi kỳ vọng tham gia trực tiếp (không chỉ được thông báo) khi:

1. **Bất kỳ sự cố P1 nào** -- không để quản lý vi mô phản hồi kỹ thuật, mà sẵn sàng cho quyết định điều hành: phân bổ tài nguyên, leo thang vendor, phê duyệt truyền thông khách hàng, quyết định thông báo pháp quy.
2. **Bất kỳ sự cố an ninh liên quan dữ liệu chủ hợp đồng** -- bất kể phân loại ưu tiên ban đầu. Hệ quả pháp quy và uy tín yêu cầu giám sát điều hành từ đầu.
3. **Bất kỳ sự cố chưa kiểm soát trong 4 giờ** -- bất kể mức ưu tiên ban đầu. Nếu không kiểm soát trong 4 giờ, có gì bất ngờ và phản hồi có thể cần tài nguyên bổ sung hoặc phương pháp khác.
4. **Bất kỳ sự cố được phân loại lại nâng mức** -- P3 trở thành P1 gợi ý phân loại ban đầu bỏ sót. Tôi cần hiểu tại sao.
5. **Nhiều sự cố P1/P2 đồng thời** -- tranh chấp tài nguyên cần ưu tiên hóa cấp điều hành.

#### Kích Hoạt Thông Báo HĐQT và Cơ Quan Quản Lý

| Kích hoạt | Thông báo | Thời hạn | Nội dung |
|---|---|---|---|
| Vi phạm dữ liệu đã xác nhận liên quan PII hoặc dữ liệu sức khỏe chủ hợp đồng | HĐQT (Ủy ban Kiểm toán), Cơ quan quản lý | HĐQT: trong 24 giờ. Cơ quan quản lý: theo yêu cầu pháp quy cụ thể (thường 24-72 giờ). | Bản chất vi phạm, số bản ghi, trạng thái kiểm soát, kế hoạch khắc phục, đánh giá rủi ro pháp lý. |
| Sai lệch báo cáo tài chính được phát hiện | HĐQT (Ủy ban Kiểm toán), Kiểm toán viên bên ngoài, Cơ quan quản lý (nếu dữ liệu đã nộp bị ảnh hưởng) | HĐQT: trong 48 giờ. Cơ quan quản lý: trước đợt nộp tiếp theo. | Phạm vi sai lệch, kỳ bị ảnh hưởng, nguyên nhân gốc, số liệu đã sửa, khắc phục kiểm soát. |
| Ngừng hoạt động kéo dài dịch vụ chủ hợp đồng cốt lõi (> 8 giờ) | HĐQT (nếu > 24 giờ), Cơ quan quản lý (theo yêu cầu pháp quy) | Cơ quan quản lý: trong 24 giờ. HĐQT: cuộc họp kế tiếp hoặc sớm hơn nếu > 24 giờ. | Thời lượng, tác động, nguyên nhân gốc, biện pháp phòng ngừa. |
| Chi trả sai cho/từ chủ hợp đồng | HĐQT (Ủy ban Kiểm toán), Cơ quan quản lý | Trong 48 giờ sau xác nhận | Số chủ hợp đồng bị ảnh hưởng, số tiền, kế hoạch khắc phục, kế hoạch thông báo khách hàng. |
| Ransomware hoặc tấn công mạng phá hoại | HĐQT (toàn bộ), Cơ quan quản lý, Cơ quan thực thi pháp luật (nếu áp dụng) | Trong 24 giờ | Vector tấn công, kiểm soát, đánh giá tác động dữ liệu, kế hoạch phục hồi, phối hợp thực thi pháp luật. |

---

### C.7 Quan Sát Chiến Lược và Khoảng Trống

#### KHOẢNG TRỐNG 1: Không Có Hệ Số Thời Gian Trong Ngày (CAO)

Ma trận hiện tại không tính đến khi nào sự cố xảy ra. P2 lúc 2 giờ chiều Thứ Ba (giờ cao điểm bán hàng, sales tại chi nhánh với khách hàng) khác biệt đáng kể so với cùng sự cố lúc 11 giờ tối Thứ Bảy. Khuyến nghị:
- **Giờ hành chính (T2-T7 8:00-18:00)**: Áp dụng mức ưu tiên chuẩn
- **Giờ cao điểm (T2-T6 9:00-12:00, 14:00-17:00)**: Xem xét nâng một mức nếu hệ thống hướng khách hàng bị ảnh hưởng
- **Ngoài giờ hành chính**: Xem xét hoãn P3/P4 đến ngày làm việc tiếp theo; P1/P2 vẫn yêu cầu phản hồi

#### KHOẢNG TRỐNG 2: Không Có Xem Xét Tác Động Tích Lũy (TRUNG BÌNH)

Ba sự cố P3 đồng thời trên các hệ thống khác nhau riêng lẻ không kích hoạt quy trình sự cố nghiêm trọng. Nhưng cùng nhau, có thể chỉ báo vấn đề hệ thống (triển khai lỗi, suy giảm hạ tầng) và tác động tích lũy đến người dùng có thể tương đương P2. Khuyến nghị: thêm quy tắc -- "3+ sự cố P3 đồng thời trên hệ thống liên quan trong 1 giờ nên được đánh giá là P2 tiềm ẩn."

#### KHOẢNG TRỐNG 3: Không Phân Biệt Sự Cố Dựa Trên Thời Gian vs Dựa Trên Dữ Liệu (CAO)

Ma trận hiện tại gộp chung hai loại sự cố khác nhau cơ bản:
- **Dựa trên thời gian**: Hệ thống ngừng. Tác động tăng tuyến tính theo thời gian. Kiểm soát = khôi phục dịch vụ.
- **Dựa trên dữ liệu**: Hệ thống cho dữ liệu sai. Tác động đã xảy ra. "Kiểm soát" nghĩa là dừng thiệt hại thêm, nhưng thiệt hại hiện tại phải được khắc phục.

Với công ty bảo hiểm nhân thọ, sự cố dựa trên dữ liệu thường nguy hiểm hơn ngừng hoạt động. Ngừng 2 giờ gây bất tiện. Hai tuần tính sai phí bảo hiểm âm thầm là sự kiện pháp quy.

#### KHOẢNG TRỐNG 4: Không Có Override Khuếch Đại Uy Tín (TRUNG BÌNH)

Sự cố thu hút chú ý mạng xã hội, truyền thông, hoặc khiếu nại công khai lên cơ quan quản lý có tác động vượt phạm vi kỹ thuật. P3 trở nên viral trên mạng xã hội vì khách hàng đăng bài không truy cập được tài liệu quyền lợi tử vong trở thành sự kiện uy tín P1. Khuyến nghị: thêm override uy tín vào kích hoạt phân loại lại Phần 9.

#### KHOẢNG TRỐNG 5: Cửa Sổ Xử Lý Batch Chưa Được Coi Trọng (TRUNG BÌNH)

Vận hành bảo hiểm nhân thọ phụ thuộc nặng vào batch (phân bổ phí, tính hoa hồng, báo cáo pháp quy, chuyển nhượng tái bảo hiểm). Lỡ batch phân bổ phí đêm nghĩa là đối soát tài chính ngày hôm sau sai, bảng sao kê hoa hồng sales bị chậm, và quy trình xuôi dòng lan truyền. Khuyến nghị: thêm vi phạm cửa sổ batch làm chỉ báo rõ ràng trong chỉ báo chung P2.

#### KHOẢNG TRỐNG 6: Không Có Phân Loại "Suýt Xảy Ra" (THẤP)

Cách tiếp cận hiện tại chỉ phân loại sự cố đã xảy ra. Không có phân loại cho sự kiện suýt tránh được -- triển khai lỗi bắt ở staging, quét an ninh tìm lỗ hổng trước khi bị khai thác. Báo cáo suýt xảy ra là dấu hiệu quản lý sự cố trưởng thành. Khuyến nghị: xem xét thêm cơ chế theo dõi suýt xảy ra vào knowledge base.

#### Điều Đội Vận Hành Có Thể Bỏ Sót

1. **Đồng hồ pháp quy bắt đầu từ phát hiện, không phải giải quyết.** Khi vấn đề dữ liệu được biết, công ty có thể có nghĩa vụ báo cáo dù nguyên nhân gốc vẫn đang điều tra. Đội vận hành không nên chờ RCA hoàn chỉnh trước khi liên hệ Tuân thủ.
2. **Hệ quả tái bảo hiểm.** Nếu dữ liệu sai được truyền cho nhà tái bảo hiểm, phải thông báo riêng. Dữ liệu chuyển nhượng sai có thể ảnh hưởng phạm vi tái bảo hiểm, tác động trực tiếp tỷ lệ an toàn vốn.
3. **Tác động dự phòng actuarial.** Dữ liệu hợp đồng sai đi vào tính toán dự phòng. "Sửa lỗi" với đội kỹ thuật có thể nghĩa là dự phòng công bố của công ty sai -- vấn đề cấp HĐQT và pháp quy.
4. **Tuân thủ cấp phép và sales.** Nếu sự cố ảnh hưởng hệ thống cấp phép sales, tính hoa hồng, hoặc báo cáo tuân thủ lực lượng bán hàng, hệ quả pháp quy mở rộng ra ngoài CNTT sang tuân thủ phân phối.
5. **Tương tác thời gian ân hạn phí.** Nếu hệ thống thanh toán phí ngừng và chủ hợp đồng không đóng phí được, chính sách thời gian ân hạn của công ty phát huy tác dụng. Đội pháp lý có thể cần gia hạn thời gian ân hạn cho chủ hợp đồng bị ảnh hưởng để tránh mất hiệu lực sai.

---

### C.8 Hệ Số Ưu Tiên Danh Mục -- Công Cụ Hỗ Trợ Quyết Định

Quy tắc tự động nâng mức trong Phần 2 được định nghĩa tốt. Để L1 có thể thực thi trong áp lực phân loại, khuyến nghị quy trình hỗ trợ quyết định sau mà L1 chạy sau khi phân loại ưu tiên ban đầu từ `classification.md`:

```
SAU KHI PHÂN LOẠI ƯU TIÊN BAN ĐẦU (từ cây quyết định classification.md)
         |
         v
Danh mục SEC với dữ liệu khách hàng bị đe dọa?    --> CÓ --> Override thành P1
         |
       KHÔNG
         |
         v
Tính toán/dữ liệu tài chính bị ảnh hưởng?          --> CÓ --> Sàn P2
         |                                                  (P1 nếu phạm vi > 100 hợp đồng)
       KHÔNG
         |
         v
Hạn pháp quy trong 72 giờ?                          --> CÓ --> Nâng một mức
         |
       KHÔNG
         |
         v
Đang trong giờ cao điểm VÀ                           --> CÓ --> Xem xét nâng một mức
hệ thống hướng khách hàng bị ảnh hưởng?
         |
       KHÔNG
         |
         v
3+ sự cố liên quan mở trong 1 giờ?                  --> CÓ --> Đánh giá là P2 tiềm ẩn
         |
       KHÔNG
         |
         v
Giữ phân loại ưu tiên ban đầu.
```

Quy trình này mất 60 giây để chạy qua và ngăn các lỗi phân loại thấp phổ biến nhất.

---

### C.9 Khuyến Nghị Triển Khai

#### Cho Đội Vận Hành

1. **In Công Cụ Hỗ Trợ Quyết Định (C.8)** và đưa vào checklist phân loại L1 cùng với checklist trong `classification.md`.
2. **Thực hiện bài tập tabletop sử dụng Kịch bản 5** từ `scenarios.md` (sai lệch dữ liệu cuối tháng). Bài tập này khai thác mọi yếu tố của phân loại -- sự cố dựa trên dữ liệu, áp lực hạn pháp quy, tác động tài chính, phối hợp liên chức năng, và kích hoạt P1 không rõ ràng từ góc nhìn kỹ thuật.
3. **Không để xảy ra gaming MTTA.** Nếu đội bắt đầu tự động xác nhận sự cố mà không thực sự xem xét để đạt mục tiêu MTTA 10 phút, chỉ số vô nghĩa. MTTA nghĩa là con người đã đọc ticket, đánh giá danh mục, và bắt đầu phân loại hoặc leo thang.
4. **Xem xét phân loại ưu tiên hàng tháng.** Nếu > 20% sự cố là P1, đội đang phân loại quá cao. Nếu < 5% sự cố P3/P4 bị phân loại lại nâng mức, chất lượng phân loại ban đầu tốt. Nếu > 15% bị phân loại lại nâng mức, chất lượng phân loại cần cải thiện.

#### Cho Ban Lãnh Đạo

1. **Đầu tư vào KPI tỷ lệ giám sát-phát hiện.** Chỉ số quan trọng nhất cho trưởng thành vận hành là tỷ lệ sự cố được giám sát phát hiện trước khi khách hàng báo cáo. Đầu tư vào giám sát cho đến khi tỷ lệ này vượt 70%.
2. **Bắt buộc đóng hành động RCA.** RCA có hành động mở sau 90 ngày không phải RCA -- đó là tài liệu. Nếu hành động không được đóng, hoặc hành động không thực tế hoặc đội thiếu năng lực. Cả hai đều cần can thiệp ban lãnh đạo.
3. **Chuẩn bị mẫu thông báo HĐQT ngay.** Không soạn memo HĐQT trong khủng hoảng P1. Chuẩn bị sẵn mẫu: tóm tắt sự cố, tác động đến chủ hợp đồng, tác động tài chính, trạng thái thông báo pháp quy, nguyên nhân gốc, và biện pháp phòng ngừa.

---

### C.10 Các Mục Mở Cho Phiên Bản Tiếp Theo

| ID | Mức độ | Mục | Hành động cần thiết |
|---|---|---|---|
| CR-H1 | Cao | Thêm mô tả tác động người dùng cuối vào thân chính Phần 3.1-3.4 | Tích hợp nội dung C.2 vào cột Mô Tả Tác Động |
| CR-H2 | Cao | Thêm phân biệt sự cố dựa trên thời gian vs dữ liệu | Thêm ghi chú Phần 1 hoặc tạo Phần 1.4 |
| CR-M1 | Trung bình | Thêm xem xét nâng mức giờ cao điểm | Mở rộng bảng Giờ Hành Chính Phần 5 |
| CR-M2 | Trung bình | Thêm quy tắc tác động tích lũy | Thêm vào Phần 2 Quy Tắc Tự Động Nâng Mức |
| CR-M3 | Trung bình | Thêm override uy tín vào kích hoạt phân loại lại | Mở rộng Phần 9 Kích Hoạt Nâng Mức |
| CR-M4 | Trung bình | Thêm vi phạm cửa sổ batch làm chỉ báo P2 rõ ràng | Cập nhật Phần 3.2 Chỉ Báo Chung |
| CR-L1 | Thấp | Thêm khuyến nghị theo dõi suýt xảy ra | Ghi chú cho trưởng thành quy trình tương lai |

---

| Phiên bản | Ngày | Tác giả | Thay đổi |
|---------|------|--------|--------|
| 1.0 | 2026-03-19 | tcl-ito | Ma trận phân loại toàn diện ban đầu |
| 1.0-review | 2026-03-19 | tcl-cio | Đánh giá CIO: PHÊ DUYỆT CÓ LƯU Ý. Thêm Phụ Lục C với góc nhìn kinh doanh (tác động người dùng cuối, rủi ro kinh doanh, truyền thông, KPI/SLA, leo thang, khoảng trống chiến lược, hệ số danh mục). |

---

**Trạng thái đánh giá**: PHÊ DUYỆT CÓ LƯU Ý bởi tcl-cio (2026-03-19)
**Soạn bởi**: tcl-ito (Vận hành CNTT)
**Đánh giá bởi**: tcl-cio (CIO)
**Ngày**: 2026-03-19
