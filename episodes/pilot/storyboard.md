# Storyboard Gió Bắc và Mặt Trời

**Bản gửi duyệt:** `board-v1` · Phong cách B, tranh thủy mặc · 60 giây, 24 fps

Tham chiếu [`script-v1`](script.md), [timing câu](narration-timing.json) và bản Quang Sơn được ghi trong [hồ sơ duyệt](approvals.md). Dùng nền giấy sáng, núi mực loang, áo đỏ son và màu nắng ấm tăng dần. Bố cục thay đổi từ toàn cảnh sang cận cảnh bàn tay để nối hành động với đoạn bình.

## Thời lượng và lời đọc

| Cảnh | Khung bắt đầu → kết thúc | Thời gian | Cue và đoạn có lời |
| --- | ---: | --- | --- |
| S01 · Cuộc thách đấu | 0 → 326 | 0,000–13,583 s | 1–3 · 0,720–12,794 s · Cuộc cá cược và lữ khách bước đi |
| S02 · Gió Bắc | 326 → 684 | 13,583–28,500 s | 4–7 · 14,344–27,741 s · Gió quật áo, lữ khách ghì hai vạt, gió nhường lượt |
| S03 · Mặt Trời | 684 → 970 | 28,500–40,417 s | 8–9 · 29,291–39,623 s · Nắng ấm lên, người cởi áo, vắt áo lên đá và xuống suối |
| S04 · Bàn tay buông áo | 970 → 1440 | 40,417–60,000 s | 10–13 · 41,173–56,712 s · Lời bình về lúc siết tay và lúc tự buông |

Mốc khung kết thúc là mốc chuyển sang cảnh kế tiếp. Tổng 1.440 khung. Ba điểm cắt nội bộ nằm trong khoảng nghỉ giữa các đoạn giọng. Lời kết dứt ở 56,712 giây. Giữ hình và phần nhạc nền đến 60 giây.

## Cảnh 01 · Cuộc thách đấu

Toàn cảnh đường mòn bên suối. Núi mờ ở xa, mặt trời đỏ son ở phía phải, thân cây mực đậm sát mép trái. Lữ khách áo đỏ bước dọc bờ, hai tay giấu vào áo.

- **Lớp và máy quay** · Nền giấy và mặt trời, hai tầng núi, gợn nước, bờ có nhân vật, cành cây tiền cảnh. Máy trượt sang phải nhẹ theo bước chân.
- **Diễn xuất** · Chân luân phiên bước và chạm đất. Thân người nhún theo bước, vạt áo rung nhẹ. Mở bằng tiếng nước và một nhịp trước lời đầu.

## Cảnh 02 · Gió Bắc

Trung cảnh gần hơn, thấp ngang sườn dốc. Vệt mực gió quét chéo qua nền sáng. Lữ khách cúi đầu, kéo hai vạt áo sát ngực.

- **Lớp và máy quay** · Nền núi, vệt gió, bờ dốc, lữ khách và lá gần máy. Máy tiến vào nhẹ khi tay siết chặt, giữ ổn định ở cuối cảnh.
- **Diễn xuất** · Gió đẩy khăn và gấu áo ngược chiều bước. Hai cánh tay kéo vạt áo vào sát thân. Gió và lá lắng xuống cùng câu nhường lượt.

## Cảnh 03 · Mặt Trời

Nắng ấm pha vàng trên mặt giấy và mặt nước. Lữ khách tháo áo đỏ, vắt lên tảng đá và tiến xuống suối. Khung mẫu giữ nhân vật ở mép nước và chiếc áo trên đá.

- **Lớp và máy quay** · Quầng nắng sau núi, phản sáng trên suối, bờ đá, nhân vật và cành cây sát mép phải. Máy hạ nhẹ từ mặt trời xuống chiếc áo và mép nước.
- **Diễn xuất** · Vai thả lỏng, tay mở vạt áo và đặt áo xuống. Khi người bước xuống suối, máy giữ ở áo trên đá và gợn nước lan ra.

## Cảnh 04 · Bàn tay buông áo

Cận cảnh bàn tay và chiếc áo trên đá. Cùng góc nhìn, bàn tay mở ra theo lời kể. Khung mẫu ghi tư thế đã mở, với gợn sáng trên suối phía sau.

- **Lớp và máy quay** · Núi mờ, sóng sáng, đá, áo đỏ và bàn tay tiền cảnh. Máy chậm dần rồi dừng ở lòng bàn tay.
- **Diễn xuất** · Ngón tay co ở nhịp “chúng siết lại”, duỗi ra ở nhịp “chúng tự buông”. Sau câu cuối, giữ bề mặt nước chuyển động nhẹ và hạ âm lượng đến hết cảnh.

## Khung tham chiếu

Chạy `.\.venv\Scripts\python.exe -m scenes.pilot_board` từ repo trên Windows. Xuất bốn PNG 1280×720 và ảnh tổng hợp `work/pilot/storyboard/board-v1.png`.

| Khung | SHA-256 PNG |
| --- | --- |
| `s01.png` | `4fed28a42823373f4a6ee63e9c52809572cfa57e19974b90974df008b643b4f3` |
| `s02.png` | `22661df88a30d33cabd4486275db0971711c04803672de06ebe2edd081df4d02` |
| `s03.png` | `426ab89a40e6c0240507171a18a90f773d47a2ccec70108a88d51a6543c96627` |
| `s04.png` | `e2a68f1deda3bcb403e268f48da112d74976817c7296d48d029f1a0f11761166` |
