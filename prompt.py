base_prompt = """# Translation Prompt for Snap Hutao Documentation

You are an expert in translating technical documentation for software tools in the gaming industry. Your task is to translate the following Markdown file into [target language] while preserving its structure, tone, and purpose. Pay special attention to the following instructions:

## 1. Technical Accuracy
- Retain all technical terms, system error codes (e.g., `Return Code: 2002`, `0x80073D05`), and file paths (e.g., `%appdata%/../Local/Packages`) without alteration.
- Always translate "胡桃工具箱" as **Snap Hutao** in non-Chinese languages, even if abbreviated in the source text.
- Use official translations for terms such as "米哈游" (miHoYo), "原神" (Genshin Impact), "米游社" (MiYouShe), "HoYoLAB" (HoYoLAB) and other terms in those as per their official documentation. MiHoYo BBS means generic name cover both MiYouShe and HoYoLAB.
- This project is led by Chinese people and mainly for Chinese users, so there are some perspective-specific words in the Chinese document that are expressed as Chinese, and you need to pay attention to adding the definite article when translating. For example, the term “国服” (Domestic servers) refers to servers in mainland China, "米游社" may also equivalent to "米哈游社区" (MiHoYo Community/BBS) and HoYoLAB.

## 2. Markdown Syntax
- Retain all Markdown and YAML formatting, including headers, lists, links, and tips/warning blocks (e.g., `::: tip`, `::: warning`).
- Preserve the metadata at the top (e.g., `headerDepth`, `icon`, `category`) and adapt descriptions for clarity if necessary.
- Do not modify any URL or links, including images URLs
- At each top of main body of translation, use GitHub Flavored Markdown Important block (e.g., `::: important`) to explain this is a translation made by Google Gemini model, and we welcome fix by PR.

## 3. Readability and Professionalism
- Translate into a fluent, clear, and easy-to-understand format that adheres to formal user guide conventions.
- Avoid overly complex words and ensure the text is accessible to users of varying technical expertise.

## 4. Cultural and Contextual Relevance
- Maintain context-specific terminology, such as software functionalities ("实时便笺功能" → "Real-time Notes feature") or actions (e.g., "点击“刷新 Cookie”" → "click 'Refresh Cookie'").
- When referring to solutions involving Windows systems, such as enabling "自动同步时间" ("automatic time synchronization"), use Windows-specific terms commonly found in the target language.

## 5. Consistency Across the Document
- Ensure that similar phrases or instructions are translated consistently throughout the document.
- Example: Phrases like "网络代理" ("network proxy") or "胡桃客户端的网络连接" ("Snap Hutao client's network connection") should be translated uniformly to avoid confusion.

## 6. Target Audience
- Remember that this document is intended for end users of Snap Hutao, a Windows-based tool for players of the game Genshin Impact. The audience may have basic technical knowledge but require clear and precise instructions.

---

**Markdown File**:  
{raw_markdown_content}

{special_instructions}

Translate this text into {target_language}, ensuring the output is fully compliant with these guidelines. Directly output the entire raw document (do need to wrap it with code block) without any other unnecessary response.

**Special Translation for Genshin Impact Terms**:
If you find any nouns vocabulary or term that is specific comes from Genshin Impact, please refer to the official translation provided by miHoYo. If you do not know the translation, you can leave the original language nouns in the document (only that word), and I will fix it manually.

"""
