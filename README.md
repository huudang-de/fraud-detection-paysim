Dự án: Hệ thống phát hiện gian lận thanh toán số tối ưu hóa Giá trị kỳ vọng (EV)

Lĩnh vực: Fintech / Ngân hàng số / Quản trị rủi ro.

1. Tóm lược mục tiêu (Impact-driven Summary)

Xây dựng mô hình Machine Learning phát hiện giao dịch gian lận trên tập dữ liệu PaySim (6.3 triệu bản ghi), giúp tiết kiệm 77% chi phí rủi ro so với hệ thống dựa trên quy luật (Rule-based) truyền thống. Dự án tích hợp ma trận chi phí bất đối xứng nhằm cân bằng giữa An toàn bảo mật và Trải nghiệm khách hàng (CX).

2. Các kỹ năng & Công cụ sử dụng (Keywords cho ATS)

.Ngôn ngữ/Thư viện: Python (Pandas, NumPy), Scikit-learn, XGBoost, LightGBM, Matplotlib, Seaborn.

.Kỹ thuật dữ liệu: Xử lý dữ liệu lớn (Big Data), Tối ưu hóa bộ nhớ (giảm 53.4% dung lượng RAM), Xử lý dữ liệu mất cân bằng (RUS).

.Nghiệp vụ: Phân tích Giá trị vòng đời khách hàng (CLV), Ma trận Giá trị kỳ vọng (EV), Quyết định 2345/QĐ-NHNN.

3. Các đóng góp chính (Key Contributions)
.Tối ưu hóa dữ liệu: Chuyển đổi kiểu dữ liệu (Downcasting) giúp giảm dung lượng file từ 533MB xuống 248MB mà không làm mất đi tính chính xác của mô hình.

.Kỹ sư đặc trưng (Feature Engineering): Thiết kế các biến chuyên sâu như:
    .Account Depletion Ratio: Nhận diện hành vi vét cạn tài khoản.
    .Temporal Features: Phân tích chu kỳ sinh học và khung giờ "vàng" của tội phạm (23h - 4h).
    .Logic Validation: Phát hiện sai số logic kế toán giữa số dư đầu và cuối kỳ.

.Phát triển mô hình: Thử nghiệm nhiều thuật toán (Random Forest, XGBoost, LightGBM). Mô hình LightGBM đạt kết quả tốt nhất với AP = 0.856.

.Tư duy kinh tế trong AI: Thay đổi ngưỡng quyết định (Threshold) dựa trên CLV để giảm thiểu việc "chặn nhầm" khách hàng VIP, tối ưu hóa lợi nhuận thực tế thay vì chỉ chạy theo độ chính xác (Accuracy) đơn thuần.

4. Kết quả định lượng (Measurable Results)
.Hiệu quả tài chính: Tiết kiệm được ~1.8 tỷ VNĐ chi phí rủi ro (giảm 77% so với hệ thống cũ).
.Tối ưu vận hành: Đề xuất chiến lược "Ma sát đa tầng" (Friction Points):
    .65.88% giao dịch được phê duyệt tự động.
    .Tích hợp xác thực sinh thực học cho các giao dịch rủi ro hoặc trên 10 triệu VNĐ theo đúng Quyết định 2345/QĐ-NHNN.