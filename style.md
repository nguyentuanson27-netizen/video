# Demo phong cách 2.5D

**Trạng thái:** Bản demo v3 có animation nhân vật. Chờ chủ dự án chọn A, B hoặc C trong Codex.

Ba clip kể cùng khoảnh khắc lữ khách áo đỏ dừng bên hồ, nâng đèn lên ngang tầm mắt, giữ một nhịp rồi hạ xuống. Vai và khuỷu tay đổi góc, đèn đung đưa và chập chờn, đuôi khăn uốn theo gió. Mỗi bản có bố cục, nét vẽ và đường máy quay riêng.

| Mã | Phong cách | Đặc điểm | MP4 cục bộ |
| --- | --- | --- | --- |
| A | Minh họa đêm trăng | Máy trượt sang phải qua rừng thông. Ánh trăng đổi hình và đậm nhạt theo gợn nước. | `work/demo-moonlit.mp4` |
| B | Tranh thủy mặc | Người đứng lệch trái dưới nhánh cây, núi tan vào sương và nét gợn mực lan trên mặt hồ. Máy lướt chậm sang trái. | `work/demo-ink-wash.mp4` |
| C | Sân khấu giấy cắt | Người đứng giữa cầu vòm. Ba mép sóng lượn độc lập dưới cầu khi máy tiến về nhân vật. | `work/demo-paper-cut.mp4` |

Contact sheet `work/m02-v3-contact.png` dùng khung trích từ MP4 tại giây 1, 6 và 11. GIF `work/m02-v3-fixed-camera.gif` là bản cận cảnh đối chiếu với máy quay cố định.

Toàn bộ hình trong clip được vẽ bằng code trong [cảnh thung lũng](scenes/valley.py) và [hai cảnh thủy mặc và giấy cắt](scenes/styles.py). Segoe UI có sẵn trên máy được dùng để ghi nhãn contact sheet cục bộ. Ba MP4 chỉ có hình.

Sau khi chủ dự án chọn, ghi mã phong cách, ngày xác nhận và clip tham chiếu vào đây trước khi viết pilot.
