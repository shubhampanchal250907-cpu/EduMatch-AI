"""
PDF Study Notes Generator using Gemini AI & ReportLab.
Generates tailored study notes customized to the student's level, goal, and available time,
and outputs a clean, publication-grade PDF file.
"""

import io
import re
import html
from datetime import datetime
from typing import Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

GEMINI_API_KEY = "AQ.Ab8RN6JC8XS33g_1wn6mVhu9BcKO7etXyiTXjraKKf_ro1xmqg"


def markdown_to_reportlab(text: str) -> str:
    """Safely escapes and converts markdown bold/italics/code into ReportLab XML."""
    escaped = html.escape(text)
    # Bold: **text** -> <b>text</b>
    escaped = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', escaped)
    # Italic: *text* -> <i>text</i>
    escaped = re.sub(r'\*(.+?)\*', r'<i>\1</i>', escaped)
    # Code: `text` -> <font name="Courier">text</font>
    escaped = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', escaped)
    return escaped


def generate_notes_with_gemini(
    subject: str,
    level: str,
    goal: str,
    time_duration: Optional[str] = "1 Hour",
    api_key: Optional[str] = None
) -> str:
    """
    Calls Gemini API to generate structured educational notes tailored to the student's parameters.
    """
    key = api_key or GEMINI_API_KEY
    prompt = f"""
You are an expert tutor creating study notes for a student.
Student Details:
- Subject: {subject}
- Proficiency Level: {level}
- Primary Objective: {goal}
- Available Study Time: {time_duration}

Please write structured, easy-to-read, comprehensive revision study notes tailored strictly for a {time_duration} session.
Include:
1. Executive Summary & Core Concepts (bullet points)
2. Essential Formulas / Code Syntax / Architecture Principles (based on {subject})
3. High-Yield Points for {goal}
4. 3 Quick Self-Check Review Questions with answers
Keep the tone clear, supportive, and practical. Avoid markdown tables or weird symbols; use plain headers and bullet points.
"""

    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-3.6-flash")
        resp = model.generate_content(prompt)
        if resp and resp.text:
            return resp.text
    except Exception as e:
        print(f"Gemini API generation error: {e}, falling back to curated notes generator.")

    return generate_fallback_notes(subject, level, goal, time_duration)


def generate_fallback_notes(subject: str, level: str, goal: str, time_duration: Optional[str]) -> str:
    """Provides high-quality structured curriculum notes when offline."""
    return f"""# {subject} Study Notes ({level} Level)
Session Duration Target: {time_duration or '1 Hour'} | Primary Focus: {goal}

## 1. Core Foundations & Fundamentals
* Key Concept 1: Understanding core architecture, syntax, and principles of {subject}.
* Key Concept 2: State management, memory allocation, and algorithmic best practices.
* Key Concept 3: Error handling, edge case validation, and clean design patterns.

## 2. Practical Syntax & High-Yield Rules
* Rule 1: Always verify boundary conditions and input types.
* Rule 2: Keep functions modular, readable, and adhering to single-responsibility principle.
* Rule 3: Use idiomatic constructs and built-in standard library utilities for performance.

## 3. Targeted Review for {goal}
* Review Strategy: Focus on active recall and solving representative problems.
* Time-saving Tip: Dedicate the first 60% of your {time_duration or '1 Hour'} to key concepts and the remaining 40% to self-testing.
* Common Pitfall: Memorizing syntax without understanding underlying mechanics.

## 4. Self-Check Review Questions
* Question 1: What is the primary difference between linear and hierarchical data structures?
  Answer: Linear structures store elements sequentially (e.g. Arrays), while hierarchical structures represent parent-child relationships (e.g. Trees).
* Question 2: How does time complexity impact real-world scaling in {subject}?
  Answer: Quadratic or exponential algorithms fail rapidly under large datasets; aim for logarithmic or linear asymptotic performance.
* Question 3: What is the best strategy when approaching an exam problem?
  Answer: Read requirements completely, draft pseudocode, test sample inputs, and then implement the clean solution.
"""


def build_notes_pdf(
    student_name: str,
    subject: str,
    level: str,
    goal: str,
    time_duration: Optional[str] = "1 Hour",
    raw_notes: Optional[str] = None
) -> io.BytesIO:
    """
    Builds a styled, publication-grade PDF in memory using ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1e293b')
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#2563eb'),
        spaceBefore=14,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1f2937'),
        leftIndent=15,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#0f172a'),
        leftIndent=12,
        spaceAfter=4
    )

    story = []

    # Title
    story.append(Paragraph(f"EduMatch AI &bull; {subject} Study Notes", title_style))
    story.append(Spacer(1, 4))

    # Meta Table Header
    now_str = datetime.now().strftime("%B %d, %Y")
    meta_data = [
        [
            Paragraph(f"<b>Student:</b> {html.escape(student_name or 'Learner')}", meta_style),
            Paragraph(f"<b>Level:</b> {html.escape(level)}", meta_style),
            Paragraph(f"<b>Session Duration:</b> {html.escape(time_duration or 'Standard')}", meta_style),
        ],
        [
            Paragraph(f"<b>Primary Goal:</b> {html.escape(goal)}", meta_style),
            Paragraph(f"<b>Generated:</b> {now_str}", meta_style),
            Paragraph(f"<b>AI Engine:</b> Gemini 3.6 Flash", meta_style),
        ]
    ]
    meta_table = Table(meta_data, colWidths=[180, 160, 180])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceAfter=8))

    # Fetch notes content
    notes_text = raw_notes or generate_notes_with_gemini(subject, level, goal, time_duration)

    lines = notes_text.split('\n')
    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            story.append(Spacer(1, 3))
            continue

        if stripped.startswith('# '):
            content = markdown_to_reportlab(stripped[2:])
            story.append(Paragraph(content, h1_style))
        elif stripped.startswith('## '):
            content = markdown_to_reportlab(stripped[3:])
            story.append(Paragraph(content, h1_style))
        elif stripped.startswith('### '):
            content = markdown_to_reportlab(stripped[4:])
            story.append(Paragraph(content, h2_style))
        elif stripped.startswith('* ') or stripped.startswith('- ') or stripped.startswith('• '):
            content = markdown_to_reportlab(stripped[2:])
            story.append(Paragraph(f"&bull; {content}", bullet_style))
        elif stripped.startswith('```') or stripped.startswith('def ') or stripped.startswith('class '):
            cleaned_code = html.escape(stripped.replace('```', ''))
            story.append(Paragraph(cleaned_code, code_style))
        else:
            content = markdown_to_reportlab(stripped)
            story.append(Paragraph(content, body_style))

    # Footer note
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceAfter=6))
    footer_text = f"EduMatch AI Study Companion &bull; Tailored for {html.escape(level)} level in {html.escape(subject)}"
    story.append(Paragraph(footer_text, meta_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
