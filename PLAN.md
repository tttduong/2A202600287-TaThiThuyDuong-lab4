# 📋 PHÂN TÍCH DỰ ÁN - TRAVEL AGENT

## 1️⃣ TRẠNG THÁI HIỆN TẠI

### ✅ Các file đã có:
| File | Trạng thái | Mô tả |
|------|-----------|-------|
| `agent.py` | 70% hoàn thiện | Cấu trúc LanggraphAgent OK, tuy nhiên chưa có xử lý lỗi |
| `tools.py` | 40% hoàn thiện | Mock data OK, nhưng 3 tools chưa implement (chỉ có `pass`) |
| `system_prompt.txt` | 30% hoàn thiện | Prompt gốc chưa hoàn chỉnh, thiếu chi tiết tools |
| `requirements.txt` | 60% hoàn thiện | Thiếu `langgraph` |
| `test_api.py` | Không liên quan | File test đơn giản, không dùng cho travel agent |

### ⚠️ Vấn đề chính:
1. **Tools không implement**: `search_flights()`, `search_hotels()`, `calculate_budget()` - chỉ có `pass`
2. **System prompt không hoàn chỉnh**: Thiếu chi tiết cách sử dụng từng tool
3. **Requirements.txt thiếu**: Không có `langgraph`
4. **Không có error handling**: Agent không xử lý trường hợp tool gọi sai/trường hợp đặc biệt
5. **Không có config file**: API keys và model name hard-coded trong agent.py

---

## 2️⃣ KẾ HOẠCH PHÁT TRIỂN

### **PHASE 1: CẬP NHẬT DEPENDENCIES**
```
File cần sửa: requirements.txt
Thêm:
- langgraph>=0.4.0
- python-dotenv>=1.0.0
```

### **PHASE 2: IMPLEMENT 3 TOOLS CHÍNH**
Tất cả các hàm nằm trong `tools.py`:

#### 🛫 **Tool 1: search_flights(origin, destination)**
```
Input: origin (str), destination (str)
Output: Danh sách chuyến bay dạng string format đẹp
Logic:
  - Tra cứu FLIGHTS_DB với key (origin, destination)
  - Nếu không tìm thấy → thử ngược (destination, origin)
  - Format: "✈️ Hãng | Khởi: HH:MM → Đến: HH:MM | Giá: 1.450.000đ | Hạng: economy"
  - Nếu không có chuyến bay → "❌ Không tìm thấy chuyến bay từ X đến Y"
```

#### 🏨 **Tool 2: search_hotels(city, max_price_per_night)**
```
Input: city (str), max_price_per_night (int, default=999999999)
Output: Danh sách khách sạn dạng string format đẹp
Logic:
  - Tra cứu HOTELS_DB[city]
  - Lọc: price_per_night <= max_price_per_night
  - Sắp xếp: theo rating giảm dần
  - Format: "⭐ Tên | Sao: 5 | Giá: 1.800.000đ/đêm | Khu: Mỹ Khê | Rating: 4.5"
  - Nếu không có → "❌ Không tìm thấy khách sạn tại X với giá dưới Y/đêm"
```

#### 💰 **Tool 3: calculate_budget(total_budget, expenses)**
```
Input: total_budget (int), expenses (str: "vé_bay:890000,khách_sạn:650000")
Output: Chi tiết chi phí và ngân sách còn lại
Logic:
  - Parse expenses string thành dictionary
  - Tính tổng chi
  - Tính còn lại = total_budget - tổng_chi
  - Format: bảng chi tiết + "Ngân sách còn lại: X đ"
```

### **PHASE 3: HOÀN THIỆN SYSTEM PROMPT**
File cần sửa: `system_prompt.txt`
```
- Mô tả rõ ràng 3 tools + cách dùng
- Thêm ví dụ cụ thể
- Quy tắc: từ chối yêu cầu không liên quan đến du lịch
- Tư vấn đơn vị tiền tệ: VNĐ
```

### **PHASE 4: TĂNG CƯỜNG AGENT.PY**
```
Thêm vào:
1. Error handling: try-catch cho invoke()
2. Logging: ghi chi tiết tool calls
3. Validation: kiểm tra input người dùng trước khi gửi
4. Response formatting: format output đẹp hơn
```

### **PHASE 5: TAO FILE BỔ SUNG**
```
📄 config.py:
  - MODEL_NAME = "gpt-4o-mini"
  - API_KEY (from .env)
  - SYSTEM_PROMPT_PATH = "system_prompt.txt"

📄 utils.py:
  - format_price(num): 1450000 → "1.450.000đ"
  - format_currency(num): giống format_price
  - parse_expenses(expenses_str): parse string thành dict
  
📄 data_loader.py:
  - load_flights_db()
  - load_hotels_db()
  - (Chuẩn bị cho việc load từ database thực trong tương lai)

📄 README.md:
  - Hướng dẫn cài đặt
  - Hướng dẫn sử dụng
  - Ví dụ prompt
  
📄 .env.example:
  - OPENAI_API_KEY=your_key_here
  - MODEL_NAME=gpt-4o-mini
```

### **PHASE 6: TESTING**
```
📄 test_tools.py:
  - Unit tests cho từng tool
  - Test edge cases (thành phố không tồn tại, ngân sách 0, vv)

📄 test_agent.py:
  - Integration test cho toàn bộ agent
  - Test scenario thực tế (VD: "Tôi muốn đi Đà Nẵng với 5 triệu")
```

---

## 3️⃣ CẤU TRÚC DỰ ÁN SAU HOÀN THÀNH

```
lab4_agent/
├── agent.py                 # 🔄 Main agent logic (cập nhật)
├── tools.py                 # 🔄 Implement 3 tools (cập nhật)
├── system_prompt.txt        # 🔄 Hoàn thiện prompt (cập nhật)
├── requirements.txt         # 🔄 Thêm langgraph (cập nhật)
├── config.py                # ✨ TẠO MỚI - Config settings
├── utils.py                 # ✨ TẠO MỚI - Utility functions
├── data_loader.py           # ✨ TẠO MỚI - Load mock data
├── test_tools.py            # ✨ TẠO MỚI - Unit tests
├── test_agent.py            # ✨ TẠO MỚI - Integration tests
├── .env.example             # ✨ TẠO MỚI - Env template
├── README.md                # ✨ TẠO MỚI - Documentation
└── test_api.py              # ⚠️ Không cần (có thể xóa)
```

---

## 4️⃣ THỨ TỰ THỰC HIỆN

| Bước | Nhiệm vụ | Mức độ ưu tiên | Thời gian ước tính |
|------|---------|---------------|------------------|
| 1 | Update requirements.txt | 🔴 CRITICAL | 2 phút |
| 2 | Implement search_flights() | 🔴 CRITICAL | 10 phút |
| 3 | Implement search_hotels() | 🔴 CRITICAL | 10 phút |
| 4 | Implement calculate_budget() | 🔴 CRITICAL | 8 phút |
| 5 | Tạo utils.py (format functions) | 🔴 CRITICAL | 5 phút |
| 6 | Hoàn thiện system_prompt.txt | 🟠 HIGH | 10 phút |
| 7 | Tạo config.py | 🟡 MEDIUM | 5 phút |
| 8 | Tạo .env.example | 🟡 MEDIUM | 2 phút |
| 9 | Tạo README.md | 🟡 MEDIUM | 10 phút |
| 10 | Tạo data_loader.py | 🟢 LOW | 5 phút |
| 11 | Tạo test_tools.py | 🟢 LOW | 15 phút |
| 12 | Tạo test_agent.py | 🟢 LOW | 15 phút |
| **TOTAL** | | | **107 phút** |

---

## 5️⃣ KẾT QUẢ MONG ĐỢI

✅ **Sau hoàn thành:**
- Một travel agent hoàn toàn chức năng có thể:
  - Tìm kiếm chuyến bay theo các thành phố
  - Tìm kiếm khách sạn với bộ lọc giá
  - Tính toán chi phí du lịch
  - Trả lời các câu hỏi du lịch bằng tiếng Việt tự nhiên
  - Xử lý lỗi gracefully
  - Có documentation đầy đủ

💡 **Có thể mở rộng sau này:**
- Thêm conversation history
- Kết nối API thực (Skyscanner, Booking.com, vv)
- Thêm tool: địa điểm du lịch, thời tiết, nhà hàng
- Persistent conversation history (database)
- Web UI hoặc Telegram bot integration
