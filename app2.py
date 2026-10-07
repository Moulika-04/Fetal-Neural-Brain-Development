from flask import Flask, render_template_string, request, send_file
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import sqlite3
import os

# =====================================================
# FLASK APP
# =====================================================

app = Flask(__name__)

# =====================================================
# LOAD CNN MODEL
# =====================================================

model = tf.keras.models.load_model(
    "fetal_brain_health_model.h5"
)

# =====================================================
# IMAGE UPLOAD FOLDER
# =====================================================

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# =====================================================
# DATABASE
# =====================================================

def init_db():

    conn = sqlite3.connect("database.db")

    c = conn.cursor()

    c.execute("""

    CREATE TABLE IF NOT EXISTS patients(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        age TEXT,

        months TEXT,

        contact TEXT

    )

    """)

    c.execute("""

    CREATE TABLE IF NOT EXISTS reports(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        patient TEXT,

        image TEXT,

        result TEXT,

        advice TEXT

    )

    """)

    conn.commit()

    conn.close()

init_db()

# =====================================================
# DIRECT BRAIN IMAGE PATH
# =====================================================
@app.route('/brain-image')
def brain_image():

    image_path = r"C:\Users\mouli\Downloads\brain image.jfif"

    return send_file(
        image_path,
        mimetype='image/jpeg'
    )
# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():

    return render_template_string("""

<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>NeuroFetal AI</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
rel="stylesheet">

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    font-family:'Poppins',sans-serif;
    background:#f5f7fb;
}

/* NAVBAR */

.navbar{

    width:100%;
    height:85px;

    background:white;

    display:flex;

    justify-content:space-between;

    align-items:center;

    padding:0 70px;

    box-shadow:0 2px 15px rgba(0,0,0,0.05);
}

.logo h1{

    font-size:35px;

    color:#111827;
}

.logo p{

    font-size:12px;

    color:#6b7280;

    letter-spacing:2px;
}

.nav-links{

    display:flex;

    gap:20px;
}

.nav-links a{

    text-decoration:none;

    color:#111827;

    font-weight:500;
}

.portal-btn{

    background:#6d5dfc;

    color:white !important;

    padding:12px 24px;

    border-radius:12px;
}

/* HERO */

.hero{

    min-height:88vh;

    display:flex;

    justify-content:space-between;

    align-items:center;

    padding:40px 90px;
}

/* LEFT */

.left{
    width:48%;
}

.badge{

    display:inline-block;

    padding:10px 22px;

    background:white;

    border-radius:50px;

    box-shadow:0 2px 10px rgba(0,0,0,0.08);

    margin-bottom:25px;

    color:#64748b;
}

.left h1{

    font-size:70px;

    line-height:1.1;

    margin-bottom:25px;

    color:#0f172a;

    font-family:Georgia;
}

.left p{

    font-size:20px;

    line-height:1.8;

    color:#475569;

    margin-bottom:35px;
}

.buttons{

    display:flex;

    gap:20px;
}

.btn1{

    background:#6d5dfc;

    color:white;

    border:none;

    padding:18px 35px;

    border-radius:14px;

    cursor:pointer;

    font-size:16px;
}

.btn2{

    background:white;

    color:#111827;

    border:none;

    padding:18px 35px;

    border-radius:14px;

    cursor:pointer;

    box-shadow:0 2px 10px rgba(0,0,0,0.08);

    font-size:16px;
}

/* RIGHT */

.right{
    width:42%;
}

.scan-card{

    background:white;

    border-radius:30px;

    padding:25px;

    box-shadow:0 20px 50px rgba(0,0,0,0.08);
}

.scan-top{

    display:flex;

    justify-content:space-between;

    margin-bottom:20px;
}

.status{

    background:#d1fae5;

    color:#059669;

    padding:10px 18px;

    border-radius:50px;

    font-weight:bold;
}

.brain-box{

    height:500px;

    border-radius:25px;

    overflow:hidden;
}

.brain-box img{

    width:100%;

    height:100%;

    object-fit:cover;
}

button{
    transition:0.3s;
}

button:hover{
    transform:scale(1.03);
}

/* MOBILE */

@media(max-width:900px){

.hero{
    flex-direction:column;
}

.left{
    width:100%;
    text-align:center;
}

.right{
    width:100%;
    margin-top:40px;
}

.left h1{
    font-size:50px;
}

}

</style>

</head>

<body>

<!-- NAVBAR -->

<div class="navbar">

<div class="logo">

<h1>NeuroFetal</h1>

<p>AI BRAIN INSIGHT</p>

</div>

<div class="nav-links">

<a href="/patient">
Patient
</a>

<a href="/doctor"
class="portal-btn">

Doctor Portal

</a>

</div>

</div>

<!-- HERO -->

<section class="hero">

<div class="left">

<div class="badge">

🧠 AI Powered Fetal Brain Monitoring

</div>

<h1>

Understand the<br>
brain before birth.

</h1>

<p>

Advanced AI platform for fetal
brain ultrasound analysis.

Predict abnormalities,
assist doctors,
and improve prenatal care.

</p>

<div class="buttons">

<a href="/patient">

<button class="btn1">

Register Patient →

</button>

</a>

<a href="/doctor">

<button class="btn2">

Doctor Dashboard

</button>

</a>

</div>

</div>

<div class="right">

<div class="scan-card">

<div class="scan-top">

<h3>SCAN #FB-2025</h3>

<div class="status">

Normal • 94%

</div>

</div>

<div class="brain-box">

<img src="/brain-image">

</div>

</div>

</div>

</section>

</body>
</html>

""")

# =====================================================
# PATIENT PAGE
# =====================================================

@app.route("/patient", methods=["GET","POST"])
def patient():

    if request.method == "POST":

        name = request.form["name"]

        age = request.form["age"]

        months = request.form["months"]

        contact = request.form["contact"]

        conn = sqlite3.connect("database.db")

        c = conn.cursor()

        c.execute("""

        INSERT INTO patients(
            name,
            age,
            months,
            contact
        )

        VALUES(?,?,?,?)

        """, (

            name,
            age,
            months,
            contact

        ))

        conn.commit()

        conn.close()

        return """

        <html>

        <body style="font-family:Poppins;
        background:#f5f7fb;
        display:flex;
        justify-content:center;
        align-items:center;
        height:100vh;">

        <div style="
        background:white;
        padding:50px;
        border-radius:25px;
        text-align:center;
        box-shadow:0 20px 50px rgba(0,0,0,0.08);">

        <h1 style="color:green;">

        ✅ Successfully Registered

        </h1>

        <br>

        <a href="/">

        <button style="
        padding:15px 25px;
        border:none;
        background:#6d5dfc;
        color:white;
        border-radius:10px;">

        Go Home

        </button>

        </a>

        </div>

        </body>

        </html>

        """

    return """

    <html>

    <head>

    <style>

    body{
        font-family:Poppins;
        background:#f5f7fb;
    }

    .box{

        width:500px;

        margin:auto;

        margin-top:70px;

        background:white;

        padding:40px;

        border-radius:25px;

        box-shadow:0 20px 50px rgba(0,0,0,0.08);
    }

    input{

        width:100%;

        padding:16px;

        margin-bottom:20px;

        border:none;

        background:#f1f5f9;

        border-radius:12px;
    }

    button{

        width:100%;

        padding:16px;

        border:none;

        background:#6d5dfc;

        color:white;

        border-radius:12px;
    }

    </style>

    </head>

    <body>

    <a href="/">

    <button style="
    width:120px;
    margin:20px;">

    ← Back

    </button>

    </a>

    <div class="box">

    <h2 align="center">

    Patient Registration

    </h2>

    <br>

    <form method="POST">

    <input type="text"
    name="name"
    placeholder="Patient Name">

    <input type="text"
    name="age"
    placeholder="Age">

    <input type="text"
    name="months"
    placeholder="Months Pregnant">

    <input type="text"
    name="contact"
    placeholder="Emergency Contact">

    <button type="submit">

    Register Patient

    </button>

    </form>

    </div>

    </body>

    </html>

    """

# =====================================================
# DOCTOR PAGE
# =====================================================

@app.route("/doctor")
def doctor():

    return """

    <html>

    <body style="
    font-family:Poppins;
    background:#f5f7fb;">

    <div style="
    width:520px;
    margin:auto;
    margin-top:70px;
    background:white;
    padding:40px;
    border-radius:25px;
    box-shadow:0 20px 50px rgba(0,0,0,0.08);">

    <h2 align="center">

    Doctor AI Dashboard

    </h2>

    <br>

    <form action="/predict"
    method="POST"
    enctype="multipart/form-data">

    <input type="text"
    name="patient"
    placeholder="Patient Name"
    style="
    width:100%;
    padding:16px;
    margin-bottom:20px;
    border:none;
    background:#f1f5f9;
    border-radius:12px;">

    <input type="file"
    name="file">

    <br><br>

    <button type="submit"
    style="
    width:100%;
    padding:16px;
    border:none;
    background:#6d5dfc;
    color:white;
    border-radius:12px;">

    Analyze Brain Scan

    </button>

    </form>

    </div>

    </body>

    </html>

    """
# =====================================================
# PREDICT
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():

    patient = request.form["patient"]

    file = request.files["file"]

    # SAVE IMAGE
    filename = file.filename

    path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(path)

    # CNN PREDICTION
    img = image.load_img(
        path,
        target_size=(224,224)
    )

    img_array = image.img_to_array(img)

    img_array = img_array / 255.0

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    prediction = model.predict(
        img_array
    )[0][0]

    # RESULT
    if prediction >= 0.5:

        result = "NORMAL"

        advice = """

Healthy fetal brain detected.

Recommended Treatment:
• Continue prenatal vitamins
• Monthly ultrasound monitoring
• Healthy diet and hydration
• Regular doctor consultation

Recommended Doctor:
Dr. Priya Sharma
Senior Fetal Neurologist

"""

        color = "#10b981"

    else:

        result = "ABNORMAL"

        advice = """

Possible abnormality detected.

Recommended Treatment:
• Immediate fetal MRI scan
• Consult neurologist urgently
• Advanced fetal monitoring
• High-risk pregnancy supervision

Recommended Doctor:
Dr. Ravi Kumar
Fetal Brain Specialist

"""

        color = "#ef4444"

    # SAVE REPORT
    conn = sqlite3.connect("database.db")

    c = conn.cursor()

    c.execute("""

    INSERT INTO reports(
        patient,
        image,
        result,
        advice
    )

    VALUES(?,?,?,?)

    """, (

        patient,
        path,
        result,
        advice

    ))

    conn.commit()

    conn.close()

    return render_template_string("""

<!DOCTYPE html>
<html>

<head>

<title>AI Result</title>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap"
rel="stylesheet">

<style>

body{
    font-family:Poppins;
    background:#f5f7fb;
}

.back-btn{

    position:absolute;

    top:25px;

    left:25px;

    background:white;

    padding:12px 22px;

    border-radius:12px;

    text-decoration:none;

    color:#111827;

    box-shadow:0 2px 10px rgba(0,0,0,0.08);
}

.box{

    width:700px;

    margin:auto;

    margin-top:60px;

    background:white;

    padding:40px;

    border-radius:30px;

    box-shadow:0 20px 50px rgba(0,0,0,0.08);

    text-align:center;
}

.result{

    font-size:50px;

    font-weight:bold;

    color:{{color}};
}

img{

    width:100%;

    height:420px;

    object-fit:cover;

    border-radius:25px;

    margin:25px 0;
}

.patient{

    font-size:22px;

    margin-bottom:20px;
}

.advice{

    background:#f8fafc;

    padding:25px;

    border-radius:20px;

    text-align:left;

    line-height:2;

    white-space:pre-line;
}

button{

    margin-top:25px;

    padding:16px 30px;

    border:none;

    background:#6d5dfc;

    color:white;

    border-radius:14px;

    cursor:pointer;

    font-size:16px;
}

</style>

</head>

<body>

<a href="/doctor" class="back-btn">

← Back

</a>

<div class="box">

<div class="result">

{{result}}

</div>

<img src="/uploads/{{filename}}">

<div class="patient">

Patient Name: <b>{{patient}}</b>

</div>

<div class="advice">

{{advice}}

</div>

<a href="/doctor">

<button>

Analyze Another Scan

</button>

</a>

</div>

</body>

</html>

    """,

    result=result,
    patient=patient,
    advice=advice,
    filename=filename,
    color=color
    )



# =====================================================
# SHOW UPLOADED IMAGES
# =====================================================

@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_file(
        os.path.join(
            UPLOAD_FOLDER,
            filename
        )
    )


# =====================================================
# RUN APP
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )