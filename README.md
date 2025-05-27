# CNRS-GPT 🧠📚

**CNRS-GPT** is a minimal prototype academic chatbot built with **Flask**, **MongoDB Atlas**, and **LlamaIndex**, designed to answer questions based on scientific research papers — specifically from **Université Lyon 1**.

> ⚠️ This project was built for **learning purposes**. The frontend is intentionally kept very simple to focus on backend and LLM integration. Please don't judge the CSS too harshly. 😅

---

## 🌟 Vision & Motivation

This prototype represents my **first draft** toward building an **excellent, robust, and intelligent chatbot** tailored for academic research at Université Lyon 1. The ultimate goal is to **empower researchers, students, and educators** with a tool that can assist in navigating complex research documents using state-of-the-art AI.

I'm especially proud to have integrated **LLMs and RAG (Retrieval-Augmented Generation)** — a cutting-edge technology that combines the reasoning power of large language models with **precision search over custom academic content**.

> 🧠 This isn't just a chatbot — it's the beginning of an AI-powered assistant designed to bring academic knowledge closer to its users, in real-time, with contextual understanding.

---

## 🏗️ Project Overview

- **Backend**: Python + Flask + LlamaIndex + HuggingFace + Groq API  
- **Frontend**: Basic HTML/CSS/JS (first version, will evolve)  
- **Database**: MongoDB Atlas (used for vector storage)  
- **LLM**: Groq's hosted `llama-3.3-70b-versatile`  
- **Use Case**: Ingest PDF research papers and enable natural-language querying against their content

---

## 🧠 What’s Inside

- ✅ **PDF Loader & Cleaner** — strips away noisy sections (e.g., references, copyrights)
- ✅ **Vector Store Indexing** — powered by HuggingFace embeddings & MongoDB Atlas
- ✅ **RAG Setup** — combines search and generation using `llama-3.3-70b` via Groq
- ✅ **Interactive Chat Interface** — simple, but functional chat UI to test LLM responses

---


