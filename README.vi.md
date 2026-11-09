# NTC Micro-Harness: Giao Thức Kỹ Thuật Nguyên Tử & Plugin `/ntc-*` (v2.1)

<p align="center">
  <strong>🌐 Ngôn ngữ / Language:</strong>
  <a href="README.md">🇺🇸 English</a> |
  <strong>🇻🇳 Tiếng Việt (Hiện tại)</strong>
</p>

[![CI Validation](https://github.com/chien5572/ntc-micro-harness/actions/workflows/validate.yml/badge.svg)](https://github.com/chien5572/ntc-micro-harness/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Protocol Version](https://img.shields.io/badge/NTC%20Plugin-v2.1.0-green.svg)](plugin.json)
[![Antigravity Ready](https://img.shields.io/badge/Google%20Antigravity-2.0%20%7C%20IDE%20%7C%20CLI%20(agy)-4285F4.svg)](plugin.json)
[![Compatible with](https://img.shields.io/badge/AI%20Agents-Claude%20Code%20%7C%20Cursor%20%7C%20Windsurf-orange.svg)](AGENTS.md)

**NTC Micro-Harness v2.1 (Plugin Edition)** là bộ khung kỷ luật kỹ thuật (Engineering Harness) kiêm **Plugin Slash Commands (`/ntc-*`)** chống trượt ngữ cảnh (zero-drift), tối ưu hóa token, được thiết kế chuyên biệt cho hệ sinh thái **Google Antigravity** (**Antigravity 2.0**, **Antigravity IDE**, **Antigravity CLI `agy`**) cũng như **Claude Code**, **Cursor**, và **Windsurf**.

Thay vì bắt bạn phải tự tay viết hàng chục trang đặc tả từ con số 0 hoặc để AI tự ý nhảy vào viết code chắp vá, lệch giao diện, **NTC Micro-Harness v2.1** dẫn dắt toàn bộ vòng đời dự án qua **6 Bước điều khiển bằng các lệnh `/ntc-*` trực quan**:
1. **Bước 1 (`/ntc-init`) — Kết nối Git Repo & Hỏi-Đáp tạo `PRD.md` + `ARCHITECTURE.md`:** Ngay khi khởi chạy, Agent hỏi **link Git Repo của dự án** (để khởi tạo `git init` và kết nối `git remote add origin <url>` trước khi làm bất cứ việc gì — có thể để trống nếu chỉ làm local) cùng **yêu cầu cơ bản**. Sau đó Agent đặt 3–5 câu hỏi làm rõ để cùng bạn hoàn thiện và sinh ra [`PRD.md`](docs/templates/prd-template.md) & [`ARCHITECTURE.md`](docs/templates/architecture-template.md).
2. **Bước 2 (`/ntc-prototype`) — Tạo & Tinh chỉnh UI Prototype từ `PRD` + `ARCHITECTURE` (nếu có UI):** Sinh các file HTML/CSS tương tác tự chứa (`docs/prototypes/<slug>/scr-<nn>-*.html`) có đủ 4 trạng thái (`default`, `loading`, `empty`, `error`) và neo `data-testid`, chỉnh sửa (`--revise`) cho đến khi bạn hài lòng và chốt (`--approve` → `APPROVED`).
3. **Bước 3 (`/ntc-spec`) — Chốt `SPEC.md` Tổng Quan & Gán AI Skills (`ai-skill-maps.md`):** Tổng hợp thành [`SPEC.md`](docs/templates/spec-template.md) tổng quan (kèm `system-roadmap.md` và `contract-registry.md`) để bạn xem và chốt. Ngay sau đó, dựa vào `SPEC.md`, Agent đề xuất và cài đặt các **AI Skills** tương ứng cho từng chức năng (module/service) vào `.agents/skills/` và lập file hướng dẫn sử dụng skills [`ai-skill-maps.md`](docs/templates/ai-skill-maps-template.md).
4. **Bước 4 (`/ntc-modules`) — Tạo SPEC Chi Tiết Từng Chức Năng & `STEP-by-STEP.md`:** Dựa theo `SPEC.md` tổng quan, các **Skills** trong `ai-skill-maps.md` và `UI Prototypes` đã chốt, Agent viết bản đặc tả chi tiết [`docs/modules-spec/<slug>.md`](docs/templates/module-spec-template.md) cho từng chức năng (module/service). Khi bạn duyệt (`--approve`), hệ thống tự động sinh sổ tay [`STEP-by-STEP.md`](docs/templates/step-by-step-template.md).
5. **Bước 5 (`/ntc-plan`) — Chia nhỏ WBS Cấp 4 Toàn Dự Án (Gate 4):** Sinh sẵn 100% Hồ sơ Pha (`docs/plans/active/<slug>/phase-<NN>-*.md`) với các Atomic Tasks cấp 4 cho mọi module trước khi viết bất kỳ dòng code nào.
6. **Bước 6 (`/ntc-run` / `"tiếp tục"`) — Thực thi Nguyên tử, Auto Git Commit, `/ntc-cr` & Khóa Đuôi `SYS` E2E (Gate 5):** Thực thi đúng **1 Lượt = 1 Atomic Task**, ép khớp **1:1 UI Prototype (`data-testid`)**, chạy test thực tế, **tự động `git commit` tạo điểm lui (rollback point) sau mỗi task**, hỗ trợ yêu cầu thay đổi giữa chừng qua **`/ntc-cr`** (`CR-<NN>`), và khóa đuôi bằng kiểm thử tích hợp Full-Stack E2E (**`/ntc-status --e2e`**).

---

## Mục Lục

1. [Hướng Dẫn Cài Đặt Plugin Cho Antigravity (2.0, IDE & CLI `agy`)](#1-hướng-dẫn-cài-đặt-plugin-cho-antigravity-20-ide--cli-agy)
   - [1.1 Cài đặt bằng Antigravity CLI (`agy`)](#11-cài-đặt-bằng-antigravity-cli-agy)
   - [1.2 Cài đặt Global Plugin 1 Lệnh cho Antigravity 2.0, IDE & CLI](#12-cài-đặt-global-plugin-1-lệnh-cho-antigravity-20-ide--cli)
   - [1.3 Cài đặt Đồng thời vào Dự án Hiện tại + Global Plugin (1-Liner)](#13-cài-đặt-đồng-thời-vào-dự-án-hiện-tại--global-plugin-1-liner)
   - [1.4 Cách Kích hoạt & Sử dụng trên Antigravity 2.0, IDE và CLI](#14-cách-kích-hoạt--sử-dụng-trên-antigravity-20-ide-và-cli)
2. [Bảng Tra Cứu Toàn Bộ Lệnh `/ntc-*` (Slash Commands) & Các Cờ (`--flags`)](#2-bảng-tra-cứu-toàn-bộ-lệnh-ntc--slash-commands--các-cờ---flags)
3. [Sơ Đồ Quy Trình 6 Bước Của Plugin NTC Micro-Harness v2.1](#3-sơ-đồ-quy-trình-6-bước-của-plugin-ntc-micro-harness-v21)
4. [Hướng Dẫn Thực Hành Chi Tiết Từng Bước (Bước 1 → Bước 6)](#4-hướng-dẫn-thực-hành-chi-tiết-từng-bước-bước-1--bước-6)
5. [Cơ Chế Khóa 5 Lớp Ép AI Tuân Thủ 100% UI Prototype](#5-cơ-chế-khóa-5-lớp-ép-ai-tuân-thủ-100-ui-prototype)
6. [Quản Lý Thay Đổi Giữa Chừng (`/ntc-cr`), Auto Git Commit & Khôi Phục Sự Cố](#6-quản-lý-thay-đổi-giữa-chừng-ntc-cr-auto-git-commit--khôi-phục-sự-cố)
7. [Kiểm Thử Tích Hợp Liên Module & Full-Stack E2E (`/ntc-status --e2e`)](#7-kiểm-thử-tích-hợp-liên-module--full-stack-e2e-ntc-status---e2e)
8. [Cấu Trúc Thư Mục & Bảng Quy Ước Định Danh](#8-cấu-trúc-thư-mục--bảng-quy-ước-định-danh)

---

## 1. Hướng Dẫn Cài Đặt Plugin Cho Antigravity (2.0, IDE & CLI `agy`)

Hệ sinh thái **Google Antigravity** (bao gồm **Antigravity 2.0 Desktop App**, **Antigravity IDE**, và **Antigravity CLI `agy`**) dùng chung thư mục cấu hình Global Plugin tại `~/.gemini/config/plugins/ntc-micro-harness` và cấu hình Workspace tại `<project-root>/.agents/`. Bạn chỉ cần cài đặt **1 lần** là cả 3 môi trường đều nhận diện đầy đủ bộ lệnh `/ntc-*`.

### 1.1 Cài đặt bằng Antigravity CLI (`agy`)

Nếu máy bạn đã cài đặt **Antigravity CLI (`agy`)**, chạy lệnh sau trong Terminal:

```bash
# Cài đặt trực tiếp plugin từ GitHub
agy plugin install https://github.com/chien5572/ntc-micro-harness.git

# Đảm bảo plugin được bật (enabled)
agy plugin enable ntc-micro-harness
```

---

### 1.2 Cài đặt Global Plugin 1 Lệnh cho Antigravity 2.0, IDE & CLI

Bạn có thể cài đặt trực tiếp gói `ntc-micro-harness` vào thư mục Global Plugin (`~/.gemini/config/plugins/ntc-micro-harness`) bằng `git clone` hoặc script `--plugin-only`:

#### 🪟 Windows (PowerShell / CMD)
```powershell
# Cách A: Dùng Git Clone trực tiếp vào thư mục Global Plugin của Antigravity
git clone https://github.com/chien5572/ntc-micro-harness.git "$HOME\.gemini\config\plugins\ntc-micro-harness"

# Cách B: Dùng PowerShell 1-Liner (Chỉ cài Global Plugin)
powershell -NoProfile -ExecutionPolicy Bypass -Command "& ([scriptblock]::Create((irm https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.ps1))) -PluginOnly"
```

#### 🍎 macOS / 🐧 Linux / WSL / Git Bash
```bash
# Cách A: Dùng Git Clone trực tiếp vào thư mục Global Plugin của Antigravity
git clone https://github.com/chien5572/ntc-micro-harness.git ~/.gemini/config/plugins/ntc-micro-harness

# Cách B: Dùng Bash 1-Liner (Chỉ cài Global Plugin)
curl -fsSL https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.sh | bash -s -- --plugin-only
```

> **Lưu ý:** Sau khi cài mới thư mục Global Plugin lần đầu, hãy **khởi động lại (Restart)** Antigravity 2.0 / Antigravity IDE / `agy` để hệ thống nạp manifest [`plugin.json`](plugin.json).

---

### 1.3 Cài đặt Đồng thời vào Dự án Hiện tại + Global Plugin (1-Liner)

Nếu bạn đang đứng tại thư mục dự án (`cd /duong-dan/du-an`) và muốn vừa cài **Global Plugin cho Antigravity (2.0, IDE, CLI)**, vừa khởi tạo luôn bộ khung thư mục (`AGENTS.md`, `docs/`, `scripts/validate_plans.py`, `.agents/skills/ntc-*/`) vào dự án đó, hãy chạy 1 dòng lệnh dưới đây:

#### 🪟 Windows PowerShell / PowerShell Core
```powershell
irm https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.ps1 | iex
```
*(Nếu muốn truyền sẵn link Git Repo của dự án ngay khi cài)*:
```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -TargetPath "." -RepoUrl "https://github.com/user/my-project.git"
```

#### 🪟 Windows Command Prompt (CMD)
```cmd
powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.ps1 | iex"
```

#### 🍎 macOS / 🐧 Linux / WSL / Git Bash
```bash
curl -fsSL https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.sh | bash
```

#### 🐍 Lệnh Python Đa Nền Tảng (Windows / macOS / Linux)
```bash
# Chạy từ xa bằng 1 dòng lệnh:
python -c "import urllib.request as u; exec(u.urlopen('https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.py').read().decode('utf-8'))"

# Hoặc chạy từ file install.py kèm kết nối Git Repo dự án:
python install.py --target . --repo https://github.com/user/my-project.git
```

---

### 1.4 Cách Kích hoạt & Sử dụng trên Antigravity 2.0, IDE và CLI

| Môi trường Antigravity | Cách kiểm tra & Quản lý Plugin | Cách gọi lệnh `/ntc-*` |
| :--- | :--- | :--- |
| **1. Antigravity 2.0 (Desktop App)** | Ở thanh bên trái (**Left-hand Sidebar**), bấm vào mục **Skills & Customizations** → tab **Plugins** để thấy thẻ **NTC Micro-Harness (Atomic Engineering v2.1)** kèm 3 nút gợi ý khởi đầu (`suggestedPrompts`). Bạn có thể bật/tắt (toggle) trực tiếp không cần restart. | Tại khung **Chat Canvas**, gõ dấu `/` để mở menu lệnh và chọn `/ntc-init`, `/ntc-prototype`, `/ntc-spec`, `/ntc-modules`, `/ntc-plan`, `/ntc-run`, `/ntc-cr`, `/ntc-status`. |
| **2. Antigravity IDE (VS Code-based)** | IDE tự động nạp cả Global Plugin (`~/.gemini/config/plugins/ntc-micro-harness`) lẫn Workspace Skills (`.agents/skills/ntc-*/`). | Mở bảng **Sidebar Chat** (chế độ **Agent Mode**), gõ `/ntc-init` hoặc `/ntc-run` (hoặc gõ `"tiếp tục"`). |
| **3. Antigravity CLI (`agy`)** | Mở terminal tại thư mục dự án và gõ `agy` để vào giao diện TUI. Có thể gõ `/help` để xem danh sách các lệnh `/` đã nạp. | Gõ trực tiếp `/ntc-init`, `/ntc-prototype`, `/ntc-spec`, `/ntc-modules`, `/ntc-plan`, `/ntc-run`, `/ntc-cr`, `/ntc-status` ngay trong khung nhắc của `agy`. |

---

## 2. Bảng Tra Cứu Toàn Bộ Lệnh `/ntc-*` (Slash Commands) & Các Cờ (`--flags`)

| Bước | Lệnh `/ntc-*` | Các Cờ (`--flags`) Hỗ Trợ | Khi Nào Sử Dụng? | Cách Sử Dụng & Hành Động Của Agent |
| :--- | :--- | :--- | :--- | :--- |
| **Bước 1** | **`/ntc-init`** | `--repo <git-url>` *(tùy chọn)*<br>`--idea "<mô tả>"`<br>`--no-ui`<br>`--approve` | Ngay khi bắt đầu dự án mới hoặc áp dụng Harness vào repo hiện có. | 1. **Hỏi link Git Repo dự án trước tiên** (có thể để trống) → Khởi tạo `git init` & kết nối `git remote add origin <url>` trước khi làm bất cứ việc gì.<br>2. Đọc yêu cầu cơ bản → Đặt 3–5 câu hỏi ngắn để làm rõ nghiệp vụ & kiến trúc.<br>3. Sinh [`PRD.md`](docs/templates/prd-template.md) và [`ARCHITECTURE.md`](docs/templates/architecture-template.md) để bạn duyệt. |
| **Bước 2** | **`/ntc-prototype`** | `--screen <SCR-ID>`<br>`--revise "<góp ý>"`<br>`--approve` | Sau khi có `PRD.md` & `ARCHITECTURE.md` (nếu dự án có giao diện `UI Required: YES`). | 1. Dựa vào `PRD.md` & `ARCHITECTURE.md`, khóa Design Tokens trong [`docs/prototypes/registry.md`](docs/prototypes/registry.md) và tạo các bản HTML tương tác tại `docs/prototypes/<slug>/scr-<nn>-*.html` (đủ 4 trạng thái + `data-testid`).<br>2. Dùng `--revise "..."` để tinh chỉnh giao diện.<br>3. Dùng `--approve` để chốt (`APPROVED`) toàn bộ màn hình. |
| **Bước 3** | **`/ntc-spec`** | `--skills-from "<url>"`<br>`--approve` | Sau khi đã chốt UI Prototype (`APPROVED`) (hoặc ngay sau Bước 1 nếu `--no-ui`). | 1. Tạo [`SPEC.md`](docs/templates/spec-template.md) tổng quan, kèm danh sách module trong [`docs/plans/system-roadmap.md`](docs/plans/system-roadmap.md) và hợp đồng [`docs/plans/contract-registry.md`](docs/plans/contract-registry.md) để bạn chốt.<br>2. Dựa trên `SPEC.md`, đề xuất các **AI Skills** tương ứng cho từng chức năng (module/service).<br>3. Khi bạn duyệt (`--approve`): Cài đặt skills vào `.agents/skills/` và tạo file hướng dẫn sử dụng skills [`ai-skill-maps.md`](docs/templates/ai-skill-maps-template.md). |
| **Bước 4** | **`/ntc-modules`** | `--module <MOD>`<br>`--approve` | Sau khi đã chốt `SPEC.md` tổng quan và `ai-skill-maps.md`. | 1. Agent **đọc các Skills trong `ai-skill-maps.md`** của từng module, kết hợp với `SPEC.md` tổng quan và `UI Prototypes` đã chốt.<br>2. Viết đặc tả chi tiết [`docs/modules-spec/<slug>.md`](docs/templates/module-spec-template.md) cho từng chức năng (DDL Schema, API `CT-*`, màn hình `SCR-*`, State Machine, Given/When/Then, Chuỗi Pha `<MOD>-P<NN>`).<br>3. Khi bạn duyệt (`--approve`): Tự động sinh [`STEP-by-STEP.md`](docs/templates/step-by-step-template.md). |
| **Bước 5** | **`/ntc-plan`** | `--module <MOD>`<br>`--verify` | Sau khi đã duyệt toàn bộ `docs/modules-spec/*.md` (Gate 4). | 1. Sinh 100% Hồ sơ Pha (`docs/plans/active/<slug>/phase-<NN>-*.md`) cho tất cả các module.<br>2. Bóc tách tới **Atomic Task cấp 4 (`<MOD>-P<NN>.<M>.<A>`)**, gắn link `SCR-<MOD>-<NN>` và lệnh kiểm thử.<br>3. Chạy `python scripts/validate_plans.py --fix` đảm bảo `0 violations`. |
| **Bước 6** | **`/ntc-run`** *(hoặc gõ `"tiếp tục"`)* | `--module <MOD>`<br>`--phase <MOD>-P<NN>` | Trong suốt quá trình code dự án (Gate 5) cho đến khi hoàn thành. | 1. Đối soát 3-Step Crash Recovery từ `git status` / `HEAD`.<br>2. Thực thi **đúng 1 Atomic Task** (`1 Turn = 1 Task`), kích hoạt Skill trong `ai-skill-maps.md`, port **1:1 UI Prototype (`data-testid`)**.<br>3. Chạy test thực tế → tích `[x]` → cập nhật `🎫 Resume Ticket` → chạy `validate_plans.py --fix` → **Tự động `git commit` tạo điểm lui an toàn**. |
| **Thay đổi (CR)** | **`/ntc-cr`** | `"<mô tả thay đổi>"`<br>`--approve-delta` | Bất cứ lúc nào ở Bước 5/6 khi muốn thêm tính năng mới, sửa API hoặc thêm màn hình mới. | Kích hoạt **Giao thức Mở khóa ngược Delta 4 bước (`CR-<NN>`)**:<br>1. Ghi log `CR-<NN>` vào `system-roadmap.md` & khoanh vùng ảnh hưởng.<br>2. Cập nhật chỉ phần Prototype (`SCR-*`) / Hợp đồng (`CT-*`) thay đổi.<br>3. Bổ sung Delta vào `SPEC.md` & `docs/modules-spec/<slug>.md`.<br>4. Nối thêm Delta Tasks/Phase Dossier mới (không sửa lịch sử đã `[x]`) và quay lại `/ntc-run`. |
| **Kiểm tra & E2E** | **`/ntc-status`** | `--fix`<br>`--e2e` | Khi muốn xem tiến độ, đồng bộ bảng trạng thái, hoặc chạy pha khóa đuôi `SYS-P<FINAL>`. | - Mặc định / `--fix`: Chạy `python scripts/validate_plans.py --fix` và in bảng tiến độ toàn dự án.<br>- `--e2e`: Kích hoạt Pha đóng dự án (`SYS-P<FINAL>`) chạy tích hợp thật liên module (`CT-*`) và Full-Stack UI E2E (`SCR-*`). |

---

## 3. Sơ Đồ Quy Trình 6 Bước Của Plugin NTC Micro-Harness v2.1

```mermaid
flowchart TD
    S1["1️⃣ Bước 1: /ntc-init<br/>Hỏi Git Repo (kết nối origin) + Yêu cầu cơ bản<br/>↔ Agent hỏi làm rõ → Sinh PRD.md & ARCHITECTURE.md"]
    S2["2️⃣ Bước 2: /ntc-prototype<br/>Tạo & chỉnh sửa HTML UI Prototype từ PRD + ARCH<br/>👉 Duyệt --approve (Khóa SCR-MOD-NN)"]
    S3["3️⃣ Bước 3: /ntc-spec<br/>Chốt SPEC.md tổng quan + Roadmap + Contracts<br/>👉 Đề xuất & cài Skills → Tạo ai-skill-maps.md"]
    S4["4️⃣ Bước 4: /ntc-modules<br/>Đọc SPEC.md + ai-skill-maps.md + Prototypes<br/>👉 Tạo docs/modules-spec/*.md chi tiết & STEP-by-STEP.md"]
    S5["5️⃣ Bước 5: /ntc-plan (Gate 4)<br/>Sinh 100% Phase Dossiers & WBS cấp 4<br/>👉 docs/plans/active/* & validate_plans.py = PASS"]
    S6["6️⃣ Bước 6: /ntc-run / 'tiếp tục' (Gate 5)<br/>1 Turn = 1 Atomic Task + 1:1 UI + Test + Auto Git Commit<br/>👉 Khóa đuôi /ntc-status --e2e (SYS-P-FINAL)"]
    CR["🔄 /ntc-cr 'yêu cầu mới'<br/>Mở khóa ngược Delta 4 bước (CR-NN)<br/>chỉ cập nhật phần thay đổi"]

    S1 --> S2
    S1 -- "--no-ui (Không có UI)" --> S3
    S2 -- "Chốt UI (APPROVED)" --> S3
    S3 -- "Chốt SPEC & Skills" --> S4
    S4 -- "Duyệt Module Specs" --> S5
    S5 -- "0 Violations" --> S6
    S6 -. "Phát sinh tính năng mới" .-> CR
    CR -. "Cập nhật Delta Prototype/Spec/WBS" .-> S6
```

---

## 4. Hướng Dẫn Thực Hành Chi Tiết Từng Bước (Bước 1 → Bước 6)

### Bước 1: Kết nối Git Repo, Điền yêu cầu cơ bản & Hỏi-Đáp tạo `PRD.md` + `ARCHITECTURE.md` (`/ntc-init`)
Trong khung chat của **Antigravity 2.0**, **Antigravity IDE** hoặc **Antigravity CLI (`agy`)**, nhập:
```text
/ntc-init
```
*(Hoặc truyền trực tiếp: `/ntc-init --repo https://github.com/user/shop.git --idea "Hệ thống quản lý đơn hàng đa chi nhánh có Web Portal"`)*

* **Việc Agent sẽ làm:**
  1. Nếu bạn chưa nhập link Git repo, Agent sẽ hỏi bạn đầu tiên: **"Link Git Repo của dự án (có thể để trống nếu chỉ làm local)"** và **"Yêu cầu cơ bản của dự án"**.
  2. Ngay khi bạn phản hồi, Agent chạy `git init` và kết nối `git remote add origin <repo-url>` **trước khi làm bất cứ việc gì khác**.
  3. Agent đưa ra **3–5 câu hỏi ngắn gọn** để bạn làm rõ các điểm khuyết (phân quyền người dùng, luồng nghiệp vụ chính, công nghệ/DB muốn dùng, có giao diện UI hay không).
  4. Từ câu trả lời của bạn, Agent tạo ra 2 file nền tảng tại gốc dự án: **`PRD.md`** và **`ARCHITECTURE.md`**.

---

### Bước 2: Tạo & Tinh chỉnh UI Prototype từ `PRD.md` và `ARCHITECTURE.md` (`/ntc-prototype`)
*(Bỏ qua nếu dự án không có giao diện `--no-ui`)*
```text
/ntc-prototype
```
* **Việc Agent sẽ làm:**
  1. Dựa vào `PRD.md` và `ARCHITECTURE.md`, khởi tạo bảng Design Tokens và danh mục màn hình `SCR-<MOD>-<NN>` trong `docs/prototypes/registry.md`.
  2. Sinh các file HTML/CSS tương tác tự chứa tại `docs/prototypes/<module-slug>/scr-<nn>-<slug>.html` có thanh chuyển đổi 4 trạng thái (`default`, `loading`, `empty`, `error`) và gắn đầy đủ neo `data-testid="scr-<nn>-..."`.
* **Chỉnh sửa cho đến khi hài lòng:**
  ```text
  /ntc-prototype --screen SCR-WEB-01 --revise "Đổi sidebar sang màu tối và thêm bộ lọc theo ngày"
  ```
* **Chốt giao diện:**
  ```text
  /ntc-prototype --approve
  ```

---

### Bước 3: Tạo `SPEC.md` Tổng Quan & Ánh Xạ AI Skills cho Từng Module (`/ntc-spec`)
```text
/ntc-spec
```
* **Việc Agent sẽ làm:**
  1. Kết hợp `PRD.md` + `ARCHITECTURE.md` + `UI Prototypes` đã chốt để tạo **`SPEC.md`** tổng quan, kèm bảng **Module Registry** trong `docs/plans/system-roadmap.md` và danh mục hợp đồng **`CT-*`** trong `docs/plans/contract-registry.md`.
  2. Dựa vào các chức năng (modules/services) trong `SPEC.md`, Agent đề xuất **danh sách các AI Skills** tương ứng cho từng module (bạn có thể truyền thêm nguồn tìm kiếm qua `/ntc-spec --skills-from "https://skillsmp.com/search"`).
* **Khi bạn xem và chốt:**
  ```text
  /ntc-spec --approve
  ```
  Agent cài đặt bộ skills vào `.agents/skills/<skill-name>/SKILL.md` và tạo file hướng dẫn sử dụng skills cho từng chức năng: **`ai-skill-maps.md`**.

---

### Bước 4: Tạo SPEC Chi Tiết cho Từng Chức Năng (Module/Service) (`/ntc-modules`)
```text
/ntc-modules
```
* **Việc Agent sẽ làm:**
  1. Đọc `SPEC.md` tổng quan + **đọc các Skills đã gán cho từng module trong `ai-skill-maps.md`** + `docs/prototypes/registry.md`.
  2. Tạo bản đặc tả chi tiết **`docs/modules-spec/<module-slug>.md`** cho từng chức năng (`system.md`, `auth.md`, `order.md`, `web.md`...) gồm đầy đủ DDL Database, API/Event Contracts `CT-*`, ánh xạ màn hình `SCR-*`, State Machine, Given/When/Then và chuỗi Phase `<MOD>-P<NN>`.
* **Khi bạn duyệt:**
  ```text
  /ntc-modules --approve
  ```
  Agent tự động sinh sổ tay điều hành **`STEP-by-STEP.md`** cho các bước tiếp theo.

---

### Bước 5: Sinh Toàn Bộ Hồ Sơ Pha & Bóc Tách WBS Cấp 4 (`/ntc-plan` — Gate 4)
```text
/ntc-plan
```
* **Việc Agent sẽ làm:**
  1. Khởi tạo 100% file Phase Dossiers tại `docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` cho toàn bộ các module trong dự án.
  2. Chia nhỏ từng Major Task thành các **Atomic Tasks cấp 4 (`<MOD>-P<NN>.<M>.<A>`)**:
     - `.1`: Định nghĩa Contract / Schema / DTO / Interface.
     - `.2`: Triển khai Logic nghiệp vụ hoặc UI Component (gắn rõ `UI Prototype Reference: SCR-<MOD>-<NN>`).
     - `.3`: Viết Unit / Component Test kiểm chứng thực tế.
  3. Chạy `python scripts/validate_plans.py --fix` đảm bảo `PASSED: 0 violations`.

---

### Bước 6: Thực Thi Nguyên Tử & Máy Trạng Thái `/ntc-run` / `"Tiếp tục"` (Gate 5)
Khi bắt đầu code hoặc tiếp tục công việc, bạn chỉ cần gõ:
```text
/ntc-run
```
*(Hoặc gõ tự nhiên bằng tiếng Việt: **`tiếp tục`**, **`tiếp tục <MOD>`**)*

* **Trong mỗi lượt chạy (`1 Turn = 1 Atomic Task`), Agent tự động:**
  1. Kiểm tra **3-Step Crash Recovery** từ `git status` / `HEAD`.
  2. Đọc Skill bắt buộc trong `ai-skill-maps.md` và (nếu là task UI) đọc file HTML Prototype `SCR-<MOD>-<NN>` để port **1:1 DOM + CSS + `data-testid`**.
  3. Viết code hoàn chỉnh (cấm viết `// TODO`) và chạy lệnh kiểm thử thực tế (`Executable Proof Command`).
  4. Đánh dấu `[x]`, cập nhật `🎫 Resume Ticket`, chạy `python scripts/validate_plans.py --fix`.
  5. **Tự động tạo Atomic Git Commit (`git commit -m "feat(<slug>): complete <MOD>-P<NN>.<M>.<A> - ..."`):** Biến `HEAD` thành điểm lui an toàn tuyệt đối!
* **Khi hoàn thành task cuối cùng của một Phase:** Agent tự động dừng cứng và nhắc bạn gõ:
  ```text
  /ntc-run --phase <MOD>-P02
  ```
  *(Hoặc `tiếp tục phase <MOD>-P02`)* để tự động chuyển `phase-01` sang `docs/plans/completed/`, kích hoạt `phase-02` và làm luôn task đầu tiên của `phase-02`.

---

## 5. Cơ Chế Khóa 5 Lớp Ép AI Tuân Thủ 100% UI Prototype

1. **Lớp 1 — Khóa Sổ đăng ký & Design Tokens (`docs/prototypes/registry.md`):** Mọi màn hình đều có mã `SCR-<MOD>-<NN>` và bảng màu/typography cố định ngay từ Bước 2 (`/ntc-prototype`).
2. **Lớp 2 — Khóa Neo Kiểm thử `data-testid`:** Mọi phần tử quan trọng trong file `.html` prototype bắt buộc gắn `data-testid="scr-<nn>-<element>"`.
3. **Lớp 3 — Khóa Kiểm tra Tự động (`scripts/validate_plans.py`):** Chặn cứng nếu màn hình còn ở trạng thái `DRAFT`, thiếu file `.html` trên ổ đĩa, hoặc trong file `.html` không có `data-testid=`.
4. **Lớp 4 — Khóa Quy tắc 1:1 trong `AGENTS.md` & Skill `ui-prototype-fidelity`:** Bắt buộc Agent `read_file` bản HTML prototype ngay trong lượt code để chuyển đổi 1:1 vào React/Vue/Next.js/Blade/Flutter.
5. **Lớp 5 — Khóa Kiểm thử Component (Task `.3`) & Full-Stack E2E (`SYS-P<FINAL>`):** Bài test bắt buộc truy vấn đúng các neo `getByTestId('scr-...')` đã khóa.

---

## 6. Quản Lý Thay Đổi Giữa Chừng (`/ntc-cr`), Auto Git Commit & Khôi Phục Sự Cố

### 6.1 Khi muốn thêm tính năng / thêm màn hình mới ở giữa Bước 5 hoặc Bước 6 (`/ntc-cr`)
Chỉ cần gõ:
```text
/ntc-cr "Thêm màn hình Xuất báo cáo PDF và API thống kê doanh thu theo tháng"
```
*(Hoặc gõ: `yêu cầu thay đổi: Thêm màn hình Xuất báo cáo PDF...`)*

Agent sẽ chạy **Giao thức Mở khóa ngược Delta 4 bước (`CR-<NN>`)** mà **không bao giờ xóa hay làm hỏng các task `[x]` đã hoàn thành**:
1. **Bước 1:** Đăng ký mã `CR-01` vào `docs/plans/system-roadmap.md` (`## 6. Change Request (CR) Log`) và khoanh vùng ảnh hưởng.
2. **Bước 2:** Chỉ tạo/cập nhật file HTML Prototype (`SCR-*`) và Hợp đồng (`CT-*`) của phần thay đổi để bạn duyệt (`/ntc-cr --approve-delta`).
3. **Bước 3:** Nối thêm đặc tả Delta vào `SPEC.md`, `docs/modules-spec/<slug>.md`, và nối thêm Tasks vào hồ sơ pha đang mở (hoặc tạo hồ sơ Delta Phase mới `phase-<NN+1>-cr-01-*.md` nếu các pha cũ đã đóng).
4. **Bước 4:** Chạy `validate_plans.py --fix`, commit kế hoạch Delta và tiếp tục `/ntc-run`.

### 6.2 Auto Git Commit & Khôi phục sự cố 3 bước (3-Step Crash Recovery)
Nhờ việc mỗi Atomic Task `[x]` đều được `git commit` ngay cuối lượt chạy, mọi thay đổi chưa commit trong `git diff HEAD` đều thuộc 100% về đúng task đang chạy dở khi mất điện/tắt IDE. Khi bạn gõ `/ntc-run` hoặc `"tiếp tục"`, Agent tự động đối chiếu `HEAD` để viết nốt phần dở dang hoặc commit bù nếu code đã pass test.

---

## 7. Kiểm Thử Tích Hợp Liên Module & Full-Stack E2E (`/ntc-status --e2e`)

Khi tất cả các module thành phần (`AUTH`, `ORD`, `WEB`...) đã hoàn thành các phase riêng và chuyển vào `docs/plans/completed/`, bạn chạy lệnh:
```text
/ntc-status --e2e
```
Agent sẽ kích hoạt Pha đóng dự án **`SYS-P<FINAL>`** của module `SYS` (`system`) để:
1. Khởi chạy toàn bộ hệ thống thật (Database + Migrations + Backend Services + API Gateway + Frontend).
2. Kiểm thử tích hợp thật các hợp đồng liên module (`CT-*`) không dùng mock.
3. Chạy kịch bản E2E tự động (Playwright/Cypress) bấm trực tiếp vào các neo `data-testid="scr-<nn>-..."` từ Giao diện → gọi API → lưu Database → kiểm tra giao diện cập nhật đúng 4 trạng thái đã duyệt.

---

## 8. Cấu Trúc Thư Mục & Bảng Quy Ước Định Danh

```text
your-project/
├── plugin.json                                     # Manifest chuẩn Plugin cho Antigravity (2.0 / IDE / CLI)
├── PRD.md                                          # [Bước 1: /ntc-init] Tài liệu Yêu cầu Sản phẩm
├── ARCHITECTURE.md                                 # [Bước 1: /ntc-init] Bản thiết kế Kiến trúc & Topology
├── SPEC.md                                         # [Bước 3: /ntc-spec] Đặc tả Hệ thống Tổng quan Tối cao
├── ai-skill-maps.md                                # [Bước 3: /ntc-spec] Bản đồ Kỹ năng AI cho từng Module/Service
├── STEP-by-STEP.md                                 # [Bước 4: /ntc-modules] Sổ tay Hướng dẫn cho Người dùng (AI cấm đọc)
├── AGENTS.md                                       # Hợp đồng vận hành 6 bước bắt buộc cho AI Agent
├── rules/AGENTS.md                                 # Quy tắc tự động nạp khi bật Plugin
├── skills/                                         # Bộ 8 Slash Command Skills (/ntc-init .. /ntc-status)
├── .agents/skills/                                 # Các kỹ năng AI đã cài đặt cho dự án
├── docs/
│   ├── WORKFLOW.md                                 # Quy trình vận hành chi tiết 6 bước
│   ├── prototypes/                                 # [Bước 2: /ntc-prototype]
│   │   ├── registry.md                             # Sổ đăng ký UI Prototype & Design Tokens (SCR-<MOD>-<NN>)
│   │   └── <module-slug>/scr-<nn>-<slug>.html      # Các bản HTML/CSS Prototype tương tác có data-testid
│   ├── modules-spec/                               # [Bước 4: /ntc-modules]
│   │   ├── system.md                               # Đặc tả module SYS (Mở đầu hạ tầng & Khóa đuôi E2E)
│   │   └── <module-slug>.md                        # Đặc tả chi tiết từng Module + Bảng Chuỗi Pha (<MOD>-P<NN>)
│   ├── plans/
│   │   ├── system-roadmap.md                       # Lộ trình Dự án, Active Work Pointer & Nhật ký CR-<NN>
│   │   ├── contract-registry.md                    # Sổ đăng ký Hợp đồng Liên Module (CT-<PROVIDER>-<NN>)
│   │   ├── active/<module-slug>/phase-<NN>-*.md    # [Bước 5: /ntc-plan] Hồ sơ Pha & WBS cấp 4 + 🎫 Resume Ticket
│   │   └── completed/<module-slug>/phase-<NN>-*.md # [Bước 6: /ntc-run] Hồ sơ Pha đã nghiệm thu & lưu trữ
│   └── templates/                                  # Bộ mẫu tài liệu chuẩn (PRD, ARCH, SPEC, Prototype, Module, WBS)
└── scripts/
    └── validate_plans.py                           # Công cụ kiểm tra & tự động đồng bộ trạng thái (--fix)
```

---

## Giấy phép (License)

Phát hành theo giấy phép **MIT License**. Xem chi tiết tại file [`LICENSE`](LICENSE).
