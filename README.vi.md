# NTC Micro Harness: Giao Thức Kỹ Thuật Nguyên Tử (Phiên Bản Microservices v2.0)

<p align="center">
  <strong>🌐 Ngôn ngữ / Language:</strong>
  <a href="README.md">🇺🇸 English</a> |
  <strong>🇻🇳 Tiếng Việt (Hiện tại)</strong>
</p>

[![CI Validation](https://github.com/chien5572/ntc-micro-harness/actions/workflows/validate.yml/badge.svg)](https://github.com/chien5572/ntc-micro-harness/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Protocol Version](https://img.shields.io/badge/Harness-v2.0.0-green.svg)](AGENTS.md)
[![Compatible with](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Windsurf-orange.svg)](AGENTS.md)

**NTC Micro Harness v2.0** là bộ khung kỷ luật kỹ thuật (Engineering Harness) chống trượt ngữ cảnh (zero-drift), tối ưu hóa token, được thiết kế chuyên biệt để lập trình cặp (pair-programming) và điều phối đa tác tử (multi-agent orchestration) với các AI Coding Agent hiện đại (**Google Antigravity**, **Anthropic Claude Code**, **Cursor**, **Windsurf**, và **Roo Code / Cline**).

Thay vì để AI tự ý nhảy vào viết code chắp vá hoặc tự chế giao diện lệch với ý đồ của bạn, **NTC Micro Harness v2.0** ép AI hoạt động như một **Kiến trúc sư Phần mềm Chính (Principal Software Architect)** thông qua quy trình **5 Cổng Kiểm Soát (5-Stage Gated Lifecycle)**:
1. **Chốt Giao diện bằng Prototype trước khi Spec & Code (nếu có UI):** Tạo các file HTML/CSS tương tác (`docs/prototypes/<slug>/scr-<nn>-*.html`) có đủ trạng thái và neo `data-testid` ngay tại **Gate 3.0** để bạn duyệt trực tiếp trên trình duyệt trước khi viết Spec và Code.
2. **Hoàn thiện Đặc tả Chi tiết & Bản đồ Kỹ năng AI:** Viết đặc tả chi tiết cho toàn bộ các module (`docs/modules-spec/`), tương tác tìm kiếm và cài đặt bộ kỹ năng AI (`ai-skill-maps.md`), đồng thời sinh sổ tay câu lệnh cho người dùng (`STEP-by-STEP.md`).
3. **Bóc tách WBS Toàn Dự Án Trước Khi Code:** Sinh sẵn toàn bộ hồ sơ pha (Phase Dossiers) và Atomic Tasks cho mọi module (`docs/plans/active/`) tại Gate 4.
4. **Thực thi Nguyên tử & Bảo toàn 1:1 Giao diện tại Gate 5:** Thực thi đúng **1 Lượt = 1 Atomic Task** kèm chuyển đổi 1:1 từ UI Prototype đã chốt, kiểm thử thực tế, **Khôi phục sự cố 3 bước (3-Step Crash Recovery)**, và chốt chặn chuyển phase an toàn bằng lệnh **`"tiếp tục"` / `"tiếp tục phase <MOD>-P<NN+1>"`**.

---

## Mục Lục

1. [Giới thiệu & Tại sao cần NTC Micro Harness v2.0?](#1-giới-thiệu--tại-sao-cần-ntc-micro-harness-v20)
2. [Kiến trúc Cốt lõi & Hệ thống Phân cấp Sự thật (Hierarchy of Truth)](#2-kiến-trúc-cốt-lõi--hệ-thống-phân-cấp-sự-thật-hierarchy-of-truth)
3. [Hướng dẫn Cài đặt 1 Lệnh Duy Nhất (Tất cả Môi trường)](#3-hướng-dẫn-cài-đặt-1-lệnh-duy-nhất-tất-cả-môi-trường)
   - [3.1 Windows PowerShell / PowerShell Core](#31-windows-powershell--powershell-core)
   - [3.2 Windows Command Prompt (CMD)](#32-windows-command-prompt-cmd)
   - [3.3 Linux / macOS / WSL / Git Bash](#33-linux--macos--wsl--git-bash)
   - [3.4 Lệnh Python Đa Nền Tảng (Mọi Hệ Điều Hành)](#34-lệnh-python-đa-nền-tảng-mọi-hệ-điều-hành)
   - [3.5 Tùy chọn Nâng cao & Các File Được Cài Đặt](#35-tùy-chọn-nâng-cao--các-file-được-cài-đặt)
4. [Quy trình Thực thi Từng Bước (Gate 1 → Gate 5)](#4-quy-trình-thực-thi-từng-bước-gate-1--gate-5)
   - [Bước 0: Khởi tạo `SPEC.md`](#bước-0-khởi-tạo-specmd)
   - [Gate 1: Tiếp nhận Đặc tả Gốc & Kiểm toán Kiến trúc](#gate-1-tiếp-nhận-đặc-tả-gốc--kiểm-toán-kiến-trúc)
   - [Gate 2: Lộ trình Hệ thống (`system-roadmap.md`) & Sổ đăng ký Hợp đồng (`contract-registry.md`)](#gate-2-lộ-trình-hệ-thống-system-roadmapmd--sổ-đăng-ký-hợp-đồng-contract-registrymd)
   - [Gate 3: UI Prototype (`3.0`), Đặc tả Module (`3.1`), `ai-skill-maps.md` (`3.2`), và `STEP-by-STEP.md` (`3.3`)](#gate-3-ui-prototype-30-đặc-tả-module-31-ai-skill-mapsmd-32-và-step-by-stepmd-33)
   - [Gate 4: Sinh trước Toàn bộ Hồ sơ Pha & WBS Nguyên tử cho Mọi Module](#gate-4-sinh-trước-toàn-bộ-hồ-sơ-pha--wbs-nguyên-tử-cho-mọi-module)
   - [Gate 5: Thực thi Nguyên tử, Bảo toàn 1:1 UI & Máy Trạng Thái `"Tiếp tục"`](#gate-5-thực-thi-nguyên-tử-bảo-toàn-11-ui--máy-trạng-thái-tiếp-tục)
5. [Cơ chế Khóa 5 Lớp Ép AI Tuân Thủ 100% UI Prototype](#5-cơ-chế-khóa-5-lớp-ép-ai-tuân-thủ-100-ui-prototype)
6. [Khôi phục Sự cố Giữa Chừng & Chạy Song Song Đa Agent (Git Worktree)](#6-khôi-phục-sự-cố-giữa-chừng--chạy-song-song-đa-agent-git-worktree)
   - [6.1 Khôi phục Sự cố Tắt Máy / Đóng App Giữa Chừng (3-Step Crash Recovery)](#61-khôi-phục-sự-cố-tắt-máy--đóng-app-giữa-chừng-3-step-crash-recovery)
   - [6.2 Chạy Song Song Nhiều AI Agent (Nhiều Tab hoặc Git Worktree)](#62-chạy-song-song-nhiều-ai-agent-nhiều-tab-hoặc-git-worktree)
7. [Kiểm tra Tự động & Đồng bộ Hóa (`validate_plans.py`)](#7-kiểm-tra-tự-động--đồng-bộ-hóa-validate_planspy)
8. [Cấu trúc Thư mục & Bảng Quy ước Định danh](#8-cấu-trúc-thư-mục--bảng-quy-ước-định-danh)

---

## 1. Giới thiệu & Tại sao cần NTC Micro Harness v2.0?

Khi xây dựng các dự án Full-stack hoặc hệ thống Microservices phức tạp, các AI Coding Agent thông thường rất dễ mắc 6 lỗi nghiêm trọng. **NTC Micro Harness v2.0** khắc phục triệt để cả 6 vấn đề này bằng cơ chế khóa cơ học:

| Điểm yếu của AI thông thường | Triệu chứng thực tế | Giải pháp của NTC Micro Harness v2.0 |
| :--- | :--- | :--- |
| **1. Vội vàng viết code khi chưa rõ thiết kế** | AI lao vào viết code ngay khi chưa có schema DB, state machine, edge cases và hợp đồng API giữa các module. | **Khóa Gate 1 → Gate 3:** Nghiêm cấm viết code sản phẩm cho đến khi hoàn tất `SPEC.md`, `system-roadmap.md`, `contract-registry.md`, và **toàn bộ** `docs/modules-spec/<slug>.md`. |
| **2. Tự chế giao diện (UI) lệch ý người dùng** | Khi code Frontend, AI tự suy diễn bố cục, đổi màu sắc, thiếu trạng thái loading/empty/error khiến phải đập đi sửa lại nhiều lần. | **Khóa UI Prototype tại Gate 3.0 & Bảo toàn 1:1 tại Gate 5:** Tạo sẵn các file HTML/CSS tương tác (`docs/prototypes/<slug>/scr-<nn>-*.html`) kèm neo `data-testid` để bạn duyệt trước. Sang Gate 5, AI bắt buộc bê nguyên 1:1 DOM, class và `data-testid` vào Component thật. |
| **3. Bỏ quên hoặc không dùng AI Skills** | AI không đọc các bộ kỹ năng (`.agents/skills/`) nên tự bịa ra các mẫu code thiếu nhất quán giữa các module. | **Gate 3.2 (`ai-skill-maps.md`):** AI dừng lại hỏi người dùng các trang web tìm skill, đề xuất danh sách skill để người dùng duyệt, cài đặt vào `.agents/skills/` và lập bảng ánh xạ bắt buộc trong `ai-skill-maps.md`. |
| **4. Xáo trộn ngữ cảnh giữa Lập kế hoạch & Code** | Vừa code vừa nghĩ kế hoạch làm loãng context window và đứt mạch làm việc của lập trình viên. | **Gate 4 Sinh trước toàn bộ Phase Dossiers:** Mọi phase của **tất cả các module** đều được bóc tách sẵn thành các Atomic Tasks trước khi bước vào Gate 5. |
| **5. Ôm đồm nhiều việc hoặc bắt gõ lệnh dài** | AI sửa 15 file cùng lúc đầy `// TODO`, hoặc bắt người dùng phải nhớ và gõ mã task dài dòng ở mỗi lượt. | **Máy trạng thái `"Tiếp tục"`:** Thực thi đúng `1 Lượt = 1 Atomic Task` kèm kiểm thử thực tế. Chỉ cần gõ `"tiếp tục"` để làm task kế tiếp; tự động dừng cứng khi hết phase và yêu cầu gõ `"tiếp tục phase <MOD>-P<NN+1>"` để chuyển phase. |
| **6. Mất trạng thái khi sập IDE / mất điện** | Đang chạy dở task thì tắt máy hoặc hôm sau mở lại, AI viết đè hoặc làm hỏng phần code đang viết dở. | **Write-Ahead `🎫 Resume Ticket` + Khôi phục 3 bước:** Tự động đối chiếu `git status` / `git diff` trên các file mục tiêu để viết tiếp phần còn thiếu hoặc tự đánh dấu `[x]` nếu code đã pass test. |

---

## 2. Kiến trúc Cốt lõi & Hệ thống Phân cấp Sự thật (Hierarchy of Truth)

Tài liệu trong dự án được phân tầng rõ ràng để AI chỉ cần nạp đúng phần ngữ cảnh cần thiết cho lượt chạy hiện tại:

```text
SPEC.md (Đặc tả Hệ thống Tối cao)
 ├─ AGENTS.md                                     Hợp đồng vận hành & Quy tắc kỷ luật bắt buộc cho AI
 ├─ docs/plans/system-roadmap.md                  Lộ trình Dự án (Global Phases, Module Registry, Active Work Pointer)
 ├─ docs/plans/contract-registry.md               Sổ đăng ký Hợp đồng Liên Module (CT-<PROVIDER>-<NN>)
 ├─ docs/prototypes/registry.md                   Sổ đăng ký Prototype Giao diện & Design Tokens (SCR-<MOD>-<NN>, nếu có UI)
 │   └─ docs/prototypes/<module-slug>/scr-*.html  File HTML/CSS Prototype tương tác đã duyệt (kèm neo data-testid)
 ├─ docs/modules-spec/<module-slug>.md            Đặc tả Chi tiết Module + Ánh xạ Màn hình UI + Bảng Chuỗi Pha (<MOD>-P<NN>)
 ├─ ai-skill-maps.md                              Bản đồ Kỹ năng AI của Dự án (.agents/skills/<skill>/SKILL.md)
 ├─ STEP-by-STEP.md                               Sổ tay Hướng dẫn dành riêng cho Người dùng (AI KHÔNG ĐƯỢC ĐỌC)
 └─ docs/plans/active/<module-slug>/
     ├─ phase-01-<slug>.md                        Hồ sơ Pha Đang Chạy (IN_PROGRESS + 🎫 Resume Ticket thời gian thực)
     └─ phase-02-<slug>.md                        Hồ sơ Pha Kế Tiếp đã sinh sẵn (PENDING)
         └─ Major Task (<MOD>-P<NN>.<M>)
             └─ Atomic Task (<MOD>-P<NN>.<M>.<A>) ──► 1 Lượt = 1 Task + Bảo toàn 1:1 UI Prototype + Bằng chứng chạy test
                 ("tiếp tục phase ...")           ──► Tự động lưu trữ sang docs/plans/completed/<module-slug>/
```

### Hệ thống Phân cấp Sự thật (Hierarchy of Truth)

Tài liệu cấp dưới **tuyệt đối không được mâu thuẫn** với tài liệu cấp trên. Nếu phát hiện xung đột, AI phải **DỪNG LẠI NGAY và hỏi Kiến trúc sư Con người**:

1. **`SPEC.md`** — Đặc tả hệ thống tối cao, phạm vi nghiệp vụ, yêu cầu giao diện (`UI Required: YES | NO`) và mục tiêu kiến trúc do con người định nghĩa.
2. **`AGENTS.md`** — Hợp đồng vận hành, ranh giới hành vi và quy tắc thực thi bắt buộc đối với AI.
3. **`docs/plans/system-roadmap.md`** — Lộ trình tổng thể của dự án: Danh mục Module, các Pha Toàn cục (`GP-<NN>`), đồ thị phụ thuộc, và **Con trỏ Công việc Hiện hành (Active Work Pointer)**.
4. **`docs/plans/contract-registry.md`** — Sổ đăng ký toàn bộ API, sự kiện (Event) và Schema dùng chung giữa các module (`CT-<MOD>-<NN>`).
5. **`docs/prototypes/registry.md` & `docs/prototypes/<module-slug>/scr-<nn>-*.html`** — Sổ đăng ký Hợp đồng Giao diện & Prototype (khi dự án có UI): khóa chặt Design Tokens (bảng màu, font chữ, khung layout), các trạng thái hiển thị (`default`, `loading`, `empty`, `error`) và các neo `data-testid` (`SCR-<MOD>-<NN>`) đã được bạn phê duyệt.
6. **`docs/modules-spec/<module-slug>.md`** — Đặc tả chi tiết từng module: phạm vi, user stories, schema DB/lưu trữ chi tiết, hợp đồng cung cấp/tiêu thụ, ánh xạ màn hình UI (`SCR-<MOD>-<NN>`), biểu đồ tuần tự/state machine, tiêu chí nghiệm thu Given/When/Then, mã lỗi, và **Chuỗi Pha của Module** (`<MOD>-P<NN>`).
7. **`ai-skill-maps.md`** — Bản đồ ánh xạ từng module và từng pha với các kỹ năng AI bắt buộc (`.agents/skills/<skill-name>/SKILL.md`).
8. **`docs/plans/active/<module-slug>/phase-<NN>-<slug>.md`** — Hồ sơ Pha được sinh sẵn chứa các Major Tasks, Atomic Tasks (WBS cấp 4), đường dẫn `UI Prototype Reference`, và `🎫 Resume Ticket`.
9. **`docs/plans/completed/<module-slug>/phase-<NN>-<slug>.md`** — Hồ sơ Pha đã hoàn thành và được lưu trữ (lịch sử kiểm toán bất biến).

> [!IMPORTANT]
> **Ranh giới Dành riêng cho Con người (`STEP-by-STEP.md`):** File `STEP-by-STEP.md` được sinh ra ở cuối Gate 3 **chỉ dành riêng cho bạn (Kiến trúc sư Con người)** đọc và copy câu lệnh. **AI Agent bị nghiêm cấm đọc file `STEP-by-STEP.md` trong suốt quá trình thực thi.**

---

## 3. Hướng dẫn Cài đặt 1 Lệnh Duy Nhất (Tất cả Môi trường)

Bạn chỉ cần **mở Terminal ngay tại thư mục dự án hiện tại của bạn** (dự án mới hoặc dự án đang có sẵn):

```bash
cd /duong-dan/toi/du-an-cua-ban
```

Sau đó **dán đúng 1 dòng lệnh** tương ứng với môi trường của bạn dưới đây. Lệnh sẽ tự động tải **NTC Micro Harness v2.0** từ GitHub về thư mục tạm, áp dụng bộ khung vào ngay thư mục dự án hiện tại (`.`), cấu hình quy tắc cho AI (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`) và tự động dọn sạch file tạm!

---

### 3.1 Windows PowerShell / PowerShell Core

Mở **PowerShell** ngay tại thư mục dự án và dán lệnh:

```powershell
irm https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.ps1 | iex
```

*(Hoặc nếu muốn dùng `git clone` trực tiếp trong PowerShell)*:
```powershell
git clone --depth 1 https://github.com/chien5572/ntc-micro-harness.git .ntc-tmp; & .\.ntc-tmp\install.ps1 -TargetPath .; Remove-Item -Recurse -Force .ntc-tmp
```

---

### 3.2 Windows Command Prompt (CMD)

Mở **CMD (`cmd.exe`)** ngay tại thư mục dự án và dán lệnh:

```cmd
powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.ps1 | iex"
```

*(Hoặc dùng `git` + `python` trong CMD)*:
```cmd
git clone --depth 1 https://github.com/chien5572/ntc-micro-harness.git .ntc-tmp && python .ntc-tmp\install.py --target . --agent all && rmdir /s /q .ntc-tmp
```

---

### 3.3 Linux / macOS / WSL / Git Bash

Mở terminal **Bash** hoặc **Zsh** ngay tại thư mục dự án và dán lệnh:

```bash
curl -fsSL https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.sh | bash
```

*(Hoặc nếu muốn dùng `git clone` trong Bash/Zsh)*:
```bash
git clone --depth 1 https://github.com/chien5572/ntc-micro-harness.git .ntc-tmp && bash .ntc-tmp/install.sh . && rm -rf .ntc-tmp
```

---

### 3.4 Lệnh Python Đa Nền Tảng (Mọi Hệ Điều Hành)

Nếu máy đã cài **Python 3.8+** (trên Windows, macOS, hoặc Linux), mở terminal tại thư mục dự án và dán:

```bash
python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/chien5572/ntc-micro-harness/main/install.py').read())"
```
*(Thay `python` bằng `python3` trên macOS/Linux nếu máy dùng lệnh `python3`).*

---

### 3.5 Tùy chọn Nâng cao & Các File Được Cài Đặt

**Cơ chế an toàn cho dự án đang có sẵn:**
- Nếu dự án của bạn đã có sẵn `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, hoặc `.windsurfrules`, bộ cài sẽ **nối thêm (append)** khối `<!-- HARNESS:BEGIN -->` vào cuối file mà không làm mất nội dung cũ của bạn.
- Tạo đầy đủ cấu trúc `docs/WORKFLOW.md`, `docs/prototypes/registry.md`, `docs/modules-spec/README.md`, `docs/plans/system-roadmap.md`, `docs/plans/contract-registry.md`, toàn bộ mẫu trong `docs/templates/`, và công cụ kiểm tra `scripts/validate_plans.py`.

Kiểm tra ngay sau khi cài đặt bằng lệnh:
```bash
python scripts/validate_plans.py
```

---

## 4. Quy trình Thực thi Từng Bước (Gate 1 → Gate 5)

```mermaid
flowchart LR
    S0["Bước 0<br/>Viết SPEC.md"] --> G1["Gate 1<br/>Đọc SPEC &<br/>Phân tích Kiến trúc"]
    G1 --> G2["Gate 2<br/>System Roadmap &<br/>Contract Registry"]
    G2 --> G3["Gate 3<br/>3.0 UI Prototypes (nếu có UI)<br/>3.1 Mọi Module SPECs<br/>3.2 ai-skill-maps.md<br/>3.3 STEP-by-STEP.md"]
    G3 --> G4["Gate 4<br/>Sinh trước TOÀN BỘ<br/>Phase Dossiers (WBS)"]
    G4 --> G5["Gate 5<br/>Code Nguyên Tử &<br/>1:1 UI Parity ('tiếp tục')"]
```

Thực hiện lần lượt từ Bước 0 đến Gate 5 như sau:

---

### Bước 0: Khởi tạo `SPEC.md`

Copy file mẫu đặc tả ra thư mục gốc của dự án và điền yêu cầu bài toán, công nghệ sử dụng, cờ giao diện (`UI Required: YES | NO`), và các luồng nghiệp vụ chính:

```bash
# Trên Linux / macOS / Git Bash
cp docs/templates/spec-template.md SPEC.md

# Trên Windows PowerShell
Copy-Item docs/templates/spec-template.md SPEC.md
```

---

### Gate 1: Tiếp nhận Đặc tả Gốc & Kiểm toán Kiến trúc

Mở AI Coding Agent (Antigravity, Claude Code, Cursor, Windsurf) và dán câu lệnh sau:

```text
Hãy đọc file `SPEC.md` và `AGENTS.md`.
Thực hiện Gate 1 (Root Specification Ingestion):
1. Phân tích kiến trúc hệ thống, ranh giới nghiệp vụ, phạm vi giao diện (`UI Required: YES | NO`) và các rủi ro kỹ thuật.
2. Đề xuất danh sách các Module / Microservices (kèm Mã Module 2-5 chữ in hoa, slug, quyền sở hữu dữ liệu và trách nhiệm — giữ mã `SYS` / `system` cho phần nền tảng dùng chung).
3. Nêu các câu hỏi cần làm rõ về nghiệp vụ hoặc luồng màn hình trước khi chuyển sang Gate 2.
QUY TẮC TUYỆT ĐỐI: KHÔNG viết bất kỳ dòng code sản phẩm nào ở bước này.
```

---

### Gate 2: Lộ trình Hệ thống (`system-roadmap.md`) & Sổ đăng ký Hợp đồng (`contract-registry.md`)

Sau khi trả lời các câu hỏi của AI và chốt danh sách module, bạn dán câu lệnh:

```text
Tôi đồng ý với đề xuất kiến trúc. Hãy chuyển sang Gate 2:
1. Điền đầy đủ `docs/plans/system-roadmap.md` (theo mẫu `docs/templates/system-roadmap-template.md`) gồm Architecture Blueprint, Module Registry (trỏ tới `docs/modules-spec/<slug>.md`), Global Phases (`GP-01`, `GP-02`...), Module Dependency Graph và Active Work Pointer.
2. Điền đầy đủ `docs/plans/contract-registry.md` (theo mẫu `docs/templates/contract-registry-template.md`) với toàn bộ các hợp đồng API/Event/Schema liên module (`CT-<PROVIDER>-<NN>`) ở trạng thái `DRAFT`.
3. Chạy `python scripts/validate_plans.py` để kiểm tra tính hợp lệ và dừng lại chờ tôi duyệt Gate 2.
```

---

### Gate 3: UI Prototype (`3.0`), Đặc tả Module (`3.1`), `ai-skill-maps.md` (`3.2`), và `STEP-by-STEP.md` (`3.3`)

Gate 3 gồm **4 bước con tuần tự** (`Bước 3.0` có điều kiện nếu dự án có giao diện người dùng → `3.1` → `3.2` → `3.3`):

#### Bước 3.0 (Có điều kiện — Bắt buộc nếu Dự án có Giao diện UI): Tạo & Chốt UI Prototype (`docs/prototypes/`)

- **Nếu dự án thuần Backend/CLI (`UI Required: NO`):** AI đánh dấu `> **UI Required:** NO` trong `docs/prototypes/registry.md` và chuyển thẳng sang **Bước 3.1**.
- **Nếu dự án có giao diện người dùng (`UI Required: YES`):** Trước khi viết bất kỳ file `docs/modules-spec/*.md` nào, hãy yêu cầu AI tạo Prototype tương tác để bạn duyệt giao diện trước:

```text
Tôi duyệt Gate 2. Hãy thực hiện Gate 3 - Bước 3.0 (Tạo & Chốt UI Prototype):
1. Điền `docs/prototypes/registry.md` (theo mẫu `docs/templates/ui-prototype-registry-template.md`) gồm Design System Tokens (bảng màu, font chữ, spacing, khung layout) và bảng danh mục màn hình (`SCR-<MOD>-<NN>`).
2. Tạo các file HTML/CSS prototype tương tác độc lập tại `docs/prototypes/<module-slug>/scr-<nn>-<slug>.html` cho từng màn hình để tôi mở xem trực tiếp trên trình duyệt.
3. Mỗi file `.html` BẮT BUỘC có đủ các trạng thái (`default`, `loading`, `empty`, `error`) và gắn thuộc tính `data-testid="scr-<nn>-<element>"` vào các vùng bố cục chính, form, input, nút bấm và bảng dữ liệu.
4. DỪNG LẠI để tôi mở xem các file HTML trên trình duyệt, yêu cầu chỉnh sửa nếu cần và chốt (`Status: APPROVED` trong `docs/prototypes/registry.md`) trước khi sang Bước 3.1.
```

> [!NOTE]
> Sau khi bạn mở các file `.html` trong `docs/prototypes/` xem trên trình duyệt và ưng ý 100%, hãy nhắn AI: *"Tôi duyệt toàn bộ giao diện prototype. Hãy chuyển trạng thái các màn hình trong `docs/prototypes/registry.md` sang `APPROVED` và bắt đầu Bước 3.1."*

#### Bước 3.1: Sinh Đặc tả Chi tiết (`docs/modules-spec/<slug>.md`) cho TẤT CẢ các Module

Dán câu lệnh:

```text
Hãy chuyển sang Gate 3 - Bước 3.1:
Dựa trên `docs/templates/module-spec-template.md`, hãy khởi tạo file Đặc tả Chi tiết Module `docs/modules-spec/<module-slug>.md` cho TẤT CẢ các module đã đăng ký trong `docs/plans/system-roadmap.md` (bắt đầu từ `system.md`, sau đó đến từng module nghiệp vụ/UI).
Mỗi file phải đầy đủ: Scope, User Stories, Tech Stack, Schema DB/DDL & Indexes chi tiết, Contracts & Events, Mục 5.4 UI Screen & Prototype Mapping (`SCR-<MOD>-<NN>`) đối với module UI, Sequence Diagrams & State Machine, Given/When/Then Acceptance Criteria, NFRs/Error Codes, và bảng Module Phase Sequence (`<MOD>-P<NN>`).
Nếu dự án có nhiều module, hãy viết kỹ từng module (1–2 module mỗi lượt) cho đến khi 100% module có file trong `docs/modules-spec/`.
Ngay khi viết xong toàn bộ `docs/modules-spec/*.md`, hãy DỪNG LẠI và hỏi tôi danh sách trang web/nguồn tìm kiếm AI Skills để bắt đầu Bước 3.2.
```

#### Bước 3.2: Tương tác Tìm kiếm Kỹ năng AI & Tạo `ai-skill-maps.md`

Ngay khi tạo xong toàn bộ `docs/modules-spec/*.md`, AI sẽ **dừng lại và hỏi bạn** các địa chỉ website hoặc kho lưu trữ để tìm kiếm AI Skills. Bạn trả lời kèm các nguồn bạn muốn:

```text
Hãy tìm kiếm các AI Skills phù hợp với tech stack và nghiệp vụ của từng module từ các nguồn sau:
- https://skillsmp.com/search
- https://felo.ai/vi/skills
- Thư mục `.agents/skills/` hoặc kho skill chính thức của framework
Đồng thời đề xuất thêm các skill đặc thù cho dự án (như `atomic-harness-gatekeeper`, `<project>-domain-invariants`, và `ui-prototype-fidelity` nếu dự án có giao diện UI).
Hãy lập bảng đề xuất danh sách Skill ánh xạ với từng module để tôi duyệt trước khi cài đặt và tạo file `ai-skill-maps.md`.
```

Sau khi xem bảng đề xuất skill của AI, bạn xác nhận duyệt:

```text
Tôi duyệt danh sách AI Skills này. Hãy thực hiện:
1. Cài đặt / khởi tạo các file `.agents/skills/<skill-name>/SKILL.md` đã được duyệt.
2. Tạo file `ai-skill-maps.md` ở thư mục gốc (theo mẫu `docs/templates/ai-skill-maps-template.md`).
3. Chuyển ngay sang Gate 3 - Bước 3.3: Tạo file `STEP-by-STEP.md` ở thư mục gốc (theo mẫu `docs/templates/step-by-step-template.md`) dành cho Kiến trúc sư Con người, rồi chạy `python scripts/validate_plans.py --fix`.
```

#### Bước 3.3: Sổ tay Hướng dẫn Thực thi (`STEP-by-STEP.md`)

- AI sẽ sinh ra file `STEP-by-STEP.md` ở thư mục gốc chứa sơ đồ thứ tự thực thi các module và các mẫu câu lệnh copy-paste đã được điền sẵn đúng tên module của dự án bạn.
- **Lưu ý quan trọng:** File `STEP-by-STEP.md` chỉ dành cho **bạn (người dùng)** đọc và copy lệnh. AI Agent sẽ không bao giờ đọc file này.

---

### Gate 4: Sinh trước Toàn bộ Hồ sơ Pha & WBS Nguyên tử cho Mọi Module

Trước khi được phép viết bất kỳ dòng code sản phẩm nào ở Gate 5, AI phải sinh trước **toàn bộ các file Phase Dossiers (`docs/plans/active/<module-slug>/phase-<NN>-<slug>.md`) cho tất cả các phase của tất cả các module trong dự án**.

Bạn có thể copy câu lệnh Gate 4 từ file `STEP-by-STEP.md` vừa được tạo (hoặc dùng lệnh dưới đây):

```text
Hãy chuyển sang Gate 4 (Sinh trước toàn bộ Phase Dossiers & WBS Nguyên tử cho toàn dự án):
1. Đọc `AGENTS.md`, `ai-skill-maps.md` (kèm các file `.agents/skills/*/SKILL.md` tương ứng), `docs/plans/system-roadmap.md`, `docs/plans/contract-registry.md`, `docs/prototypes/registry.md`, và toàn bộ `docs/modules-spec/*.md`. (Tuyệt đối KHÔNG đọc `STEP-by-STEP.md`).
2. Dựa trên `docs/templates/phase-dossier-template.md`, hãy khởi tạo TẤT CẢ các Phase Dossiers `docs/plans/active/<module-slug>/phase-<NN>-<slug>.md` cho MỌI phase của MỌI module trong dự án.
3. Trong mỗi Phase Dossier, phân rã chi tiết thành các Major Tasks (`<MOD>-P<NN>.<M>`) và Atomic Micro-Tasks cấp 4 (`<MOD>-P<NN>.<M>.<A>`):
   - `.1`: Định nghĩa Contract / Interface / Schema / Type (Contract-First)
   - `.2`: Triển khai logic nghiệp vụ hoặc UI Component (đối với task UI, BẮT BUỘC điền rõ `UI Prototype Reference: SCR-<MOD>-<NN>` trỏ tới file `docs/prototypes/<module-slug>/scr-<nn>-*.html`)
   - `.3`: Viết Unit Test / Component Test kèm lệnh kiểm chứng thực thi (assert đầy đủ các `data-testid` của Prototype đối với task UI)
4. Đặt `phase-01` của module khởi đầu ở trạng thái `READY_TO_EXECUTE` và các phase kế tiếp (`phase-02`, `phase-03`...) ở trạng thái `PENDING`.
5. Chạy `python scripts/validate_plans.py --fix` và báo cáo danh sách toàn bộ các Phase Dossiers đã tạo để tôi duyệt Gate 4.
QUY TẮC TUYỆT ĐỐI: KHÔNG viết code sản phẩm ở Gate 4.
```

---

### Gate 5: Thực thi Nguyên tử, Bảo toàn 1:1 UI & Máy Trạng Thái `"Tiếp tục"`

Khi toàn bộ Phase Dossiers đã sẵn sàng trong `docs/plans/active/` và `python scripts/validate_plans.py` báo `PASSED: 0 violations`, dự án chính thức mở khóa **Gate 5**.

#### 1. Bắt đầu Pha đầu tiên của một Module (ví dụ `SYS-P01`)

```text
Gate 4 đã hoàn tất. Hãy bước vào Gate 5 và bắt đầu thực thi Phase `SYS-P01`:
1. Đọc `ai-skill-maps.md` và kích hoạt các kỹ năng bắt buộc cho module `SYS` (`system`).
2. Đọc `docs/modules-spec/system.md` và `docs/plans/active/system/phase-01-foundation.md`.
3. Thực thi ĐÚNG 1 Atomic Task đầu tiên là `SYS-P01.1.1` (1 Lượt = 1 Atomic Task).
4. Chạy lệnh kiểm thử thực tế (Executable Proof), đánh dấu `[x]`, cập nhật `🎫 Resume Ticket`, và chạy `python scripts/validate_plans.py --fix`.
```

#### 2. Thực thi tuần tự cực nhanh chỉ với lệnh `"tiếp tục"`

Từ lúc này trở đi, bạn **không cần** phải gõ lại mã task dài dòng nữa. Ở mỗi lượt tiếp theo, bạn chỉ cần gõ:

```text
tiếp tục
```
*(Hoặc `"tiếp tục <MOD>"`, ví dụ `"tiếp tục AUTH"` / `"tiếp tục WEB"`, hoặc `"continue"`).*

Mỗi lần bạn gõ `"tiếp tục"`, AI sẽ tự động:
1. Kiểm tra `🎫 Resume Ticket` và chạy **Quy trình Đối soát Khôi phục Sự cố 3 Bước**.
2. Cập nhật `🎫 Resume Ticket` sang `IN_PROGRESS` với mã Atomic Task đang làm (Write-Ahead).
3. **Nếu task có `UI Prototype Reference` (`SCR-<MOD>-<NN>`):** Đọc ngay file `.html` prototype đã duyệt trong `docs/prototypes/<module-slug>/`, bê nguyên 1:1 cấu trúc DOM, CSS/Tailwind classes, các trạng thái (`default`/`loading`/`empty`/`error`) và các thuộc tính `data-testid` sang Component thực tế.
4. Chạy lệnh Unit Test / Component Test để chứng minh code chạy đúng (`Executable Proof`).
5. Đánh dấu `- [x]`, cập nhật `🎫 Resume Ticket` trỏ sang Atomic Task kế tiếp, và dừng lại chờ bạn.

#### 3. Hoàn thành Task Cuối cùng của một Phase & Chốt Chặn An Toàn (Hard Stop)

Ở lượt chạy hoàn thành **Atomic Task cuối cùng** của một phase (ví dụ `AUTH-P01`):
- AI đánh dấu `- [x]` cho task cuối cùng đó và chuyển `Lifecycle Status` trong `🎫 Resume Ticket` sang **`PHASE_COMPLETED`**.
- AI thông báo rõ ràng:
  > *"Đã hoàn thành toàn bộ Atomic Tasks của Phase `AUTH-P01`. Vui lòng nhập `tiếp tục phase AUTH-P02` để lưu trữ phase hiện tại và chuyển sang phase kế tiếp."*
- **Chốt chặn an toàn:** Khi một phase đã ở trạng thái `PHASE_COMPLETED` (không còn task `- [ ]` nào), nếu bạn vô tình gõ `"tiếp tục"` thông thường, AI **sẽ KHÔNG tự ý nhảy sang phase mới** mà dừng lại nhắc bạn nhập đúng lệnh chuyển phase.

#### 4. Chuyển sang Phase Kế tiếp với lệnh `"tiếp tục phase <MOD>-P<NN+1>"`

Để lưu trữ phase vừa xong và bắt đầu ngay phase tiếp theo, bạn gõ:

```text
tiếp tục phase AUTH-P02
```
*(Hoặc `"tiếp tục phase 02"`).*

Chỉ trong **1 lượt duy nhất đó**, AI sẽ tự động thực hiện trọn gói:
1. Di chuyển file hồ sơ `docs/plans/active/auth/phase-01-*.md` sang thư mục lưu trữ `docs/plans/completed/auth/phase-01-*.md`.
2. Kích hoạt file hồ sơ `docs/plans/active/auth/phase-02-*.md` (`Lifecycle Status: IN_PROGRESS`).
3. Chạy `python scripts/validate_plans.py --fix` để tự động đồng bộ bảng tiến độ trong `docs/modules-spec/auth.md` và `Active Work Pointer` trong `docs/plans/system-roadmap.md`.
4. Thực thi ngay **Atomic Task đầu tiên (`AUTH-P02.1.1`)** của phase mới!

---

## 5. Cơ chế Khóa 5 Lớp Ép AI Tuân Thủ 100% UI Prototype

Để ngăn chặn triệt để tình trạng AI "quên" giao diện mẫu hoặc tự ý sửa đổi bố cục khi sang Gate 5, **NTC Micro Harness v2.0** áp dụng **5 lớp bảo vệ đa tầng**:

| Lớp khóa | Nơi áp dụng | Cách thức ép AI tuân thủ 100% |
| :--- | :--- | :--- |
| **Lớp 1: Hợp đồng Giao diện (`SCR-<MOD>-<NN>`)** | `docs/prototypes/registry.md` & `docs/prototypes/<slug>/scr-<nn>-*.html` | Khóa chặt Design Tokens (bảng màu, font, bo góc, layout khung) và gán mã định danh `SCR-<MOD>-<NN>` cho từng màn hình. Phải đạt trạng thái `APPROVED` trước khi sang Bước 3.1. |
| **Lớp 2: Nhúng đường dẫn vào từng Atomic Task** | `docs/modules-spec/<slug>.md` (§5.4) & `phase-<NN>-*.md` (§3) | Mỗi Atomic Task giao diện đều có dòng `- **UI Prototype Reference:** SCR-<MOD>-<NN> (docs/prototypes/...)`. Khi bạn gõ `"tiếp tục"`, mắt AI nhìn thấy ngay đường dẫn file `.html` cần đọc trong lượt đó. |
| **Lớp 3: Khóa DOM bằng neo `data-testid`** | File HTML Prototype → Component thật → Unit Test (`.3`) | File HTML prototype bắt buộc gắn `data-testid="scr-<nn>-<element>"`. Component thật ở Gate 5 phải giữ nguyên các `data-testid` này, và Task `.3` (Unit/Component Test) bắt buộc assert sự tồn tại của chúng. |
| **Lớp 4: Luật trong `AGENTS.md` & Skill `ui-prototype-fidelity`** | `AGENTS.md`, `ai-skill-maps.md`, `STEP-by-STEP.md` | Quy định luật **1:1 UI Prototype Parity Invariant**: bắt buộc đọc file `.html` gốc ngay trong lượt code, bê nguyên cấu trúc DOM/class và cấm tự ý đổi thiết kế. |
| **Lớp 5: Kiểm tra cơ học bằng `validate_plans.py`** | `python scripts/validate_plans.py` | Tự động chặn đứng Gate 4/5 nếu có màn hình còn ở trạng thái `DRAFT` (`PROTOTYPE_NOT_APPROVED`), nếu thiếu file `.html` trên ổ cứng (`PROTOTYPE_FILE_MISSING`), hoặc nếu file `.html` quên gắn `data-testid=` (`PROTOTYPE_TESTID_MISSING`). |

---

## 6. Khôi phục Sự cố Giữa Chừng & Chạy Song Song Đa Agent (Git Worktree)

### 6.1 Khôi phục Sự cố Tắt Máy / Đóng App Giữa Chừng (3-Step Crash Recovery)

Nếu đang chạy dở một Atomic Task mà IDE bị treo, mất điện hoặc mất mạng giữa chừng, khi mở lại dự án bạn chỉ cần gõ:

```text
tiếp tục
```

Trước khi sửa bất kỳ file nào, AI bắt buộc thực hiện **3 bước đối soát thực tế trên ổ đĩa**:
1. **Đọc Hồ sơ Pha đang mở:** Xác định Atomic Task `- [ ]` đầu tiên chưa tích chọn và danh sách `Target Files` của task đó.
2. **Kiểm tra Cây thư mục Git (`git status` & `git diff`):** Kiểm tra xem các file mục tiêu trong `Code Root` của module đã bị sửa đổi gì trước khi sập máy chưa.
3. **Tự động xử lý thông minh:**
   - **Trường hợp 1 (Chưa có file nào bị sửa):** Thực thi Atomic Task đó từ đầu như bình thường.
   - **Trường hợp 2 (Code đã được viết xong trước khi sập máy và chạy Test PASS):** Tự động tích chọn `- [x]` cho task đó, ghi nhận khôi phục vào nhật ký, và chuyển sang làm luôn Atomic Task kế tiếp ngay trong lượt đó.
   - **Trường hợp 3 (Code đang viết dở dang hoặc Test đang FAIL):** Báo cáo ngắn gọn 3 dòng (*Module/Phase/Task đang dở, file/dòng bị ngắt quãng, và hướng xử lý*), sau đó **viết nốt phần logic còn thiếu** của đúng Atomic Task đó mà không làm mất hay nhân đôi code đã viết.

---

### 6.2 Chạy Song Song Nhiều AI Agent (Nhiều Tab hoặc Git Worktree)

Ngay khi các hợp đồng nền tảng ở `GP-01` (`SYS-P01`) đã được định nghĩa xong và chuyển sang trạng thái `AVAILABLE` trong `docs/plans/contract-registry.md`, bạn có thể mở **nhiều AI Agent chạy song song** cho các module độc lập (ví dụ: Agent 1 làm `AUTH`, Agent 2 làm `ORD`, Agent 3 làm `WEB`):

#### Cách A: Mở nhiều Tab Chat AI trong cùng Workspace
Ở mỗi tab chat, chỉ định rõ mã module khi gõ lệnh:
- **Tab 1:** `"tiếp tục AUTH"`
- **Tab 2:** `"tiếp tục WEB"`

Vì mỗi module chỉ được phép sửa code trong `Code Root` riêng của nó (ví dụ `services/auth/` và `services/web/`) và hồ sơ pha riêng (`docs/plans/active/auth/` và `docs/plans/active/web/`), các Agent hoàn toàn không bao giờ đụng độ file của nhau.

#### Cách B: Cô lập hoàn toàn bằng Git Worktree (Khuyên dùng khi chạy build/test nặng)
Tại thư mục gốc của dự án, tách nhánh Worktree riêng cho từng module:

```bash
git worktree add ../du-an-auth -b feat/auth main
git worktree add ../du-an-web -b feat/web main
```

Mở cửa sổ IDE / AI Agent riêng trong từng thư mục Worktree và gõ `"tiếp tục AUTH"` / `"tiếp tục WEB"`. Khi một module hoàn thành toàn bộ các phase:

```bash
python scripts/validate_plans.py --fix
git add . && git commit -m "feat(auth): hoan thanh toan bo cac phase cua module AUTH"
# Quay về thư mục dự án chính để gộp nhánh:
git checkout main
git merge --no-ff feat/auth
git worktree remove ../du-an-auth
```

---

## 7. Kiểm tra Tự động & Đồng bộ Hóa (`validate_plans.py`)

Bộ khung đi kèm công cụ kiểm tra cấu trúc và tự động đồng bộ trạng thái viết bằng Python thuần (không cần cài thêm thư viện ngoài):

```bash
# 1. Kiểm tra toàn bộ cấu trúc kế hoạch, module specs, hợp đồng, UI prototypes và hồ sơ pha
python scripts/validate_plans.py

# 2. Tự động đồng bộ bảng tiến độ trong docs/modules-spec/*.md và Active Work Pointer trong system-roadmap.md
python scripts/validate_plans.py --fix
```

**Những gì `scripts/validate_plans.py` tự động kiểm tra:**
- `AGENTS.md` giữ nguyên khối hợp đồng `<!-- HARNESS:BEGIN -->` ... `<!-- HARNESS:END -->`.
- Mọi module trong `docs/plans/system-roadmap.md` đều có file đặc tả `docs/modules-spec/<slug>.md` hợp lệ.
- Mọi hợp đồng liên module trong `docs/plans/contract-registry.md` (`CT-<MOD>-<NN>`) có file spec thực tế trên ổ cứng khi ở trạng thái `AVAILABLE`.
- Mọi màn hình giao diện trong `docs/prototypes/registry.md` (`SCR-<MOD>-<NN>`) đều thuộc về module đã đăng ký, có file `.html` thực tế chứa thuộc tính `data-testid="..."` khi `APPROVED`, và không còn màn hình nào ở trạng thái `DRAFT` khi module đó đã bước sang Gate 4/5.
- Khi đã có Phase Dossiers (Gate 4/5), bắt buộc phải tồn tại `ai-skill-maps.md` và `STEP-by-STEP.md` ở thư mục gốc.

---

## 8. Cấu trúc Thư mục & Bảng Quy ước Định danh

### Cấu trúc Thư mục

```text
.
├── AGENTS.md                                      # Hợp đồng vận hành & Quy tắc kỷ luật cho AI (v2.0)
├── README.md                                      # Tài liệu hướng dẫn tiếng Anh (English)
├── README.vi.md                                   # Tài liệu hướng dẫn tiếng Việt (Vietnamese)
├── docs/
│   ├── WORKFLOW.md                                # Đặc tả chi tiết giao thức 5 cổng, UI parity & khôi phục sự cố
│   ├── README.md                                  # Bản đồ thư mục tài liệu
│   ├── prototypes/                                # Sổ đăng ký UI Prototype & các file HTML mẫu (Gate 3.0)
│   │   ├── README.md
│   │   └── registry.md                            # Danh mục màn hình (SCR-<MOD>-<NN>) & Design System Tokens
│   ├── modules-spec/                              # Đặc tả chi tiết từng Module (docs/modules-spec/<slug>.md)
│   │   └── README.md
│   ├── patterns/
│   │   └── encoding-invariants.md                 # Các mẫu bất biến kỹ thuật & kiểm chứng cơ học
│   ├── plans/
│   │   ├── system-roadmap.md                      # Lộ trình Hệ thống, Module Registry & Active Work Pointer
│   │   ├── contract-registry.md                   # Sổ đăng ký hợp đồng API/Event/Schema liên module
│   │   ├── active/                                # Hồ sơ các phase đang chạy hoặc chờ chạy (<slug>/phase-<NN>-*.md)
│   │   └── completed/                             # Hồ sơ các phase đã hoàn thành & lưu trữ
│   └── templates/
│       ├── spec-template.md                       # Mẫu SPEC.md gốc
│       ├── system-roadmap-template.md             # Mẫu lộ trình hệ thống
│       ├── contract-registry-template.md          # Mẫu sổ đăng ký hợp đồng liên module
│       ├── ui-prototype-registry-template.md      # Mẫu sổ đăng ký UI Prototype & Design System
│       ├── module-spec-template.md                # Mẫu đặc tả chi tiết module (docs/modules-spec/<slug>.md)
│       ├── ai-skill-maps-template.md              # Mẫu bản đồ kỹ năng AI (ai-skill-maps.md)
│       ├── step-by-step-template.md               # Mẫu sổ tay hướng dẫn cho người dùng (STEP-by-STEP.md)
│       ├── phase-dossier-template.md              # Mẫu hồ sơ pha + Resume Ticket + WBS + UI Prototype Reference
│       ├── decision.md                            # Mẫu ghi nhận quyết định kiến trúc (ADR)
│       ├── exec-plan.md                           # Mẫu kế hoạch thực thi nhanh
│       └── application-runbook.md                 # Mẫu sổ tay vận hành & xử lý sự cố
├── scripts/
│   └── validate_plans.py                          # Công cụ kiểm tra cấu trúc & tự động đồng bộ (--fix)
├── install.py                                     # Trình cài đặt Python đa nền tảng (hỗ trợ chạy 1 lệnh từ xa)
├── install.ps1                                    # Trình cài đặt Windows PowerShell (hỗ trợ chạy 1 lệnh từ xa)
├── install.sh                                     # Trình cài đặt Linux / macOS / WSL Bash (hỗ trợ chạy 1 lệnh từ xa)
└── LICENSE                                        # Giấy phép MIT
```

### Bảng Quy ước Định danh (Identifier Convention)

| Cấp độ | Định dạng | Ví dụ | File Quản lý Chính thức |
| :--- | :--- | :--- | :--- |
| **Pha Toàn cục (Global Phase)** | `GP-<NN>` | `GP-01` | `docs/plans/system-roadmap.md` |
| **Mã Module / Slug** | `<MOD>` / `<slug>` | `AUTH` / `auth` | `docs/plans/system-roadmap.md` & `docs/modules-spec/auth.md` |
| **Pha của Module (Module Phase)** | `<MOD>-P<NN>` | `AUTH-P01` | `docs/plans/active/auth/phase-01-*.md` |
| **Tác vụ Lớn (Major Task)** | `<MOD>-P<NN>.<M>` | `AUTH-P01.2` | `docs/plans/active/auth/phase-01-*.md` |
| **Tác vụ Nguyên tử (Atomic Task)** | `<MOD>-P<NN>.<M>.<A>` | `AUTH-P01.2.3` | `docs/plans/active/auth/phase-01-*.md` (**1 Lượt = 1 Task**) |
| **Tác vụ Bổ sung Động (Hotfix)** | `<MOD>-P<NN>.<M>.<A>[a-z]` | `AUTH-P01.2.3a` | `docs/plans/active/auth/phase-01-*.md` |
| **Hợp đồng Liên Module (Contract)** | `CT-<PROVIDER>-<NN>` | `CT-AUTH-01` | `docs/plans/contract-registry.md` |
| **Nguyên mẫu Màn hình (UI Prototype)** | `SCR-<MOD>-<NN>` | `SCR-WEB-01` | `docs/prototypes/registry.md` (`docs/prototypes/<slug>/scr-<nn>-*.html`) |

---

## Giấy phép (License)

Phát hành theo giấy phép [MIT License](LICENSE). Bản quyền (c) 2026 [chien5572](https://github.com/chien5572).
