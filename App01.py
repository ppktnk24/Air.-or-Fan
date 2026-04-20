import streamlit as st
import cv2
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

# ตั้งค่าหน้าเว็บ
st.title("Fan vs Air Conditioner Classifier")
st.write("เปิดกล้องเพื่อแยกแยะพัดลมหรือแอร์")

# โหลด Model ที่คุณเทรนมา
@st.cache_resource
def load_my_model():
    return load_model('model.h5') # เปลี่ยนชื่อไฟล์ตามที่คุณโหลดมา

model = load_my_model()
class_names = ["Air Conditioner", "Fan"] # เรียงตาม Class ใน Teachable Machine

# ส่วนของการใช้กล้อง
img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # อ่านรูปภาพ
    img = Image.open(img_file_buffer)
    img_array = np.array(img)
    
    # Pre-processing (ปรับขนาดให้ตรงกับที่ Model ต้องการ เช่น 224x224)
    img_resized = cv2.resize(img_array, (224, 224))
    img_normalized = (img_resized.astype(np.float32) / 127.5) - 1
    img_reshaped = img_normalized.reshape(1, 224, 224, 3)

    # ทำนายผล
    prediction = model.predict(img_reshaped)
    index = np.argmax(prediction)
    label = class_names[index]
    confidence = prediction[0][index]

    # แสดงผล
    st.subheader(f"ผลลัพธ์: {label}")
    st.write(f"ความแม่นยำ: {confidence*100:.2f}%")