# Forms v0.2.3.1-fix-01

## 1. สร้างฟอร์ม

### 1 สร้างแบบฟอร์มจากแบบร่างคำร้อง (Draft)

การสร้างฟอร์มจะต้องสร้าง `FormDraftContainer` ซึ่งจะเก็บข้อมูลของ Reqform และ Warrant

สามารถบันทึกความคืบหน้าได้ทุกเมื่อ

เมื่อเสร็จทุกอย่างแล้ว ต้องกดปุ่มเพื่อสร้าง `FormAwaitingApproval` จากข้อมูลทั้งหมดที่เก็บไว้ข้างใน

การสร้างแบบฟอร์มที่สำเร็จ จะสร้าง Object ดังนี้:

- `FormAwaitingApproval` โดยเก็บ ReqformDataModel ไว้แบบ One-to-One
- `ReqformDataModel` เป็นแบบฟอร์มที่เก็บ WarrantDataModel แบบ Many-to-Many
- `WarrantDataModel` 

## 2. รับรองฟอร์มและส่ง

การรับรองแบบฟอร์มจะทำการสร้าง Object เพิ่ม ดังนี้

- `VisualReqformData` ดูสถานะ Reqform
- `VisualWarrantData` ดูสถานะ Warrant

และจะทำการส่ง API ทันที หากการตั้งค่าเปิดเอาไว้

## 3. การให้ศาลแก้ไขสถานะ

[ดูได้จากเอกสาร API](/_documentation/API.md)

## 4. การส่งสถานะของ Warrant กลับไปให้ศาล

เมื่อได้ Warrant แล้ว จะสามารถส่งข้อมูลว่าได้มีการใช้หมายได้แล้วหรือไม่ให้กับศาลได้