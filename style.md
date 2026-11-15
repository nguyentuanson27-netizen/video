# Demo phong cách 2.5D

**Trạng thái:** Chờ chủ dự án chọn A, B hoặc C trong Codex.

Cả ba clip dùng cùng cảnh lữ khách cầm đèn nhìn qua hồ, cùng thời lượng và cùng đường máy quay. Trăng hoặc mặt trời nằm ở lớp xa, lữ khách ở sườn đồi và hàng thông sát máy ở tiền cảnh. Khoảng dịch chuyển khác nhau giữa các lớp giúp so sánh cảm giác chiều sâu.

| Mã | Phong cách | Đặc điểm | MP4 cục bộ |
| --- | --- | --- | --- |
| A | Đêm trăng minh họa | Lam tím, trăng vàng và đèn ấm. Hợp cảnh kể chậm. Chi tiết vùng tối ít nổi bật hơn hai mẫu còn lại. | `work/demo-moonlit.mp4` |
| B | Tranh khắc mực | Nét gạch chéo, giấy ngả vàng, mặt trời và áo khoác đỏ son. Đường nét nổi rõ, chất liệu hạt dễ thấy nhất trong ba mẫu. | `work/demo-ink-print.mp4` |
| C | Giấy cắt nổi | Xanh ngọc và cam đất. Viền sáng cùng bóng đổ giúp đọc hình khối của núi, thảm cây và tiền cảnh. | `work/demo-paper-cut.mp4` |

Contact sheet `work/m02-contact.png` dùng khung trích từ MP4 tại giây 1, 6 và 11. Mỗi hàng là một phong cách.

Toàn bộ hình trong clip được dựng bằng code trong [cảnh thung lũng](scenes/valley.py) và [xử lý phong cách](scenes/styles.py). Không dùng ảnh, font, giọng hoặc nhạc trong ba MP4. Segoe UI có sẵn trên máy được dùng để ghi nhãn contact sheet cục bộ.

Sau khi chủ dự án chọn, ghi mã phong cách, ngày xác nhận và clip tham chiếu vào đây trước khi viết pilot.
