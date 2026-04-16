# Permissions v0.2.1

## AWIS CUSTOM SETTINGS

### 1. settings.py
เก็บการตั้งค่าระบบสิทธิ์และ Role ไว้

Permission List คือประเภทของสิทธิทั้งหมดที่มี

### 2. default_perm.py
เก็บสิทธิ์พื้นฐานของแต่ละ Role ไว้

---

## Users Folder -> Permission

### 1. base.py

เก็บประเภทของสิทธิ Permission Type

- VIEW
- CREATE
- EDIT
- DELETE
- APPROVE

`!!ซึ่งจะต่างจาก LOG ที่มีเพิ่มจาก List นี้มาอีกเล็กน้อย`

### 2. perms.py

เก็บ function ที่ใช้แปลง PermissionType และ PermissionList ให้กลายเป็น String

```
perm_str(... , ...)

perm_str_list([...], ...)
```

โดยมีทั้งแบบเดี่ยวและแบบหลายอันพร้อมกัน

Django เช็คสิทธิของผู้ใช้โดยการใช้

```
user_obj.has_perms(.....)
```

ซึ่งต้องมีการใช้ String, โดย function ที่ได้กล่าวมาช่วยแก้ไขเรื่องนี้

### 3. decorator

```python
@perm_req_log([...], ..., ...)
def view_x(request : HttpRequest):
    pass
```

เป็น Decorator ที่ทำการตรวจสอบสิทธิ์ของ URL ที่เรียก View ดังกล่าว

- หาก PermissionDenied จะถูก logged ว่า Denied 

- หากเกิด Exception อื่น ๆ ก็จะถูก logged ว่า Errors

รับค่าทั้งหมด 3 ค่า

1. list[PermissionType] เพื่อกำหนดสิทธิ์ทั้งหมดที่ต้องมีในการเข้าถึง
1. PermissionList เพื่อบอกว่าต้องการสิทธิ์จากระบบอะไรเพื่อเข้าถึง
1. AccessList เพื่อเก็บว่าผู้ใช้ทำอะไรไปในการเข้าถึง URL ดังกล่าว