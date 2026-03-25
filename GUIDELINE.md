# Guideline

บอกรายละเอียดคร่าว ๆ สำหรับ Version: v0.1.4

## 1. เริ่มต้น

```bash
./setup.sh
```
สิ่งที่จะเกิดขึ้นคือ

1. Database ถูก Migrate
1. Superuser ถูกสร้างขึ้น
1. ~~Group ถูกสร้างขึ้น~~
1. ~~มีการ Assign Permission ให้อัตโนมัติ~~

## 2. สร้างฟอร์ม

การสร้างฟอร์มจะสร้าง Object ดังนี้:

- `ReqformDataModel` 
- `WarrantDataModel` ที่ถูกเก็บแบบ Many-to-Many โดย ReqformDataModel
- `FormAwaitingApproval` โดยเก็บ ReqformDataModel ไว้

## 3. รับรองฟอร์มและส่ง

การรับรองแบบฟอร์มจะทำการสร้าง Object เพิ่ม ดังนี้

- `VisualReqformData`
- `VisualWarrantData`

และจะทำการส่ง API ทันที หากการตั้งค่าเปิดเอาไว้