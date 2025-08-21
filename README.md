# ​ WhatsApp Chat Analyzer

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-app-orange)](https://streamlit.io/)
[![MIT License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

An interactive **WhatsApp Chat Analyzer** built with **Streamlit** and **Pandas**. Upload your exported WhatsApp chat file to explore your conversation trends via intuitive visual analytics.

---

##  Features
| Insight | Description |
|---|---|
| **Timeline Analysis** | View messaging trends by day, week, and month. |
| **Emoji Insights** | See your top-used emojis in a slice of pie. |
| **Most Active Users** | Discover who messages the most in group chats. |
| **WordCloud** | Quickly visualize frequently used words. |
| **Interactive Charts** | Clean visualizations powered by Matplotlib. |

---

##  Tech Stack
- **Python**: `pandas`, `regex`, `matplotlib`, `wordcloud`, `emoji`  
- **Streamlit**: For building a web-based interactive UI 

---

##  Installation & Usage

```bash
git clone https://github.com/armanphaugat/Whatsapp_chat_analyser.git
cd Whatsapp_chat_analyser
pip install -r requirements.txt
streamlit run app.py
