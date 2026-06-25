from reportlab.platypus import *

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.enums import TA_CENTER

from reportlab.lib.colors import blue

styles = getSampleStyleSheet()

title_style = styles["Heading1"]

title_style.alignment = TA_CENTER

title_style.textColor = blue


def generate_report(summary,
                    state,
                    category,
                    tips):

    doc = SimpleDocTemplate(
        "reports/Business_Report.pdf"
    )

    story = []

    story.append(
        Paragraph(
            "AI Business Intelligence Report",
            title_style
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            f"Total Sales : ₹{summary['sales']:,.0f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Total Profit : ₹{summary['profit']:,.0f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Orders : {summary['orders']}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            f"Best Performing State : {state[0]}",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Best Category : {category[0]}",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "AI Recommendations",
            styles["Heading2"]
        )
    )

    for i in tips:

        story.append(
            Paragraph(
                "• "+i,
                styles["Normal"]
            )
        )

    doc.build(story)
