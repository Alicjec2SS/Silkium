# Silkium(INeedANewGuitar) Whitepaper v1.0

**A Decentralized Commerce Protocol**

Author: Evenander Alice  
Date: 2026-04-24  
Status: Draft / Active Development


Xin thứ lỗi quý độc giả vì bản tài liệu này được viết bằng tiếng Việt. Đây là ngôn ngữ tôi yêu, nhưng cũng là cách nhanh nhất để diễn đạt thẳng ý tưởng mà không bị mất chất.

Tôi tên là **Evenander Alice** (gọi tôi là Hoàng cũng được, hoặc đầy đủ hơn là Phan Minh Thiên Hoàng(tên giả thôi :33)).

Tôi là người chủ trì dự án **Silkium (hay có tên khác chuyên nghiệp hơn là INeedANewGuitar  )**.

---

## Abstract
**Silkium(INeedANewGuitar)** là một marketplace phi tập trung cho hàng vật lý, được thiết kế để giảm phí trung gian, giảm spam, chống buff đơn ảo, và hạn chế việc một nền tảng duy nhất kiểm soát toàn bộ luồng giao dịch.

# 1. Tóm tắt dự án

**Silkium(INeedANewGuitar)** là một marketplace phi tập trung cho hàng vật lý, được thiết kế để giảm phí trung gian, giảm spam, chống buff đơn ảo, và hạn chế việc một nền tảng duy nhất kiểm soát toàn bộ luồng giao dịch.

Mục tiêu của hệ thống là:

* không có sàn trung tâm nắm quyền sinh sát
* mọi giao dịch đều có thể xác minh bằng chữ ký số và smart contract
* tìm kiếm sản phẩm được thực hiện theo cơ chế phân tán
* giao tiếp giữa buyer và seller có thể đi qua relay để giảm lộ IP
* ranking dùng **weight system** thay vì đếm lượt mua thô
* xử lý tranh chấp bằng một cơ chế cực đơn giản: **code 3 = cả hai bên cùng chịu phí phạt như nhau**

Tinh thần chung của hệ thống là:

```text
không cần tin người
→ chỉ cần tin code
```

---

# 2. Vấn đề mà hệ thống muốn giải quyết

Marketplace truyền thống có một số vấn đề cốt lõi:

* phí trung gian cao
* tài khoản clone có thể buff đơn, buff review, buff uy tín giả
* dữ liệu người dùng bị tập trung
* dispute thường phụ thuộc vào một bên trung gian xử lý
* người bán nhỏ khó cạnh tranh công bằng với nền tảng lớn

Silkium(INeedANewGuitar) được thiết kế để giảm những điểm này bằng kiến trúc phân tán, cơ chế ký số, escrow, và weight-based ranking.

---

# 3. Mô hình tổng thể

Hệ thống gồm bốn lớp chính:

1. **Identity layer**: định danh bằng cặp khóa công khai / bí mật
2. **Network layer**: P2P + DHT + relay broadcast
3. **Commerce layer**: listing, search, order, escrow, settlement
4. **Incentive layer**: weight, stake, penalty, treasury/community fund

---

# 4. Identity

Mỗi node trong hệ thống có hai cặp khóa:

```text
1. Signing keypair
- private signing key
- public signing key

2. Encryption keypair
- private decrypt key
- public encrypt key
```

## Ý nghĩa

* **private signing key**: dùng để ký
* **public signing key**: dùng để verify chữ ký
* **public encrypt key**: dùng để mã hóa nội dung gửi đến người đó
* **private decrypt key**: dùng để giải mã

Hệ thống không dựa vào account truyền thống theo kiểu sàn tập trung.
Thay vào đó, identity gắn với keypair và lịch sử hành vi trên mạng.

---

# 5. Network

Hệ thống hoạt động trên mô hình:

* **P2P hoàn toàn**
* **DHT để discovery**
* **relay broadcast để giảm lộ IP**
* **broadcast listing / request / transaction state**

## Nguyên tắc relay

Khi một packet được gửi đi:

1. nó được mã hóa cho người nhận mục tiêu
2. nó được ký bởi người gửi
3. nó được bọc lại cùng public key cần thiết để verify / giải mã
4. nó được gửi đến một node bất kỳ
5. node đó relay tiếp cho đến khi đến được đích

Mục đích là không để buyer và seller phải lộ trực tiếp IP gốc của mình nếu không cần thiết.

---

# 6. Search Engine

Search không có server trung tâm.

Mỗi user chạy một search engine local, lấy dữ liệu từ:

* DHT table
* listing broadcast
* metadata công khai của seller
* logic ranking cục bộ trên máy người dùng

## Mục tiêu của search

* tìm sản phẩm theo từ khóa
* tìm seller theo region / uy tín / weight
* lọc các listing phù hợp với điều kiện người mua

---

# 7. Weight System

Đây là phần quan trọng để chống clone, chống buff đơn, và làm ranking công bằng hơn.

Hệ thống **không** dùng số lượt mua thô.
Hệ thống dùng **weight score**.

## 7.1. Ý tưởng

Một giao dịch thật không nên có giá trị giống một tương tác rác.

Vì vậy, mỗi account / key / listing sẽ có weight phản ánh chất lượng hành vi, không chỉ phản ánh số lượng.

---

## 7.2. Thành phần của weight

Giả sử một seller có weight tổng là:

```text
W = Wrep + Wstake + Wage + Wtrade - Wrisk - Wdispute
```

Trong đó:

* `Wrep`: weight từ giao dịch thành công
* `Wstake`: weight từ stake đang khóa
* `Wage`: weight từ tuổi key / tuổi tài khoản
* `Wtrade`: weight từ khối lượng giao dịch thật
* `Wrisk`: trừ điểm rủi ro do behavior xấu
* `Wdispute`: trừ điểm do tranh chấp / code 3 / vi phạm

---

## 7.3. Công thức đề xuất

### Weight giao dịch thành công

Mỗi giao dịch thành công đóng góp một lượng weight:

```text
Wrep += log2(1 + V) × Q
```

Trong đó:

* `V` = giá trị giao dịch
* `Q` = hệ số chất lượng của giao dịch

`Q` có thể được tính từ:

```text
Q = 1 - r
```

với `r` là dispute rate lịch sử của seller/buyer trong khoảng thời gian gần nhất.

---

### Weight theo stake

Stake càng cao thì weight nền càng lớn:

```text
Wstake = k1 × sqrt(S)
```

Trong đó:

* `S` = số token đang bị khóa làm stake
* `k1` = hệ số điều chỉnh của protocol

Dùng căn bậc hai để tránh người có vốn lớn áp đảo hoàn toàn.

---

### Weight theo tuổi key

Key càng lâu đời, weight nền càng cao:

```text
Wage = k2 × ln(1 + D)
```

Trong đó:

* `D` = số ngày key đã tồn tại
* `k2` = hệ số điều chỉnh

Dùng log để tránh việc chỉ cần chờ rất lâu là weight tăng quá mạnh.

---

### Trừ điểm rủi ro

Nếu một account có hành vi xấu, weight bị trừ:

```text
Wrisk = a × FraudSignals + b × SpamSignals + c × FailedOrders
```

Trong đó:

* `FraudSignals`: tín hiệu gian lận
* `SpamSignals`: tín hiệu spam listing / spam request
* `FailedOrders`: số đơn thất bại do lỗi bên đó

---

### Trừ điểm dispute

```text
Wdispute = d × DisputeCount + e × Code3Count
```

Trong đó:

* `DisputeCount`: số lần dispute
* `Code3Count`: số lần kích hoạt code 3

---

## 7.4. Chuẩn hóa weight

Để ranking dễ dùng, weight có thể được chuẩn hóa về khoảng `0..1000`:

```text
Wnorm = 1000 × (W - Wmin) / (Wmax - Wmin)
```

Nếu không có đủ dữ liệu, hệ thống có thể dùng `W = 0` hoặc `W = base_weight` theo policy của protocol.

---

# 8. Transaction Model

Mỗi giao dịch có các trường cơ bản:

```text
- transaction_id
- buyer pubkey
- seller pubkey
- item_id
- price
- timestamp
- status_code
- signatures
```

## Nguyên tắc

* mỗi trạng thái giao dịch đều phải có dấu vết rõ ràng
* dữ liệu quan trọng đều phải ký số
* smart contract là nơi chốt trạng thái cuối cùng

---

# 9. Listing Model

Seller tạo listing gồm:

```text
- item
- giá
- mô tả
- region
- public key
- timestamp
- listing signature
```

Listing được ký bằng private signing key của seller, sau đó broadcast toàn mạng.

Search engine local của người dùng sẽ đọc listing này từ DHT/broadcast stream và đưa vào kết quả tìm kiếm.

---

# 10. Flow Buyer

## Bước 1: tìm seller

Buyer tìm mặt hàng mình cần bằng search engine local.

Search engine dùng:

```text
- DHT table
- listing broadcast
- ranking theo weight
- lọc theo region / giá / mô tả
```

Kết quả là danh sách seller phù hợp.

---

## Bước 2: gửi yêu cầu mua qua relay broadcast

Buyer tạo packet chứa:

```text
{
  item cần mua,
  nơi nhận hàng,
  timestamp
}
```

Sau đó:

1. mã hóa packet bằng public encrypt key của seller
2. ký nội dung ciphertext bằng private signing key của buyer
3. đính kèm:

   * buyer public signing key
   * buyer public encryption key
4. gửi packet tới một node bất kỳ trong mạng

Node nhận packet sẽ relay tiếp theo cơ chế P2P cho đến khi seller nhận được.

Mục tiêu là giảm việc lộ IP trực tiếp của buyer.

---

## Bước 3: seller phản hồi

Seller nhận packet, giải mã, kiểm tra chữ ký, rồi gửi phản hồi bằng packet mới:

```text
{
  item,
  nơi để hàng / nơi giao,
  thời gian,
  mô tả thêm,
  timestamp
}
```

Packet phản hồi:

* được encrypt bằng public key của buyer
* được seller ký
* được relay ngược lại qua network

---

## Bước 4: buyer gửi tiền vào escrow

Buyer gửi tiền vào smart contract trên Ethereum/EVM chain.

```text
status = FUNDED
```

Tiền lúc này chưa thuộc seller, cũng chưa quay về buyer.
Nó đang nằm trong escrow.

---

## Bước 5: xác nhận giao dịch

Buyer và seller cùng ký vào một message chung:

```text
{
  item,
  transaction_id,
  signed_time,
  code
}
```

Trong đó `code` là trạng thái thỏa thuận cuối cùng:

* `1` → hoàn thành giao dịch
* `2` → hoàn hàng / refund
* `3` → không nhận được hàng / tranh chấp cứng

Message này có thể được ghi on-chain hoặc broadcast để contract đọc.

---

# 11. Flow Seller

## Bước 1: tạo listing

Seller tạo listing, ký số, rồi broadcast.

---

## Bước 2: nhận request

Seller nhận packet relay từ buyer.

Seller sẽ:

* verify chữ ký buyer
* decrypt nội dung
* check format
* kiểm tra item có hợp lệ không

---

## Bước 3: phản hồi buyer

Seller gửi packet phản hồi đã ký và mã hóa cho buyer.

---

## Bước 4: đợi escrow

Nếu thấy tiền đã vào contract:

```text
→ chuẩn bị giao hàng
```

---

## Bước 5: ship hàng

Seller giao hàng đến nơi đã thỏa thuận.

---

# 12. State Machine

Trạng thái giao dịch có thể được mô tả như sau:

```text
CREATED
→ REQUEST_SENT
→ LISTING_CONFIRMED
→ FUNDED
→ SHIPPED
→ DELIVERED
→ SETTLED
```

Với nhánh khác:

```text
FUNDED
→ CODE_2_REFUND
→ REFUNDED
```

Hoặc:

```text
FUNDED
→ CODE_3_DISPUTE
→ PENALIZED
```

---

# 13. Xử lý bằng code

## Code = 1

```text
buyer + seller cùng ký code 1
→ smart contract release tiền cho seller
→ giao dịch kết thúc
```

Đây là trạng thái tốt nhất.

---

## Code = 2

```text
buyer + seller cùng ký code 2
→ refund buyer
→ có thể hoàn toàn hoặc một phần tùy chính sách
```

Dùng khi hai bên đồng thuận kết thúc giao dịch theo hướng hoàn hàng / hủy đơn.

---

## Code = 3

Đây là điểm quan trọng nhất của protocol.

```text
buyer ký code 3
→ tranh chấp cứng
→ không xét đúng sai
→ cả buyer và seller cùng mất penalty như nhau
→ số tiền penalty chuyển vào community fund
```

### Tại sao làm như vậy

* không cần verifier phải phán xét ai đúng ai sai
* không cần evidence phức tạp
* giảm bớt chi phí tranh chấp
* làm cho việc đi đến code 3 trở nên đắt đỏ
* tránh tình trạng spam dispute

### Tính chất của code 3

Code 3 không phải nút refund.
Nó là nút **khóa tổn thất đối xứng**.

Nếu giao dịch đi đến code 3, hệ thống xem đây là một failure state mà cả hai bên đều phải chia sẻ trách nhiệm.

---

# 14. Công thức penalty cho code 3

Giả sử:

```text
P = giá trị món hàng
```

Hệ thống có thể quy định:

```text
buyer_penalty = α × P
seller_penalty = α × P
```

với:

```text
0 < α ≤ 1
```

Nếu muốn cực đoan và rất nghiêm khắc, có thể đặt:

```text
α = 1
```

khi đó cả buyer và seller đều mất đúng 100% phần collateral đã khóa cho giao dịch đó.

## Khi code 3 xảy ra

```text
buyer mất αP
seller mất αP
```

Nếu alpha bằng 1:

```text
buyer mất 100% giá trị buyer đã khóa
seller mất 100% collateral seller đã khóa
```

### Nơi số tiền đi tới

Số tiền này không bị đốt.
Nó được chuyển vào **community fund** hoặc **public treasury** của protocol.

Mục đích:

* tài trợ audit
* tài trợ bug bounty
* tài trợ hạ tầng node
* hỗ trợ hoạt động cộng đồng
* làm quỹ công khai, minh bạch, có thể kiểm toán

---

# 15. Vì sao penalty đối xứng

Penalty đối xứng là hợp lý nhất nếu protocol muốn giữ triết lý:

```text
không phán xét ai đúng ai sai
```

Nếu bất đối xứng, protocol sẽ ngầm nói rằng một bên đáng tin hơn bên kia.
Điều đó làm hệ thống nghiêng về phán xử thay vì rule-based.

Vì vậy:

* buyer và seller cùng chấp nhận luật chơi
* giao dịch thất bại nghiêm trọng thì cả hai cùng chịu hậu quả ngang nhau
* không có cơ chế thiên vị cố định

---

# 16. Community Fund

Community fund là nơi nhận các khoản penalty từ code 3.

## Mục tiêu của quỹ

* chi trả cho audit smart contract
* thưởng node vận hành mạng
* tài trợ nhà phát triển
* tài trợ học bổng / hoạt động cộng đồng / dự án xã hội nếu governance quyết định như vậy

## Nguyên tắc

Quỹ này phải:

* công khai
* on-chain hoặc có sổ ghi minh bạch
* dễ kiểm toán
* không phụ thuộc vào một cá nhân nắm quyền

---

# 17. Verifier

Ở bản thiết kế hiện tại, **code 3 không cần verifier để xét đúng sai**.

Tuy nhiên, verifier vẫn có thể tồn tại trong hệ thống cho các nhiệm vụ khác như:

* kiểm tra tính hợp lệ của transaction format
* xác nhận packet broadcast có đúng chuẩn protocol
* tham gia các cơ chế hệ thống khác nếu sau này mở rộng

## Nếu dùng verifier

* chọn ngẫu nhiên từ pool có stake
* nhiều verifier cùng lúc
* slash nếu hành xử sai

Nhưng với **code 3**, mặc định không cần họ phán xử tranh chấp.

---

# 18. Stake System

Muốn tham gia các vai trò có trách nhiệm cao trong protocol, một node phải khóa token vào smart contract.

## Stake dùng để làm gì

* tăng độ tin cậy
* chống spam
* chống hành vi phá mạng
* tạo ràng buộc kinh tế

---

# 19. Slashing

Nếu một vai trò có stake mà làm sai vai trò của mình, stake có thể bị slash.

Ví dụ:

* xác thực sai dữ liệu
* cố tình phá quy trình
* gian lận theo luật của protocol

Stake bị slash có thể được dùng để:

* thưởng lại cho bên bị thiệt hại
* chuyển vào community fund
* dùng cho hoạt động của protocol

---

# 20. Các case phổ biến

## Case 1: buyer biến mất

Nếu buyer không phản hồi trong thời gian quy định:

* protocol dùng timeout
* dựa vào state hiện tại để kết thúc giao dịch
* tài sản được xử lý theo rule đã định sẵn

---

## Case 2: seller không giao

Nếu seller không thực hiện nghĩa vụ sau khi đã nhận trạng thái funding hợp lệ:

* giao dịch có thể bị đẩy vào code 3 hoặc timeout failure
* penalty áp dụng theo rule của protocol

---

## Case 3: buyer báo không nhận được hàng

Trong thiết kế này, code 3 không cần tranh luận dài dòng.
Nó là một trạng thái fail cứng với penalty đối xứng.

---

## Case 4: người dùng spam tranh chấp

Nếu một key liên tục kích hoạt code 3:

* dispute score tăng
* weight giảm
* phí tham gia giao dịch có thể tăng
* listing của bên đó tụt rank

---

# 21. Threat Model

Các kiểu tấn công mà hệ thống cần chịu được:

* clone account để buff đơn
* spam listing
* relay spam
* wash reputation
* phá mạng bằng packet giả
* tranh chấp lặp đi lặp lại

## Biện pháp

* dùng weight thay vì count thô
* dùng stake để tăng chi phí tấn công
* dùng ký số để chặn giả mạo
* dùng DHT và relay để giảm phụ thuộc vào trung tâm

---

# 22. Bản chất của hệ thống

Cốt lõi của INeedANewGuitar là:

```text
không ai cần tin ai
chỉ cần tin luật chơi
```

Hệ thống không cố đoán ai thiện, ai ác.
Nó chỉ định nghĩa luật rất rõ:

* giao dịch thành công thì tiền đi đúng nơi
* giao dịch hủy đúng luật thì tiền quay về đúng nơi
* giao dịch rơi vào code 3 thì cả hai cùng chịu phí phạt như nhau

---

# 23. Kết luận

INeedANewGuitar là một marketplace phi tập trung với ba điểm nổi bật:

1. **phân tán quyền lực**: không có sàn trung tâm nắm toàn bộ luồng giao dịch
2. **phân tán discovery**: tìm kiếm bằng DHT + broadcast
3. **phân tán niềm tin**: dựa vào signature, escrow, stake, và rule-based settlement

Mục tiêu cuối cùng là xây dựng một hệ thống mà:

* giao dịch có thể xác minh
* gian lận trở nên đắt đỏ
* tranh chấp trở thành một lựa chọn tốn kém
* cộng đồng có lợi từ việc duy trì protocol

```text
Trong hệ thống này,
m có thể fake cảm xúc,
nhưng m không thể fake chữ ký,
không thể fake trạng thái contract,
và không thể fake hậu quả của code 3.
```
