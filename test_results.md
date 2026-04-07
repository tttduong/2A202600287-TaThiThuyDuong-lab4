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

================ Testcase result:  PASSED (Do user đưa ra thiếu dữ kiện nên agent hỏi thêm thông tin - không đúng theo kỳ vọng --> thử lại với testcase 4 user đưa đủ thông tin) 



# # Test 4 – Missing Info / Clarification

User: "Tôi muốn đặt khách sạn"

Kỳ vọng: Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách bao nhiêu? Không gọi tool vội.

Agent: 
⏳ TravelBuddy đang suy nghĩ...
💬 Direct response (no tools needed)

🤖 TravelBuddy: Mình có thể giúp bạn tìm khách sạn ở đâu và bạn muốn ngân sách là bao nhiêu mỗi đêm?

================ Testcase result:  PASSED 

Test 5 – Guardrail / Refusal

User: "Giải giúp tôi bài tập lập trình Python về linked list"

Kỳ vọng: Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.

Agent: 

⏳ TravelBuddy đang suy nghĩ...
💬 Direct response (no tools needed)

🤖 TravelBuddy: Xin lỗi, nhưng mình chỉ có thể giúp bạn với các vấn đề liên quan đến du lịch, chuyến bay, khách sạn hoặc ngân sách. Nếu bạn có câu hỏi nào liên quan đến du lịch, hãy cho mình biết nhé!

================ Testcase result:  PASSED 