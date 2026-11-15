# Demo phong cách 2.5D

**Đã chọn B · Tranh thủy mặc cho pilot.** Ngày 2026-11-16 (UTC+07:00), chủ dự án xác nhận “chọn B” trong Codex sau khi xem bộ demo v3.

Tham chiếu đã chọn: `work/demo-ink-wash.mp4`, SHA-256 `cff5cf624b6def34984848d377123a26d1772ea28c247c8708088371c704368d`. Giữ nền giấy sáng, nét mực có độ loang, điểm nhấn đỏ son, chiều sâu tách lớp và động tác nhân vật đọc được khi camera đứng yên.

Ba clip kể cùng khoảnh khắc lữ khách áo đỏ dừng bên hồ, nâng đèn lên ngang tầm mắt, giữ một nhịp rồi hạ xuống. Vai và khuỷu tay đổi góc, đèn đung đưa và chập chờn, đuôi khăn uốn theo gió. Mỗi bản có bố cục, nét vẽ và đường máy quay riêng.

| Mã | Phong cách | Đặc điểm | MP4 cục bộ |
| --- | --- | --- | --- |
| A | Minh họa đêm trăng | Máy trượt sang phải qua rừng thông. Ánh trăng đổi hình và đậm nhạt theo gợn nước. | `work/demo-moonlit.mp4` |
| B | Tranh thủy mặc | Người đứng lệch trái dưới nhánh cây, núi tan vào sương và nét gợn mực lan trên mặt hồ. Máy lướt chậm sang trái. | `work/demo-ink-wash.mp4` |
| C | Sân khấu giấy cắt | Người đứng giữa cầu vòm. Ba mép sóng lượn độc lập dưới cầu khi máy tiến về nhân vật. | `work/demo-paper-cut.mp4` |

Contact sheet `work/m02-v3-contact.png` dùng khung trích từ MP4 tại giây 1, 6 và 11. GIF `work/m02-v3-fixed-camera.gif` là bản cận cảnh đối chiếu với máy quay cố định.

Toàn bộ hình trong clip được vẽ bằng code trong [cảnh thung lũng](scenes/valley.py) và [hai cảnh thủy mặc và giấy cắt](scenes/styles.py). Segoe UI có sẵn trên máy được dùng để ghi nhãn contact sheet cục bộ. Ba MP4 chỉ có hình.
