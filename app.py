import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Etik Profil Testi", page_icon="🧠", layout="centered")

st.title("🧠 Etik Karar Verme Testi")
st.write("Bu test, kararlarının arkasındaki etik yaklaşımı analiz eder.")

# -----------------------------
# SORULAR
# -----------------------------
questions = [
    ("İş yerinde bir arkadaşın küçük bir hata yaptı ve kimse fark etmedi.", [
        ("Hatayı bildiririm", "Deontoloji"),
        ("Bildirmem, zarar küçük", "Faydacılık"),
        ("Arkadaşımla konuşurum", "Erdem"),
        ("Kendi çıkarıma bakarım", "Egoizm")
    ]),
    ("Beş kişiyi kurtarmak için bir kişinin zarar görmesi gerekiyor.", [
        ("Beş kişiyi kurtarırım", "Faydacılık"),
        ("Kimseye zarar vermem", "Deontoloji"),
        ("Niyet önemli", "Erdem"),
        ("Bana en az zarar", "Egoizm")
    ]),
    ("Sınavda kopya çekersen yakalanmayacaksın.", [
        ("Çekerim, sonuç önemli", "Faydacılık"),
        ("Çekmem, kurallara aykırı", "Deontoloji"),
        ("Çekmem, karakterime zarar", "Erdem"),
        ("Çekerim, avantajım", "Egoizm")
    ]),
    ("Bir arkadaşın hatasını gizlemeni istiyor.", [
        ("Gerçeği söylerim", "Deontoloji"),
        ("Arkadaşımı korurum", "Faydacılık"),
        ("Kendisi itiraf etsin", "Erdem"),
        ("Fayda sağlarım", "Egoizm")
    ]),
    ("Yolda cüzdan buldun.", [
        ("Sahibine ulaştırırım", "Deontoloji"),
        ("Parayı alırım", "Egoizm"),
        ("Ulaştırmaya çalışırım", "Erdem"),
        ("Pay çıkarırım", "Faydacılık")
    ]),
    ("Projede ekip arkadaşların çalışmıyor.", [
        ("Ekstra çalışırım", "Faydacılık"),
        ("Kendi payımı yaparım", "Deontoloji"),
        ("Ekibi motive ederim", "Erdem"),
        ("Minimum çaba", "Egoizm")
    ]),
    ("Adil olmayan bir yasa var.", [
        ("Kurala uyarım", "Deontoloji"),
        ("Karşı çıkarım", "Erdem"),
        ("Uyar ama değiştirmeye çalışırım", "Faydacılık"),
        ("Umursamam", "Egoizm")
    ]),
    ("İyi niyetli bir yalan söylendi.", [
        ("Yalan her zaman yanlıştır", "Deontoloji"),
        ("Sonuç iyiyse sorun yok", "Faydacılık"),
        ("Niyet önemli", "Erdem"),
        ("Bana zarar yoksa sorun yok", "Egoizm")
    ]),
    ("Bağış yapma fırsatın var.", [
        ("Bağış yaparım", "Erdem"),
        ("Yapmam", "Egoizm"),
        ("Duruma göre", "Faydacılık"),
        ("Bana fayda yok", "Egoizm")
    ]),
    ("Karar verirken en önemli şey:", [
        ("Toplam fayda", "Faydacılık"),
        ("Kurallar", "Deontoloji"),
        ("Nasıl insanım", "Erdem"),
        ("Kendi çıkarım", "Egoizm")
    ]),
]

# -----------------------------
# YORUM FONKSİYONU
# -----------------------------
def generate_comment(scores):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary, secondary = sorted_scores[0], sorted_scores[1]

    yorum = ""

    if primary[0] == "Faydacılık":
        yorum += "Kararlarında sonuç odaklısın. Maksimum fayda üretmek senin için belirleyici. "
    elif primary[0] == "Deontoloji":
        yorum += "Kurallar ve ilkeler senin pusulan. Doğru-yanlış çizgini koruyorsun. "
    elif primary[0] == "Erdem":
        yorum += "Nasıl bir insan olduğun, kararlarının merkezinde. Karakter odaklısın. "
    elif primary[0] == "Egoizm":
        yorum += "Kararlarında kişisel çıkarın önemli. Önce kendini konumlandırıyorsun. "

    yorum += f"Aynı zamanda {secondary[0]} eğilimin de güçlü. "

    if scores["Deontoloji"] > 0 and scores["Faydacılık"] > 0:
        yorum += "Zaman zaman kural ile sonuç arasında içsel çatışma yaşayabilirsin. "

    if scores["Egoizm"] >= 4:
        yorum += "Kritik anlarda kendi çıkarına kayma ihtimalin yüksek. "

    if scores["Erdem"] >= 4:
        yorum += "Ahlaki kimliğin güçlü bir referans noktası. "

    return yorum

# -----------------------------
# UI
# -----------------------------
answers = []

for i, (q, options) in enumerate(questions):
    st.subheader(f"{i+1}. {q}")
    choice = st.radio(
        "Seç:",
        options=[opt[0] for opt in options],
        key=f"q{i}"
    )
    answers.append((choice, options))

# -----------------------------
# SONUÇ
# -----------------------------
if st.button("Sonucu Göster 🚀"):

    scores = {
        "Faydacılık": 0,
        "Deontoloji": 0,
        "Erdem": 0,
        "Egoizm": 0
    }

    for choice, options in answers:
        for text, category in options:
            if text == choice:
                scores[category] += 1

    st.write("## 📊 Skorların")
    st.write(scores)

    dominant = max(scores, key=scores.get)
    st.write(f"### 🧠 Baskın etik yaklaşımın: **{dominant}**")

    st.write("## 🧾 Etik Analizin")
    comment = generate_comment(scores)
    st.success(comment)

    # -----------------------------
    # RADAR CHART
    # -----------------------------
    labels = list(scores.keys())
    values = list(scores.values())
    values += values[:1]

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots()
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    st.pyplot(fig)
