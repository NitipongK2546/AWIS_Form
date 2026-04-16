# Guideline v0.2.1

## 1. เริ่มต้น

```bash
./setup.sh
```
สิ่งที่จะเกิดขึ้นคือ

1. Database ถูก Migrate
1. Superuser ถูกสร้างขึ้น
1. Court User ถูกสร้างขึ้น
1. Group ถูกสร้างขึ้น
1. มีการสร้าง และ Assign Permission ให้อัตโนมัติ

## 2. สร้างฟอร์ม

การสร้างฟอร์มจะมีทั้งหมด 4 Steps.

Step 0: เลือกผู้ที่เป็นเจ้าของตัวจริงของคำขอดังกล่าว

Step 1: กรอกข้อมูลแบบฟอร์มคำขอ (Reqform)

Step 2: กรอกข้อมูลหมาย (Warrant)

Step 3: ตรวจสอบความถูกต้อง

หากผู้ใช้ได้ทำ Step 1 หรือ Step 2 สำเร็จแล้ว ข้อมูลจะถูกเก็บไว้ใน Django Session ซึ่งจะหายไปก็ต่อเมื่อ Step 3 สำเร็จ

เมื่อกดยืนยันจะถือว่าสำเร็จการสร้างแบบฟอร์ม โดยจะมีการสร้าง reqno ที่เป็นการผสมกันระหว่าง req_case_type_id, reqform_number, และ req_year, ซึ่งไม่สามารถซ้ำกันได้

โดยการสร้างแบบฟอร์มที่สำเร็จ จะสร้าง Object ดังนี้:

- `FormAwaitingApproval` โดยเก็บ ReqformDataModel ไว้แบบ One-to-One
- `ReqformDataModel` เป็นแบบฟอร์มที่เก็บ WarrantDataModel แบบ Many-to-Many
- `WarrantDataModel`


## 3. รับรองฟอร์มและส่ง

การรับรองแบบฟอร์มจะทำการสร้าง Object เพิ่ม ดังนี้

- `VisualReqformData` ดูสถานะ Reqform
- `VisualWarrantData` ดูสถานะ Warrant

และจะทำการส่ง API ทันที หากการตั้งค่าเปิดเอาไว้


## 4. การให้ศาลแก้ไขสถานะ

ศาลจะสามารถส่ง API เข้ามาที่ Directory ดังกล่าว เพื่อเปลี่ยนค่าได้

```
VisualReqformData
{{ HOST }}/api/v1/update-status/reqwarrant
```

```
VisualWarrantData
{{ HOST }}/api/v1/update-status/warrant
```

ศาลจะไม่สามารถเข้าถึง API ได้ หากไม่มีการเพิ่ม JWT (JSON Web Token) ไว้ที่ Header

โดยสามารถขอ JWT ได้จาก Directory ดังกล่าว ด้วยการส่ง POST Request

```
{{ HOST }}/api/v1/authenticate/

{
    username: XXX,
    password: YYY,   
}
```
JWT ดังกล่าวควรที่ออกได้ก็ต่อเมื่อเป็น User สำหรับการใช้ API เท่านั้น todo: แก้ algorithm ด้วย

