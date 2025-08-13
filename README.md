# RSNA Intracranial Aneurysm Detection — Starter (Python + SQL Server)

Dự án mẫu giúp **người mới** bắt đầu nhanh với 3 mục tiêu:
1) **Tổ chức dữ liệu** theo lớp (Study/Series/Instance/Annotation) & nhóm tài sản
2) **Lưu trữ vào SQL Server**
3) **Làm việc nhóm** với Git

---

## 0) Yêu cầu hệ thống
- Python 3.10+ (khuyến nghị dùng Miniconda/Anaconda)
- Git, Git LFS (khuyến nghị)
- SQL Server (Express cũng được) + **ODBC Driver 17/18 for SQL Server**
- (Tuỳ chọn) Kaggle CLI để tải data

## 1) Tạo môi trường & cài thư viện
```bash
# Tạo env (Conda)
conda create -n rsna-iad python=3.10 -y
conda activate rsna-iad

# Cài libs
pip install -r requirements.txt
```

## 2) Cấu hình .env
Tạo file `.env` (hoặc sửa `.env.example` rồi đổi tên) ở thư mục gốc:
```
MSSQL_SERVER=localhost
MSSQL_DB=RSNA
MSSQL_USER=sa
MSSQL_PASSWORD=your_password
DATA_ROOT=D:/rsna_data   # đường dẫn chứa DICOM
```

## 3) Tạo DB & bảng
- Mở **SQL Server Management Studio** (SSMS) hoặc `sqlcmd`
- Chạy file `tools/create_tables.sql`
  - Sẽ tạo các bảng: `Studies`, `Series`, `Instances`, `AneurysmFindings`, `Splits`

## 4) Chuẩn bị dữ liệu DICOM
- Giải nén/đặt dữ liệu DICOM vào thư mục `DATA_ROOT` (trong `.env`)
- Cấu trúc có thể là `DATA_ROOT/<study>/<series>/*.dcm` hoặc tương tự

## 5) Ingest Series & Instances vào DB
```bash
# Quét series (mỗi .dcm đọc SeriesInstanceUID, StudyInstanceUID)
python tools/ingest_dicoms.py --scan series

# Quét instances (đọc SOPInstanceUID, InstanceNumber, spacing)
python tools/ingest_dicoms.py --scan instances
```

## 6) Ingest annotations (nếu có CSV)
- Đặt file `annotations.csv` theo mẫu cột:
  `ann_id,study_id,series_uid,x,y,z,diameter_mm,location_label`
```bash
python tools/ingest_annotations.py --csv /path/to/annotations.csv
```

## 7) Kiểm tra nhanh trong DB
```sql
SELECT TOP (10) * FROM Series;
SELECT COUNT(*) FROM Instances;
SELECT TOP (10) * FROM AneurysmFindings;
```

## 8) Làm việc nhóm với Git
```bash
# Khởi tạo repo
git init
git add .
git commit -m "init: rsna-iad starter"

# Tạo repo trống trên GitHub/GitLab, lấy URL rồi:
git remote add origin https://github.com/<your-username>/rsna-iad-starter.git
git branch -M main
git push -u origin main
```
- Quy ước nhánh: `main` (ổn định), `dev`, `feat/<tên-tính-năng>`, `fix/<sửa-lỗi>`
- Dùng Pull Request + Review trước khi merge
- (Tuỳ chọn) DVC quản lý data lớn; MLflow theo dõi thí nghiệm

## 9) Huấn luyện (gợi ý tiếp theo)
- Viết `training/datamodule.py` đọc từ DB và load volume (pydicom/nibabel)
- Chia fold theo **StudyID** để tránh rò rỉ
- Log metric (FROC/mAP) bằng MLflow/W&B

---

### Cấu trúc thư mục
```
rsna-iad-starter/
├─ core/                 # entities, organizer
├─ storage/              # mssql engine, dao
├─ tools/                # scripts: ingest, create_tables.sql
├─ configs/              # yaml cấu hình
├─ data/                 # dữ liệu gốc (không commit)
├─ outputs/              # cache, log, export
├─ notebooks/            # EDA, thử nghiệm
├─ requirements.txt
├─ .env.example
└─ README.md
```

Chúc bạn và team triển khai suôn sẻ!
