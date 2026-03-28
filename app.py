import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Etik Profil Testi", page_icon="🧠", layout="centered")

st.title("🧠 Etik Karar Verme Testi")
st.write("Aşağıdaki soruları cevapla, etik profilini analiz edelim.")

# Sorular ve şıklar
questions = [
    ("İş yerinde bir arkadaşın küçük bir hata yaptı...", [
        ("Hatayı bildiririm", "Deontoloji"),
        ("Bildirmem, zarar küçük", "Faydacılık"),
        ("Arkadaşımla konuşurum", "Erdem"),
        ("Kendi çıkarıma bakarım", "Egoizm")
    ]),
    ("Beş kişiyi kurtarmak için bir kişi...", [
        ("Beş kişiyi kurtarırım", "Faydacılık"),
        ("Kimseye zarar vermem", "Deontoloji"),
        ("Niyet önemli", "Erdem"),
        ("Bana en az zarar", "Egoizm")
    ]),
    ("Sınavda kopya çekme durumu...", [
        ("Çekerim, sonuç önemli", "Faydacılık"),
        ("Çekmem, kurallara aykırı", "Deontoloji"),
        ("Çekmem, karakterime zarar", "Erdem"),
        ("Çekerim, avantajım", "Egoizm")
    ]),
    ("Arkadaşının hatasını gizleme...", [
        ("Gerçeği söylerim", "Deontoloji"),
        ("Arkadaşımı korurum", "Faydacılık"),
        ("Kendisi itiraf etsin", "Erdem"),
        ("Fayda sağlarım", "Egoizm")
    ]),
    ("Cüzdan buldun...", [
        ("Sahibine ulaştırırım", "Deontoloji"),
        ("Parayı alırım", "Egoizm"),
        ("Ulaştırmaya çalışırım", "Erdem"),
        ("Pay çıkarırım", "Faydacılık")
    ]),
    ("Projede ekip çalışması...", [
        ("Ekstra çalışırım", "Faydacılık"),
        ("Kendi payım", "Deontoloji"),
        ("Ekibi motive ederim", "Erdem"),
        ("Minimum çaba", "Egoizm")
    ]),
    ("Adil olmayan yasa...", [
        ("Kurala uyarım", "Deontoloji"),
        ("Karşı çıkarım", "Erdem"),
        ("Uyar ama değiştirmeye çalışırım", "Faydacılık"),
        ("Umursamam", "Egoizm")
    ]),
    ("İyi niyetli yalan...", [
        ("Yalan yanlıştır", "Deontoloji"),
        ("Sonuç iyiyse sorun yok", "Faydacılık"),
        ("Niyet önemli", "Erdem"),
        ("Bana zarar yoksa sorun yok", "Egoizm")
    ]),
    ("Bağış yapma...", [
        ("Bağış yaparım", "Erdem"),
        ("Yapmam", "Egoizm"),
        ("Duruma göre", "Faydacılık"),
        ("Bana fayda yok", "Egoizm")
    ]),
    ("Karar verirken en önemli şey...", [
        ("Toplam fayda", "Faydacılık"),
        ("Kurallar", "Deontoloji"),
        ("Nasıl insanım", "Erdem"),
        ("Kendi çıkarım", "Egoizm")
    ]),
]

answers = []

# Soruları göster
for i, (q, options) in enumerate(questions):
    st.subheader(f"{i+1}. {q}")
    choice = st.radio(
        "Seç:",
        options=[opt[0] for opt in options],
        key=f"q{i}"
    )
    answers.append((choice, options))


# Sonuç butonu
if st.button("Sonucu Göster 🚀"):

    scores = {
        "Faydacılık": 0,
        "Deontoloji": 0,
        "Erdem": 0,
        "Egoizm": 0
    }

    # Puanlama
    for choice, options in answers:
        for text, category in options:
            if text == choice:
                scores[category] += 1

    st.write("## 📊 Skorların")
    st.write(scores)

    # Baskın akım
    dominant = max(scores, key=scores.get)
    st.write(f"### 🧠 Baskın etik yaklaşımın: **{dominant}**")

    # Açıklama
    explanations = {
        "Faydacılık": "Kararlarında sonuç ve toplam fayda ön planda.",
        "Deontoloji": "Kurallar ve doğru-yanlış ayrımı senin için belirleyici.",
        "Erdem": "Karakter ve iyi insan olma motivasyonu baskın.",
        "Egoizm": "Kararlarında kişisel çıkarın önemli rol oynuyor."
    }

    st.info(explanations[dominant])

    # Radar grafik
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
