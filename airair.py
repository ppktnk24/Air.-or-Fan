import streamlit as st
import numpy as np
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Fan vs AC Classifier", page_icon="🌬️")
st.title("Fan vs Air Conditioner Classifier 🌬️❄️")
st.write("เปิดกล้องเพื่อแยกแยะพัดลม (Fan) หรือแอร์ (Air Conditioner)")

# 2. โหลด Model (เพิ่ม compile=False เพื่อลด Error จาก Teachable Machine)
@st.cache_resource
def load_my_model():
    return load_model('model.h5', compile=False) # เปลี่ยนชื่อไฟล์ตามของคุณ

try:
    model = load_my_model()
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดโมเดล กรุณาตรวจสอบไฟล์ model.h5: {e}")
    st.stop() # หยุดทำงานถ้าไม่มีโมเดล

# ตั้งชื่อ Class ให้ตรงกับตอนที่เทรนมา
class_names = ["Air Conditioner", "Fan"] 

# 3. ส่วนของการใช้กล้อง
img_file_buffer = st.camera_input("📸 ถ่ายภาพเพื่อวิเคราะห์")

if img_file_buffer is not None:
    # อ่านรูปภาพ
    img = Image.open(img_file_buffer)
    
    # แปลงเป็น RGB เพื่อป้องกันปัญหาภาพติด Alpha channel (RGBA)
    img = img.convert('RGB')
    
    # ปรับขนาดและ Crop ภาพให้เป็น 224x224 แบบรักษาสัดส่วน (ดีกว่า resize ตรงๆ)
    img_resized = ImageOps.fit(img, (224, 224), Image.Resampling.LANCZOS)
    img_array = np.array(img_resized)
    
    # Pre-processing (Normalization ให้ค่าสีอยู่ในช่วง -1 ถึง 1 แบบที่โมเดลต้องการ)
    img_normalized = (img_array.astype(np.float32) / 127.5) - 1.0
    img_reshaped = img_normalized.reshape(1, 224, 224, 3)

    # 4. ทำนายผล
    prediction = model.predict(img_reshaped)
    index = np.argmax(prediction)
    label = class_names[index]
    confidence = prediction[0][index]

    # 5. แสดงผลลัพธ์
    st.markdown("---")
    st.subheader("💡 ผลการวิเคราะห์")
    
    if label == "Air Conditioner":
        st.info(f"🧊 **สิ่งนี้คือ: {label}**")
    else:
        st.success(f"🌀 **สิ่งนี้คือ: {label}**")
        
    st.write(f"**ความมั่นใจ (Confidence):** {confidence * 100:.2f}%")
    
    # เพิ่มแถบหลอดพลัง (Progress bar) เพื่อแสดงความน่าจะเป็นของแต่ละคลาส
    st.write("รายละเอียดความน่าจะเป็น:")
    for i, class_name in enumerate(class_names):
        prob = float(prediction[0][i])
        st.progress(prob, text=f"{class_name}: {prob * 100:.2f}%")