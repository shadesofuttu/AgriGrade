from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from io import BytesIO
from typing import Dict, Any

class ReportGenerationService:
    """
    Generate PDF reports for batch quality assessments.
    """
    
    def generate_batch_report(self, batch_data: Dict[str, Any]) -> BytesIO:
        """
        Generate a PDF report for a batch analysis.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12
        )
        
        # Title
        title = Paragraph("ONION QUALITY ASSESSMENT REPORT", title_style)
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        # Batch Information
        batch_info = Paragraph("Batch Information", heading_style)
        story.append(batch_info)
        
        batch_table_data = [
            ['Batch ID:', batch_data.get('batch_id', 'N/A')],
            ['Date & Time:', batch_data.get('created_at', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')],
            ['Inspector:', batch_data.get('inspector_name', 'N/A')],
            ['Total Sample Size:', str(batch_data.get('total_onions', 0))],
            ['AI Model Version:', batch_data.get('model_version', 'v1.0')],
        ]
        
        batch_table = Table(batch_table_data, colWidths=[2*inch, 4*inch])
        batch_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        story.append(batch_table)
        story.append(Spacer(1, 0.4*inch))
        
        # Quality Distribution
        quality_heading = Paragraph("Quality Distribution", heading_style)
        story.append(quality_heading)
        
        quality_data = [
            ['Category', 'Count', 'Percentage'],
            ['Grade A (Healthy)', str(batch_data.get('grade_a_count', 0)), f"{batch_data.get('grade_a_percentage', 0):.2f}%"],
            ['URS (Undersized)', str(batch_data.get('urs_count', 0)), f"{batch_data.get('urs_percentage', 0):.2f}%"],
            ['Damaged', str(batch_data.get('damaged_count', 0)), f"{batch_data.get('damaged_percentage', 0):.2f}%"],
            ['Rotten', str(batch_data.get('rotten_count', 0)), f"{batch_data.get('rotten_percentage', 0):.2f}%"],
            ['Sprouted', str(batch_data.get('sprouted_count', 0)), f"{batch_data.get('sprouted_percentage', 0):.2f}%"],
        ]
        
        quality_table = Table(quality_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        quality_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ECF0F1'), colors.white])
        ]))
        
        story.append(quality_table)
        story.append(Spacer(1, 0.4*inch))
        
        # AI Analysis Summary
        summary_heading = Paragraph("AI Analysis Summary", heading_style)
        story.append(summary_heading)
        
        confidence = batch_data.get('ai_confidence', 0)
        confidence_text = f"AI Confidence Score: <b>{confidence:.2f}%</b>"
        confidence_para = Paragraph(confidence_text, styles['Normal'])
        story.append(confidence_para)
        story.append(Spacer(1, 0.2*inch))
        
        # Quality Assessment
        grade_a_pct = batch_data.get('grade_a_percentage', 0)
        if grade_a_pct >= 70:
            assessment = "Excellent quality batch. Suitable for premium markets."
            color = colors.green
        elif grade_a_pct >= 50:
            assessment = "Good quality batch. Suitable for standard markets."
            color = colors.orange
        else:
            assessment = "Below standard quality. Further sorting recommended."
            color = colors.red
        
        assessment_style = ParagraphStyle(
            'Assessment',
            parent=styles['Normal'],
            fontSize=11,
            textColor=color,
            spaceAfter=12
        )
        assessment_para = Paragraph(f"<b>Assessment:</b> {assessment}", assessment_style)
        story.append(assessment_para)
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer_text = "This report was generated automatically by the Onion Quality Grading System (SIH 26031)"
        footer_para = Paragraph(footer_text, ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        ))
        story.append(footer_para)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

# Singleton instance
report_service = ReportGenerationService()