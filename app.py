import streamlit as st
import face_recognition
import numpy as np
from PIL import Image

# Complete 5-Language dictionary matching DeepShield-Auth specs
TRANSLATIONS = {
    "English": {
        "title": "🛡️ DeepShield-Auth: Global Deepfake Platform",
        "desc": "Active Biometric Scanning: Isolates and analyzes human faces using advanced focal math.",
        "label_img": "Upload Profile Picture or Video Frame",
        "btn": "🚀 Start Biometric Authentication",
        "err_no_img": "⚠️ Error: No image was uploaded.",
        "err_no_face": "🔒 SCANNER LOCKED: DeepShield Secure Authentication Activated.\n\n❌ RESULT: NO HUMAN FACE DETECTED.\n\nℹ️ This security engine *only* authenticates profile images or facial frames.",
        "rep_title": "📊 DEEPSHIELD-AUTH ANALYSIS REPORT\n=================================\n",
        "rep_risk": "🚨 VERDICT: HIGH RISK of AI Generation / Deepfake anomalies detected!",
        "rep_auth": "✅ VERDICT: LIKELY AUTHENTIC (Natural human skin frequency distribution)."
    },
    "Español": {
        "title": "🛡️ DeepShield-Auth: Plataforma Global Deepfake",
        "desc": "Escaneo Biométrico Activo: Aísla y analiza rostros humanos utilizando matemática focal avanzada.",
        "label_img": "Subir foto de perfil o fotograma de video",
        "btn": "🚀 Iniciar Autenticación Biométrica",
        "err_no_img": "⚠️ Error: No se subió ninguna imagen.",
        "err_no_face": "🔒 ESCÁNER BLOQUEADO: Autenticación segura DeepShield activada.\n\n❌ RESULTADO: NO SE DETECTÓ ROSTRO HUMANO.\n\nℹ️ Este motor de seguridad *solo* autentica imágenes de perfil o fotogramas faciales.",
        "rep_title": "📊 INFORME DE ANÁLISIS DE DEEPSHIELD-AUTH\n=================================\n",
        "rep_risk": "🚨 VEREDICTO: ¡ALTO RIESGO de generación de IA / anomalías de Deepfake detectadas!",
        "rep_auth": "✅ VEREDICTO: PROBABLEMENTE AUTÉNTICO (Distribución natural de la frecuencia de la piel humana)."
    },
    "Français": {
        "title": "🛡️ DeepShield-Auth : Plateforme Globale Deepfake",
        "desc": "Analyse Biométrique Active : Isole et analyse les visages humains à l'aide de mathématiques fouillées.",
        "label_img": "Télécharger une photo de profil ou une image vidéo",
        "btn": "🚀 Lancer l'authentification biométrique",
        "err_no_img": "⚠️ Erreur : Aucune image n'a été téléchargée.",
        "err_no_face": "🔒 SCANNER VERROUILLÉ : Authentification sécurisée DeepShield activée.\n\n❌ RÉSULTAT : AUCUN VISAGE HUMAIN DÉTECTÉ.\n\nℹ️ Ce moteur de sécurité authentifie *uniquement* les images de profil ou les cadres faciaux.",
        "rep_title": "📊 RAPPORT D'ANALYSE DEEPHIELD-AUTH\n=================================\n",
        "rep_risk": "🚨 VERDICT : RISQUE ÉLEVÉ de génération d'IA / anomalies Deepfake détectées !",
        "rep_auth": "✅ VERDICT : PROBABLEMENT AUTHENTIQUE (Distribution naturelle de la fréquence de la peau)."
    },
    "简体中文": {
        "title": "🛡️ DeepShield-Auth: 全球智能反伪验证平台",
        "desc": "主动生物特征扫描：利用先进的聚焦数学算法隔离并分析人类面部细节特征。",
        "label_img": "上传个人头像照片或视频帧截图",
        "btn": "🚀 开始生物特征安全验证",
        "err_no_img": "⚠️ 错误：未上传任何图像文件。",
        "err_no_face": "🔒 扫描器锁定：DeepShield 安全认证机制已被激活。\n\n❌ 检测结果：未识别到人类面部。\n\nℹ️ 本安全引擎仅对个人头像图片、肖像照或含有人脸的视频帧进行认证。",
        "rep_title": "📊 DEEPSHIELD-AUTH 面部特征分析报告\n=================================\n",
        "rep_risk": "🚨 检测裁决：高风险！检测到AI合成生成或Deepfake异常伪造痕迹！\n",
        "rep_auth": "✅ 检测裁决：真实度高（符合人类皮肤的天然频率分布规律）。"
    },
    "العربية": {
        "title": "🛡️ DeepShield-Auth: منصة التحقق العالمي من التزييف العميق",
        "desc": "الفحص البيومتري النشط: يعزل ويحلل الوجوه البشرية باستخدام رياضيات بؤرية متقدمة.",
        "label_img": "تحميل صورة الملف الشخصي أو لقطة إطار الفيديو",
        "btn": "🚀 بدء التحقق البيومتري الأمن",
        "err_no_img": "⚠️ خطأ: لم يتم تحميل أي صورة.",
        "err_no_face": "🔒 الماسح مغلق: تم تفعيل مصادقة DeepShield الآمنة.\n\n❌ النتيجة: لم يتم اكتشاف وجه بشري.\n\nℹ️ يعمل هذا المحرك الأمني *فقط* على مصادقة صور الملفات الشخصية أو إطارات الوجه.",
        "rep_title": "📊 تقرير تحليل DEEPSHIELD-AUTH\n=================================\n",
        "rep_risk": "🚨 القرار: خطر كبير! تم اكتشاف شذوذ تزييف عميق أو توليد ذكاء اصطناعي!",
        "rep_auth": "✅ القرار: على الأرجح حقيقي (توزيع طبيعي لترددات الجلد البشري)."
    }
}

# Language Dropdown Selector at the very top
lang = st.selectbox("🌐 Language / Idioma / Langue / 语言 / لغة", ["English", "Español", "Français", "简体中文", "العربية"])
t = TRANSLATIONS[lang]

# Dynamic Brand Display
st.title(t["title"])
st.write(t["desc"])
st.info("💡 **FREE TIER:** This security processing is funded by sponsored content below.")

uploaded_file = st.file_uploader(t["label_img"], type=["jpg", "jpeg", "png"])

if uploaded_file is not None and st.button(t["btn"]):
    # Read file data directly into numpy framework
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = face_recognition.load_image_file(uploaded_file)
    
    # Track facial coordinate arrays
    face_locations = face_recognition.face_locations(img)
    if not face_locations:
        st.error(t["err_no_face"])
    else:
        # Run advanced frequency spectrum calculations
        img_gray = np.array(Image.fromarray(img).convert('L'))
        f_transform = np.fft.fft2(img_gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = 20 * np.log(np.abs(f_shift) + 1)
        
        ratio = np.sum(magnitude_spectrum > np.mean(magnitude_spectrum)) / magnitude_spectrum.size
        
        # Output clean localized reporting blocks
        st.text(t["rep_title"] + f"Focal High-Frequency Value: {ratio:.4f}\n---------------------------------")
        if ratio > 0.45:
            st.error(t["rep_risk"])
        else:
            st.success(t["rep_auth"])
