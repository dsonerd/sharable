# TÀI LIỆU HƯỚNG DẪN QUẢN LÝ SỰ CỐ IT
## IT Incident Management Guidelines

**Phiên bản:** 1.0  
**Ngày ban hành:** 18/03/2026  
**Đơn vị:** Phòng IT Operations  
**Tham chiếu:** ITIL v4, Google SRE, ISO/IEC 20000-1

---

## MỤC LỤC
1. [Phân loại sự cố](#1-phân-loại-sự-cố)
2. [Hướng dẫn xử lý sự cố](#2-hướng-dẫn-xử-lý-sự-cố)
3. [Chuẩn hoá thông báo sự cố](#3-chuẩn-hoá-thông-báo-sự-cố)

---

# 1. PHÂN LOẠI SỰ CỐ

## 1.1 Phân loại theo Danh mục (Category)

| Mã | Danh mục | Mô tả | Ví dụ |
|----|----------|--------|-------|
| **HW** | Hardware | Lỗi phần cứng, thiết bị vật lý | Server hỏng, disk failure, nguồn điện |
| **SW** | Software / Application | Lỗi ứng dụng, phần mềm | App crash, bug nghiêm trọng, DB corruption |
| **NW** | Network | Lỗi mạng, kết nối | Mất kết nối, latency cao, DNS failure |
| **SEC** | Security | Sự cố bảo mật | Ransomware, data breach, DDoS, phishing |
| **CLD** | Cloud / Infrastructure | Lỗi hạ tầng cloud | AWS/Azure outage, container crash, scaling failure |
| **DB** | Database | Lỗi liên quan CSDL | Deadlock, replication lag, data loss |
| **ACC** | Access / Identity | Lỗi quyền truy cập, xác thực | SSO failure, AD outage, certificate expired |
| **OTH** | Khác | Không thuộc danh mục trên | Quy trình, con người, thảm hoạ |

## 1.2 Ma trận Ưu tiên (Priority Matrix)

Ưu tiên = **Impact × Urgency**

### Impact (Mức ảnh hưởng)

| Mức | Tên | Mô tả |
|-----|-----|--------|
| 1 | **Rộng (Extensive)** | Toàn bộ tổ chức / hệ thống lõi ngừng hoạt động |
| 2 | **Lớn (Significant)** | Nhiều phòng ban / nhóm người dùng bị ảnh hưởng |
| 3 | **Trung bình (Moderate)** | Một phòng ban / nhóm nhỏ bị ảnh hưởng |
| 4 | **Nhỏ (Minor)** | Cá nhân bị ảnh hưởng, có workaround |

### Urgency (Mức cấp bách)

| Mức | Tên | Mô tả |
|-----|-----|--------|
| 1 | **Rất cao (Critical)** | Dịch vụ ngừng hoàn toàn, không có workaround |
| 2 | **Cao (High)** | Dịch vụ suy giảm nghiêm trọng, workaround tạm |
| 3 | **Trung bình (Medium)** | Dịch vụ suy giảm nhẹ, workaround khả dụng |
| 4 | **Thấp (Low)** | Bất tiện nhưng không ảnh hưởng công việc |

### Priority Matrix

|  | Urgency 1 | Urgency 2 | Urgency 3 | Urgency 4 |
|--|-----------|-----------|-----------|-----------|
| **Impact 1** | **P1 – Critical** | **P1 – Critical** | **P2 – High** | **P3 – Medium** |
| **Impact 2** | **P1 – Critical** | **P2 – High** | **P2 – High** | **P3 – Medium** |
| **Impact 3** | **P2 – High** | **P3 – Medium** | **P3 – Medium** | **P4 – Low** |
| **Impact 4** | **P3 – Medium** | **P3 – Medium** | **P4 – Low** | **P4 – Low** |

## 1.3 SLA theo mức Priority

| Priority | Thời gian phản hồi | Thời gian xử lý (MTTR) | Escalation | Major Incident? |
|----------|-------------------|------------------------|------------|-----------------|
| **P1 – Critical** | ≤ 15 phút | ≤ 4 giờ | Ngay → L2/L3 + IM | ✅ Có |
| **P2 – High** | ≤ 30 phút | ≤ 8 giờ | 30 phút → L2 | Tuỳ đánh giá |
| **P3 – Medium** | ≤ 4 giờ | ≤ 24 giờ | 4 giờ → L2 | ❌ Không |
| **P4 – Low** | ≤ 8 giờ | ≤ 72 giờ | 24 giờ → L2 | ❌ Không |

## 1.4 Phân loại Major Incident

Một sự cố được xác định là **Major Incident** khi thoả **ít nhất 1** điều kiện:

| # | Tiêu chí |
|---|----------|
| 1 | Hệ thống core (Core Banking, Trading, CRM) ngừng hoạt động |
| 2 | Ảnh hưởng ≥ 30% người dùng hoặc ≥ 2 phòng ban |
| 3 | Rủi ro mất dữ liệu (data loss / data breach) |
| 4 | Sự cố bảo mật (active attack, ransomware, DDoS) |
| 5 | Vi phạm quy định pháp lý (regulatory compliance) |
| 6 | Ảnh hưởng doanh thu / giao dịch tài chính |
| 7 | Sự cố đã kéo dài > 1 giờ mà chưa xác định nguyên nhân |

---

# 2. HƯỚNG DẪN XỬ LÝ SỰ CỐ

## 2.1 Quy trình tổng quan

```
Phát hiện → Ghi nhận → Phân loại → Chẩn đoán → Escalation → Khắc phục → Xác nhận → Đóng ticket → Post-mortem
```

## 2.2 Chi tiết từng bước

### Bước 1 — Phát hiện & Báo cáo

| Kênh | Mô tả |
|------|--------|
| **Monitoring tự động** | Zabbix, Datadog, PagerDuty, CloudWatch alert |
| **Hotline IT** | Ext. 8888 hoặc +84-xxx-xxx-xxxx |
| **ITSM Portal** | ServiceNow / Jira Service Management |
| **Email** | it-support@company.com |
| **Chat** | Kênh #it-support trên Slack/Teams |

**Yêu cầu thông tin tối thiểu khi báo cáo:**
- Ai bị ảnh hưởng? (cá nhân / nhóm / toàn bộ)
- Hiện tượng cụ thể là gì?
- Khi nào bắt đầu xảy ra?
- Có thay đổi gì trước khi xảy ra không?
- Ảnh chụp màn hình / log (nếu có)

### Bước 2 — Ghi nhận Ticket

- **Tự động tạo** ticket trên ITSM từ alert hoặc portal
- **Bắt buộc điền:** Tiêu đề, mô tả, danh mục, người báo cáo, hệ thống ảnh hưởng
- **Mã ticket:** `INC-YYYYMMDD-XXXX` (VD: INC-20260318-0042)

### Bước 3 — Phân loại & Ưu tiên

1. Xác định **Category** (HW/SW/NW/SEC/CLD/DB/ACC/OTH)
2. Đánh giá **Impact** (1-4) và **Urgency** (1-4)
3. Tra **Priority Matrix** → P1/P2/P3/P4
4. Nếu thoả tiêu chí Major Incident → Kích hoạt quy trình MI

### Bước 4 — Chẩn đoán & Xử lý (3-Tier)

#### Tier 1 — Service Desk (L1)
| Hành động | Chi tiết |
|-----------|---------|
| Tra cứu Knowledge Base | Tìm giải pháp đã biết |
| Troubleshoot cơ bản | Restart service, clear cache, reset password |
| Áp dụng workaround | Giải pháp tạm nếu có trong KB |
| Thời gian giữ tại L1 | Tối đa **30 phút** trước khi escalate |

#### Tier 2 — Kỹ thuật (L2)
| Hành động | Chi tiết |
|-----------|---------|
| Phân tích log | Application log, system log, network trace |
| Reproduce lỗi | Tái hiện trên môi trường test |
| Root cause analysis | Xác định nguyên nhân gốc |
| Implement fix | Patch, config change, hotfix |
| Thời gian giữ tại L2 | Theo SLA của Priority |

#### Tier 3 — Chuyên gia / Vendor (L3)
| Hành động | Chi tiết |
|-----------|---------|
| Deep analysis | Code-level debug, hardware diagnostics |
| Vendor escalation | Mở ticket với nhà cung cấp (Oracle, Microsoft, AWS...) |
| Patch / Replace | Áp dụng patch chính thức, thay thế phần cứng |
| Custom development | Fix code nếu là lỗi nội bộ |

### Bước 5 — Change Management (nếu cần)

Nếu giải pháp yêu cầu thay đổi hệ thống production:

1. **Tạo RFC** (Request for Change) liên kết với ticket sự cố
2. **Emergency Change** cho P1/P2: Phê duyệt bởi Incident Manager + CAB Lead
3. **Standard Change** cho P3/P4: Theo quy trình Change Management thông thường
4. Ghi nhận change vào ticket sự cố

### Bước 6 — Xác nhận & Đóng Ticket

1. **Verify** dịch vụ đã khôi phục hoàn toàn
2. **Liên hệ người báo cáo** để xác nhận sự cố đã được giải quyết
3. **Cập nhật Knowledge Base** nếu có giải pháp mới
4. **Ghi nhận metrics:** Thời gian xử lý, root cause, resolution
5. **Đóng ticket** — Nếu người dùng không phản hồi trong 48h → auto-close

### Bước 7 — Post-Incident Review (PIR)

**Bắt buộc cho:** P1, P2, Major Incident  
**Tùy chọn cho:** P3 có root cause đáng chú ý

| Mục | Nội dung |
|-----|---------|
| **Timeline** | Sự kiện theo trình tự thời gian |
| **Root Cause** | Phân tích 5-Why hoặc Fishbone |
| **Impact** | Số user, thời gian downtime, thiệt hại |
| **What went well** | Điều làm tốt trong quá trình xử lý |
| **What could improve** | Điều cần cải thiện |
| **Action Items** | Hành động cụ thể + Owner + Deadline |

> **Nguyên tắc chính:** Blameless Post-Mortem — Tập trung vào hệ thống & quy trình, KHÔNG đổ lỗi cá nhân.

---

# 3. CHUẨN HOÁ THÔNG BÁO SỰ CỐ

## 3.1 Nguyên tắc chung

| Nguyên tắc | Mô tả |
|------------|--------|
| **Kịp thời** | Thông báo trong vòng 15 phút sau khi phát hiện (P1/P2) |
| **Chính xác** | Chỉ thông tin đã xác minh, không suy đoán |
| **Nhất quán** | Sử dụng template chuẩn |
| **Đúng đối tượng** | Theo ma trận thông báo bên dưới |
| **Cập nhật định kỳ** | P1: mỗi 30 phút / P2: mỗi 1 giờ / P3-P4: khi có tiến triển |

## 3.2 Ma trận thông báo (Notification Matrix)

| Đối tượng | P1 | P2 | P3 | P4 |
|-----------|----|----|----|----|
| Người dùng bị ảnh hưởng | ✅ | ✅ | ✅ | ✅ |
| Trưởng phòng IT | ✅ | ✅ | ❌ | ❌ |
| Incident Manager | ✅ | ✅ | ❌ | ❌ |
| CTO / CIO | ✅ | ⚠️ Nếu > 4h | ❌ | ❌ |
| CEO / Ban điều hành | ⚠️ Nếu > 8h hoặc data breach | ❌ | ❌ | ❌ |
| Các phòng ban liên quan | ✅ | ✅ | ⚠️ | ❌ |
| Khách hàng / Đối tác | ✅ Nếu external-facing | ⚠️ | ❌ | ❌ |

## 3.3 Kênh thông báo

| Priority | Kênh chính | Kênh phụ |
|----------|-----------|---------|
| **P1** | 📞 Gọi điện + 💬 Slack/Teams #incident-war-room | 📧 Email |
| **P2** | 💬 Slack/Teams #it-incidents | 📧 Email |
| **P3** | 📧 Email | 💬 Slack/Teams #it-support |
| **P4** | 🎫 Cập nhật trên ticket ITSM | — |

## 3.4 Templates thông báo

### 📢 Template 1: Thông báo Sự cố Mới (Initial Notification)

```
══════════════════════════════════════════════════════
🔴 THÔNG BÁO SỰ CỐ — [Priority: P1/P2/P3/P4]
══════════════════════════════════════════════════════

📋 Mã ticket:      INC-YYYYMMDD-XXXX
📅 Thời gian phát hiện: DD/MM/YYYY HH:MM
🏷️ Danh mục:       [HW/SW/NW/SEC/CLD/DB/ACC]
⚡ Mức ưu tiên:    [P1-Critical / P2-High / P3-Medium / P4-Low]

📌 MÔ TẢ SỰ CỐ:
[Mô tả ngắn gọn hiện tượng, hệ thống bị ảnh hưởng]

👥 ẢNH HƯỞNG:
- Hệ thống: [Tên hệ thống / dịch vụ]
- Phạm vi: [Số user / phòng ban bị ảnh hưởng]
- Mức độ: [Ngừng hoàn toàn / Suy giảm / Gián đoạn từng lúc]

🔧 HÀNH ĐỘNG ĐANG THỰC HIỆN:
[Mô tả các bước đang xử lý]

👤 NGƯỜI PHỤ TRÁCH:
- Incident Owner: [Tên — Chức danh]
- Liên hệ: [SĐT / Ext.]

⏰ CẬP NHẬT TIẾP THEO: DD/MM/YYYY HH:MM
══════════════════════════════════════════════════════
```

### 🔄 Template 2: Cập nhật Tiến độ (Status Update)

```
══════════════════════════════════════════════════════
🟡 CẬP NHẬT SỰ CỐ #[Lần cập nhật: X]
══════════════════════════════════════════════════════

📋 Mã ticket:      INC-YYYYMMDD-XXXX
📅 Thời gian cập nhật: DD/MM/YYYY HH:MM
⏱️ Thời gian xử lý: [X giờ Y phút kể từ khi phát hiện]

📊 TRẠNG THÁI: [Đang điều tra / Đã xác định nguyên nhân / Đang khắc phục]

📝 TIẾN ĐỘ:
- [Mô tả những gì đã thực hiện]
- [Kết quả phân tích / phát hiện]

🎯 BƯỚC TIẾP THEO:
- [Hành động sẽ thực hiện]
- [Thời gian dự kiến]

⚠️ THAY ĐỔI (nếu có):
- Mức ưu tiên: [Giữ nguyên / Nâng / Hạ]
- Phạm vi ảnh hưởng: [Mở rộng / Thu hẹp / Không đổi]

⏰ CẬP NHẬT TIẾP THEO: DD/MM/YYYY HH:MM
══════════════════════════════════════════════════════
```

### ✅ Template 3: Thông báo Khắc phục (Resolution Notification)

```
══════════════════════════════════════════════════════
🟢 SỰ CỐ ĐÃ ĐƯỢC KHẮC PHỤC
══════════════════════════════════════════════════════

📋 Mã ticket:      INC-YYYYMMDD-XXXX
📅 Thời gian khắc phục: DD/MM/YYYY HH:MM
⏱️ Tổng thời gian xử lý: [X giờ Y phút]

✅ GIẢI PHÁP:
[Mô tả ngắn gọn giải pháp đã áp dụng]

📊 TÓM TẮT:
- Nguyên nhân: [Root cause ngắn gọn]
- Ảnh hưởng thực tế: [Số user / thời gian downtime]
- Dịch vụ: [Đã khôi phục hoàn toàn / Khôi phục một phần]

⚠️ LƯU Ý CHO NGƯỜI DÙNG:
[Hướng dẫn cần làm, ví dụ: refresh, clear cache, re-login...]

📞 Nếu sự cố tái diễn, liên hệ: [SĐT / Email / Portal]

══════════════════════════════════════════════════════
```

### 🚨 Template 4: Thông báo Major Incident (Dành cho Ban điều hành)

```
══════════════════════════════════════════════════════
🚨 MAJOR INCIDENT REPORT — EXECUTIVE SUMMARY
══════════════════════════════════════════════════════

📋 Mã ticket:      INC-YYYYMMDD-XXXX
📅 Thời gian:      DD/MM/YYYY HH:MM — DD/MM/YYYY HH:MM
⏱️ Downtime:       [Tổng thời gian]
🎯 Severity:       [P1 — Critical]

📌 TÓM TẮT 1 CÂU:
[Hệ thống A ngừng hoạt động X giờ do nguyên nhân B, 
 ảnh hưởng N người dùng]

💰 ẢNH HƯỞNG KINH DOANH:
- Doanh thu: [Ước tính thiệt hại / Không ảnh hưởng]
- Khách hàng: [Số khách hàng bị ảnh hưởng]
- SLA vi phạm: [Có / Không — chi tiết]
- Dữ liệu: [Mất mát / Toàn vẹn]

🔍 NGUYÊN NHÂN GỐC:
[Root cause analysis ngắn gọn]

✅ HÀNH ĐỘNG ĐÃ THỰC HIỆN:
1. [Bước 1]
2. [Bước 2]
3. [Bước 3]

🛡️ PHÒNG NGỪA TÁI DIỄN:
1. [Action item 1 — Owner — Deadline]
2. [Action item 2 — Owner — Deadline]
3. [Action item 3 — Owner — Deadline]

👤 Incident Commander: [Tên]
📄 Post-Mortem đầy đủ: [Link đến tài liệu PIR]

══════════════════════════════════════════════════════
```

---

## PHỤ LỤC

### A. Danh sách Vai trò & Trách nhiệm (RACI)

| Hoạt động | Service Desk (L1) | Kỹ thuật (L2) | Chuyên gia (L3) | Incident Manager | Quản lý |
|-----------|:--:|:--:|:--:|:--:|:--:|
| Tiếp nhận & ghi nhận | **R** | I | — | I | — |
| Phân loại & ưu tiên | **R** | C | — | **A** | — |
| Chẩn đoán L1 | **R** | — | — | I | — |
| Điều tra L2 | I | **R** | — | I | — |
| Xử lý L3 / Vendor | — | I | **R** | I | — |
| Major Incident Process | I | R | R | **A** | I |
| Thông báo stakeholders | R | — | — | **A** | I |
| Đóng ticket | **R** | C | — | **A** | — |
| Post-Mortem | I | **R** | R | **A** | I |

> **R** = Responsible · **A** = Accountable · **C** = Consulted · **I** = Informed

### B. Glossary

| Thuật ngữ | Định nghĩa |
|-----------|-----------|
| **Incident** | Sự gián đoạn ngoài kế hoạch hoặc suy giảm chất lượng dịch vụ IT |
| **Major Incident** | Sự cố có ảnh hưởng nghiêm trọng, yêu cầu quy trình xử lý đặc biệt |
| **MTTR** | Mean Time To Resolve — Thời gian trung bình để giải quyết sự cố |
| **MTTA** | Mean Time To Acknowledge — Thời gian phản hồi trung bình |
| **RFC** | Request for Change — Yêu cầu thay đổi |
| **PIR** | Post-Incident Review — Đánh giá sau sự cố |
| **KB** | Knowledge Base — Cơ sở tri thức |
| **IC** | Incident Commander — Chỉ huy sự cố |
| **War Room** | Phòng họp khẩn cấp (vật lý hoặc virtual bridge call) |
| **SLA** | Service Level Agreement — Cam kết chất lượng dịch vụ |
| **CAB** | Change Advisory Board — Hội đồng phê duyệt thay đổi |

---

*Tài liệu được biên soạn tham khảo ITIL v4 Framework, Google SRE Handbook, Meta Incident Response, ServiceNow Best Practices, và Amazon COE Process.*
