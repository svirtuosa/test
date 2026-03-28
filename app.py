import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# SAYFA AYARI
# -----------------------------
st.set_page_config(page_title="Etik Profil Testi", page_icon="🧠", layout="centered")

# -----------------------------
# SESSION STATE
# -----------------------------
if "step" not in st.session_state:
    st.session_state.step = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

# -----------------------------
# SORULAR (daha doğal dil)
# -----------------------------
questions = [
    ("İş yerinde bir arkadaşın küçük bir hata yaptı ve kimse fark etmedi. Bu durum küçük bir zarara yol açacak. Ne yaparsın?", [
        ("Durumu bildiririm; doğru olan bu.", "Deontoloji"),
        ("Zarar küçükse görmezden gelebilirim.", "Faydacılık"),
        ("Önce arkadaşımla konuşur, düzeltmesini isterim.", "Erdem"),
        ("Benim için ne avantajlıysa onu yaparım.", "Egoizm")
    ]),
    ("Beş kişiyi kurtarmak için bir kişinin zarar görmesi gerekiyor. Nasıl karar verirsin?", [
        ("Beş kişiyi kurtarmayı seçerim.", "Faydacılık"),
        ("Kimseye bilerek zarar vermem.", "Deontoloji"),
        ("Niyet ve insanlık açısından değerlendiririm.", "Erdem"),
        ("Kendim için en az riskli olanı seçerim.", "Egoizm")
    ]),
    ("Sınavda kopya çekersen yakalanmayacaksın ve notun yükselecek. Ne yaparsın?", [
        ("Sonuç önemliyse kopya çekebilirim.", "Faydacılık"),
        ("Kural ihlali olduğu için yapmam.", "Deontoloji"),
        ("Bu benim karakterime uymaz, yapmam.", "Erdem"),
        ("Avantaj sağlıyorsa yaparım.", "Egoizm")
    ]),
    ("Bir arkadaşın senden hatasını gizlemeni istiyor. Aksi halde başka biri suçlanacak.", [
        ("Gerçeği söylerim.", "Deontoloji"),
        ("Arkadaşımı korumayı seçebilirim.", "Faydacılık"),
        ("Onu dürüst olmaya teşvik ederim.", "Erdem"),
        ("Durumdan nasıl fayda sağlarım ona bakarım.", "Egoizm")
    ]),
    ("Yolda içinde para ve kimlik olan bir cüzdan buldun.", [
        ("Sahibine ulaştırırım.", "Deontoloji"),
        ("Parayı alırım.", "Egoizm"),
        ("Sahibine ulaşmaya çalışırım.", "Erdem"),
        ("Duruma göre kendime pay çıkarırım.", "Faydacılık")
    ]),
    ("Bir projede ekip arkadaşların yeterince çalışmıyor.", [
        ("Herkes için daha çok çalışırım.", "Faydacılık"),
        ("Sadece kendi sorumluluğumu yerine getiririm.", "Deontoloji"),
        ("Ekibi motive etmeye çalışırım.", "Erdem"),
        ("En az çabayla işimi hallederim.", "Egoizm")
    ]),
    ("Adil olmadığını düşündüğün bir yasa var.", [
        ("Yine de kurallara uyarım.", "Deontoloji"),
        ("Karşı çıkmayı tercih ederim.", "Erdem"),
        ("Uyarken değiştirmek için çabalarım.", "Faydacılık"),
        ("Beni etkilemiyorsa umursamam.", "Egoizm")
    ]),
    ("Birinin seni mutlu etmek için küçük bir yalan söylediğini öğrendin.", [
        ("Yalan her durumda yanlıştır.", "Deontoloji"),
        ("Sonuç iyiyse sorun etmeyebilirim.", "Faydacılık"),
        ("Niyetine önem veririm.", "Erdem"),
        ("Bana zarar vermiyorsa önemsemem.", "Egoizm")
    ]),
    ("Kimsenin bilmeyeceği bir bağış yapma fırsatın var.", [
        ("Yine de bağış yaparım.", "Erdem"),
        ("Yapmam.", "Egoizm"),
        ("Duruma göre karar veririm.", "Faydacılık"),
        ("Bana katkısı yoksa yapmam.", "Egoizm")
    ]),
    ("Genel olarak karar verirken en çok neye dikkat edersin?", [
        ("Ortaya çıkacak toplam faydaya.", "Faydacılık"),
        ("Doğru-yanlış kurallarına.", "Deontoloji"),
        ("Nasıl bir insan olmak istediğime.", "Erdem"),
        ("Kendi çıkarlarıma.", "Egoizm")
    ]),
]

# -----------------------------
# YORUM FONKSİYONU
# -----------------------------
def generate_comment(scores):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary, secondary = sorted_scores[0], sorted_scores[1]

    yorum = f"Kararlarında ağırlıklı olarak {primary[0]} yaklaşımı öne çıkıyor. "
    yorum += f"Bunun yanında {secondary[0]} eğilimin de dikkat çekiyor. "

    if scores["Deontoloji"] > 0 and scores["Faydacılık"] > 0:
        yorum += "Bazı durumlarda kural ile sonuç arasında ikilem yaşayabilirsin. "

    if scores["Erdem"] >= 4:
        yorum += "Karakter ve değerler senin için güçlü bir referans noktası. "

    if scores["Egoizm"] >= 4:
        yorum += "Kritik anlarda kişisel çıkarın belirleyici olabilir. "

    return yorum

# -----------------------------
# BAŞLANGIÇ EKRANI
# -----------------------------
if st.session_state.step == 0:
    st.title("🧠 Etik Karar Verme Testi")
    st.markdown("Bu test, karar verirken hangi etik yaklaşımı benimsediğini analiz eder.")
    
    if st.button("Teste Başla"):
        st.session_state.step = 1
        st.rerun()

# -----------------------------
# SORU EKRANI (TEK TEK)
# -----------------------------
elif st.session_state.step <= len(questions):
    q_index = st.session_state.step - 1
    q, options = questions[q_index]

    st.progress((q_index + 1) / len(questions))
    st.subheader(f"Soru {q_index + 1}")
    st.write(q)

    # boş başlangıç (None)
    choice = st.radio(
        "Seçimin:",
        options=[opt[0] for opt in options],
        index=None
    )

    if st.button("Devam Et"):
        if choice is None:
            st.warning("Lütfen bir seçenek işaretle.")
        else:
            st.session_state.answers.append((choice, options))
            st.session_state.step += 1
            st.rerun()

# -----------------------------
# SONUÇ EKRANI
# -----------------------------
else:
    st.title("📊 Sonuçların")

    scores = {
        "Faydacılık": 0,
        "Deontoloji": 0,
        "Erdem": 0,
        "Egoizm": 0
    }

    for choice, options in st.session_state.answers:
        for text, category in options:
            if text == choice:
                scores[category] += 1

    dominant = max(scores, key=scores.get)

    # Kart görünümü
    st.markdown("### Etik Dağılımın")
    col1, col2 = st.columns(2)

    items = list(scores.items())

    for i, (k, v) in enumerate(items):
        with (col1 if i % 2 == 0 else col2):
            st.metric(label=k, value=v)

    st.markdown("---")

    st.markdown(f"### 🧠 Baskın Yaklaşım: {dominant}")

    # Görsel alanı (placeholder)
    st.image("https://via.placeholder.com/600x200.png?text=Etik+Yaklaşım", use_container_width=True)

    st.markdown("### 🧾 Analiz")
    st.success(generate_comment(scores))

    # -----------------------------
    # RADAR CHART (küçük ve dengeli)
    # -----------------------------
    labels = list(scores.keys())
    values = list(scores.values())
    values += values[:1]

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4,4))  # küçük grafik
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    st.pyplot(fig)

    # yeniden başlat
    if st.button("Tekrar Çöz"):
        st.session_state.step = 0
        st.session_state.answers = []
        st.rerun()
