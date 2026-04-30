---
layout: page
title: Newspaper
permalink: /newspaper/
---

### Silkium
Author: Alice Evenander - Phan Minh Thiên Hoàng
Date: 30/4/2026, lúc 19h33 phút cùng ngày


# Lời nói đầu 
Vào khoảng 2009, Satoshi Nakamoto giới thiệu mô hình Bitcoin, mô hình tiền ảo với phương châm theo đuổi chân lý phân tán hoàn toàn(decentralized system) trong đó đề cập đến việc xem tiền tệ như một đơn vị phi tập trung(tức rằng không bị ràng buộc bởi các cơ chế chính phủ hiện hành). Năm 2015, lập trình viên gốc Nga người Canada Vitalik Buterin vận hành một hệ thống tiền tệ tương tự với Bitcoin, nhưng trong đó áp dụng các công nghệ Smart Contract và cơ chế PoS(Proof of Stake) đối lập với tính bảo thủ của Bitcoin. Đó là hai ví dụ rất tốt về một mô hình phân tán hoàn toàn, dẫu vậy những dạng mô hình được đề cập ở trên chỉ dừng lại trong khuôn khổ tài chính chứ chưa được phổ biến rộng rãi qua các lĩnh vực khác.

Thương mại điện tử hiện đại phụ thuộc vào các nền tảng trung gian tập trung, nơi phí cao, hệ thống xếp hạng dễ bị làm giả qua giao dịch ảo, review farm và tối ưu nội bộ nền tảng, seller chịu chi phí nền tảng cao và phụ thuộc thuật toán phân phối traffic, buyer thường phải cung cấp danh tính, địa chỉ, lịch sử mua sắm và dữ liệu hành vi cho nền tảng trung gian.

Nhận thấy đặc điểm đó, một mô hình mạng phân tán trong lĩnh vực thương mại, Silkium, được giới thiệu, trong đó được kì vọng giải quyết các vấn đề hiện hữu của đa số các sàn thương mại điện tử lúc bấy giờ:
- Phí trung gian cao(khoảng 8%-15% tùy vào sàn)
- Uy tín bị nâng một cách vô lý do sự xuất hiện của các đơn mua hàng ảo bởi các tài khoản ảo
- Quyền sở hữu và thêm các luật thuộc về chủ của hệ thống chứ không phải từ ý kiến đa số của người dùng
- Sự cạnh tranh thiếu công bằng(bằng các thủ thuật được đề cập ở trên) giữa các người bán 

Vì vậy, Silkium được thiết kế để giảm thiểu những vấn đề này thông qua kiến ​​trúc phi tập trung, xác minh mật mã, ký quỹ và mô hình uy tín dựa trên hành vi có trọng số thay vì chỉ dựa trên số lượng tương tác thông thường. Tất cả điều đó sẽ được giới thiệu ở phần sau nữa của văn bản

# Mục lục
- Lời nói đầu
- 1. Kiến trúc của Silkium
- 2. Các khái niệm được sử dụng 
    - a. Mã hóa và xác minh danh tính bằng RSA(X25519) và EdDSA(Ed25519)
    - b. Phương thức PoS(Proof of Stake) trong việc xác minh tính chính xác của thông tin 
    - c. DNS 
    - d. Cơ chế code xác nhận
    - e. Cơ chế tính toán trọng số weight W
    - f. Máy tìm kiếm
    - g. Blockchain
- 3. Vấn đề về lưu trữ chuỗi blockchain
- 4. Định hướng phát triển


## 1. Kiến trúc của Silkium 


