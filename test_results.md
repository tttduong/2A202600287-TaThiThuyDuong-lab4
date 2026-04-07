# # Test 1 – Direct Answer (Không cần tool)

User: "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."

Kỳ vọng: Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool nào.

Agent: 

⏳ TravelBuddy đang suy nghĩ...
💬 Direct response (no tools needed)

🤖 TravelBuddy: Chào bạn! Thật tuyệt khi nghe bạn đang lên kế hoạch cho chuyến đi. Bạn có thể cho mình biết một chút về 
sở thích du lịch của bạn không? Bạn thích những địa điểm biển, núi rừng hay thành phố nhộn nhịp? Hoặc có thể bạn muốn trải nghiệm văn hóa và ẩm thực? Hãy cho mình biết để mình có thể gợi ý cho bạn những điểm đến thú vị nhé!

================ Testcase result:  PASS

# # Test 2 – Single Tool Call

User: "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"

Kỳ vọng: Gọi search_flights("Hà Nội", "Đà Nẵng"), liệt kê 4 chuyến bay.

Agent: 

⏳ TravelBuddy đang suy nghĩ...
🔧 Tool: search_flights({'origin': 'Hà Nội', 'destination': 
'Đà Nẵng'})
💬 Direct response (no tools needed)

🤖 TravelBuddy: Dưới đây là các chuyến bay từ Hà Nội đến Đà 
Nẵng mà bạn có thể tham khảo:

1. **Vietnam Airlines** | 06:00 → 07:20 | 1.450.000đ | economy
2. **Vietnam Airlines** | 14:00 → 15:20 | 2.800.000đ | business
3. **VietJet Air** | 08:30 → 09:50 | 890.000đ | economy     
4. **Bamboo Airways** | 11:00 → 12:20 | 1.200.000đ | economy

Bạn có thích chuyến bay nào không? Hoặc nếu bạn cần thêm thông tin về khách sạn hay hoạt động ở Đà Nẵng, hãy cho mình biết nhé!

================ Testcase result:  PASS

# # Test 3 – Multi-Step Tool Chaining

User: "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"

Kỳ vọng: Agent phải tự chuỗi nhiều bước:

search_flights("Hà Nội", "Phú Quốc") -> tìm vé rẻ nhất (1.100.000đ)

Google Hotels("Phú Quốc", max_price phù hợp) -> gợi ý trong tầm giá

calculate_budget(5000000, "vé_bay:1100000,khách_sạn:...") -> tính còn lại

Rồi tổng hợp thành gợi ý hoàn chỉnh với bảng chi phí.

Agent: 
⏳ TravelBuddy đang suy nghĩ...
💬 Direct response (no tools needed)

🤖 TravelBuddy: Rất tuyệt vời! Phú Quốc là một điểm đến rất đẹp. 
Để có thể tư vấn tốt hơn, mình sẽ tìm chuyến bay và khách sạn cho bạn. Vào ngày nào bạn dự định khởi hành?

================ Testcase result:  UNPASSED (Do user đưa ra thiếu dữ kiện nên agent hỏi thêm thông tin - không đúng theo kỳ vọng --> Cần tích hợp conversation history) 



# # Test 4 – Missing Info / Clarification

User: "Tôi muốn đặt khách sạn"

Kỳ vọng: Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách bao nhiêu? Không gọi tool vội.

Agent: 
⏳ TravelBuddy đang suy nghĩ...
💬 Direct response (no tools needed)

🤖 TravelBuddy: Mình có thể giúp bạn tìm khách sạn ở đâu và bạn muốn ngân sách là bao nhiêu mỗi đêm?

================ Testcase result:  PASSED 

# # Test 5 – Guardrail / Refusal

User: "Giải giúp tôi bài tập lập trình Python về linked list"

Kỳ vọng: Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.

Agent: 

⏳ TravelBuddy đang suy nghĩ...
💬 Direct response (no tools needed)

🤖 TravelBuddy: Xin lỗi, nhưng mình chỉ có thể giúp bạn với các vấn đề liên quan đến du lịch, chuyến bay, khách sạn hoặc ngân sách. Nếu bạn có câu hỏi nào liên quan đến du lịch, hãy cho mình biết nhé!

================ Testcase result:  PASSED 

# # ✅ Test Case 6: Happy Path - Tìm Chuyến Bay Đơn Giản

User: tìm chuyến bay từ Hà nội đến Phú Quốc

Agent: 
⏳ TravelBuddy đang suy nghĩ...
🔧 Tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú 
Quốc'})
💬 Direct response (no tools needed)

🤖 TravelBuddy: Dưới đây là các chuyến bay từ Hà Nội đến Phú Quốc:

1. **Vietnam Airlines**:
   - Ngày: 08/04/2024
   - Giờ: 07:00 → 09:15
   - Giá: 2.100.000đ
   - Hạng: Economy

2. **VietJet Air**:
   - Ngày: 08/04/2024
   - Giờ: 10:00 → 12:15
   - Giá: 1.350.000đ
   - Hạng: Economy

3. **VietJet Air**:
   - Ngày: 08/04/2024
   - Giờ: 16:00 → 18:15
   - Giá: 1.100.000đ
   - Hạng: Economy

Bạn có dự định đi vào ngày nào và có ngân sách dự kiến cho khách 
   - Hạng: Economy

Bạn có dự định đi vào ngày nào và có ngân sách dự kiến cho khách 
Bạn có dự định đi vào ngày nào và có ngân sách dự kiến cho khách 
sạn hay không? Mình có thể giúp bạn tìm khách sạn phù hợp ở Phú Quốc!
================ Testcase result:  PASSED 
---

# # Test Case 7: Tricky Entity - Nhập nhằng địa danh

User: Đưa tôi từ Phú Quốc về Hà Nội, không phải ngược lại nhé.

Agent:

⏳ TravelBuddy đang suy nghĩ...
💬 Direct response (no tools needed)

🤖 TravelBuddy: Bạn muốn bay từ Phú Quốc về Hà Nội, đúng không? Cho mình biết thêm thông tin về ngày khởi hành và ngân sách bạn dự định nhé!

================ Testcase result:  PASSED 
---

## ✅ Test Case 8: Implicit Intent - Ý định ngầm định

User: Tôi đang ở Hà Nội, thèm ăn hải sản ở Đảo Ngọc quá nhưng chỉ có 2 triệu trong túi thôi.

Agent: 

⏳ TravelBuddy đang suy nghĩ...
💬 Direct response (no tools needed)

🤖 TravelBuddy: Nghe có vẻ thú vị đó! Nhưng trước tiên, mình cần 
biết một chút thông tin để giúp bạn lên kế hoạch cho chuyến đi nhé:

1. Bạn dự định đi trong bao lâu? (một ngày, hai ngày, ba ngày...?)
2. Bạn có muốn ở lại khách sạn hay homestay nào không? (chất lượng như thế nào: bình dân hay cao cấp?)
3. Bạn có muốn đặt vé máy bay trước không?

Khi có những thông tin này, mình sẽ giúp bạn tìm chuyến bay và chỗ ở phù hợp với ngân sách 2 triệu nhé!

================ Testcase result:  PASSED 
---

## ⚠️ Test Case 9: Context Switch & Correction - Thay đổi ý định đột ngột

User: Tìm cho tôi khách sạn 3 sao ở Đà Nẵng.

Agent: 

⏳ TravelBuddy đang suy nghĩ...
💬 Direct response (no tools needed)

🤖 TravelBuddy: Cho mình hỏi là bạn có ngân sách tối đa cho mỗi đêm ở khách sạn là bao nhiêu không? Điều này sẽ giúp mình tìm kiếm khách sạn phù hợp cho bạn hơn.

User: À thôi, đổi sang 5 sao đi, mà ở Phú Quốc nhé, cuối tuần này.

Agent: 
⏳ TravelBuddy đang suy nghĩ...
🔧 Tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú 
Quốc'})
🔧 Tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 2000000})
💬 Direct response (no tools needed)

🤖 TravelBuddy: Wow, bạn đã chọn một điểm đến tuyệt vời! Dưới đây là thông tin chuyến bay và khách sạn cho chuyến đi Phú Quốc cuối tuần này:

### 1. Chuyến bay từ Hà Nội đến Phú Quốc:
- **Vietnam Airlines** | 2024-04-08 | 07:00 → 09:15 | **2.100.000đ** (economy)
- **VietJet Air** | 2024-04-08 | 10:00 → 12:15 | **1.350.000đ** (economy)
- **VietJet Air** | 2024-04-08 | 16:00 → 18:15 | **1.100.000đ** (economy)

### 2. Khách sạn 5 sao tại Phú Quốc:
- **Sol by Meliá** | ⭐⭐⭐⭐ | **1.500.000đ/đêm** | Bãi Trường | Rat
ing: 4.2

*Còn một số khách sạn khác nhưng không đạt tiêu chuẩn 5 sao, như 
9Station Hostel và Lahana Resort.*

### 3. Tổng chi phí ước tính:
- **Chuyến bay**: từ **1.100.000đ** đến **2.100.000đ** (tuỳ chọn)- **Khách sạn**: **1.500.000đ/đêm** (tối thiểu)

### 4. Gợi ý thêm:
- Bạn có thể tham quan các điểm du lịch nổi tiếng như Vinpearl Land, Dinh Cậu, hay tham gia các hoạt động thể thao dưới nước thú vị ở Dương Đông.

Bạn có muốn tôi kiểm tra thêm thông tin gì nữa không?

================ Testcase result:  PASSED 

---

## ⚠️ Test Case 10: Edge Case - Ngày Tháng Không Chuẩn

👤 Bạn: Tìm giúp tôi chuyến bay từ hà nội đến phú quốc ngày 3/13

⏳ TravelBuddy đang suy nghĩ...
🔧 Tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú 
Quốc'})
💬 Direct response (no tools needed)

🤖 TravelBuddy: Xin lỗi, nhưng hệ thống hiện tại chỉ có dữ liệu chuyến bay cho ngày 8 tháng 4, không phải ngày 3 tháng 13. Dưới đây là các chuyến bay mà tôi tìm thấy cho ngày 8 tháng 4:

1. **Vietnam Airlines**
   - Giờ bay: 07:00 → 09:15
   - Giá: 2.100.000đ
   - Hạng ghế: Economy

2. **VietJet Air**
   - Giờ bay: 10:00 → 12:15
   - Giá: 1.350.000đ
   - Hạng ghế: Economy

3. **VietJet Air**
   - Giờ bay: 16:00 → 18:15
   - Giá: 1.100.000đ
   - Hạng ghế: Economy

Bạn có muốn chọn một trong những chuyến bay này không, hoặc bạn cần trợ giúp với ngày bay khác không?

================ Testcase result:  PASSED 
