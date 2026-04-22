"""
creational_patterns/abstract_factory.py
Pattern: Abstract Factory
Use Case: Report export families — PDF and CSV exports require different
          formatter and renderer objects that must be consistent with each
          other. The Abstract Factory ensures a PDF report always uses a
          PDF formatter with a PDF renderer, and never mixes formats.

Justification: FR-08 requires reports exportable as both PDF and CSV.
Each format needs a consistent family of objects (formatter + renderer).
Abstract Factory guarantees this consistency without the client knowing
which concrete classes are being used.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from abc import ABC, abstractmethod
from src.models import Report


# ── Abstract Products ──────────────────────────────────────────────────────────

class ReportFormatter(ABC):
    """Abstract product: formats report data into a string."""

    @abstractmethod
    def format_header(self, report: Report) -> str:
        pass

    @abstractmethod
    def format_row(self, row: dict) -> str:
        pass

    @abstractmethod
    def format_footer(self, report: Report) -> str:
        pass


class ReportRenderer(ABC):
    """Abstract product: renders formatted content to output."""

    @abstractmethod
    def render(self, content: str) -> str:
        pass

    @abstractmethod
    def get_file_extension(self) -> str:
        pass


# ── Abstract Factory ───────────────────────────────────────────────────────────

class ReportExportFactory(ABC):
    """Abstract factory declaring creation methods for a report export family."""

    @abstractmethod
    def create_formatter(self) -> ReportFormatter:
        pass

    @abstractmethod
    def create_renderer(self) -> ReportRenderer:
        pass

    def export(self, report: Report, rows: list) -> str:
        """
        Template method using both products from the same family.
        Client calls this without knowing which concrete family is used.
        """
        formatter = self.create_formatter()
        renderer = self.create_renderer()

        content = formatter.format_header(report)
        for row in rows:
            content += formatter.format_row(row)
        content += formatter.format_footer(report)

        return renderer.render(content)


# ── CSV Family ─────────────────────────────────────────────────────────────────

class CSVFormatter(ReportFormatter):
    def format_header(self, report: Report) -> str:
        return f"Report: {report.report_type}\n"

    def format_row(self, row: dict) -> str:
        return ",".join(str(v) for v in row.values()) + "\n"

    def format_footer(self, report: Report) -> str:
        return f"Generated: {report._generated_date}\n"


class CSVRenderer(ReportRenderer):
    def render(self, content: str) -> str:
        return content  # CSV is plain text

    def get_file_extension(self) -> str:
        return ".csv"


class CSVReportFactory(ReportExportFactory):
    """Concrete factory producing CSV formatter + CSV renderer."""

    def create_formatter(self) -> ReportFormatter:
        return CSVFormatter()

    def create_renderer(self) -> ReportRenderer:
        return CSVRenderer()


# ── PDF Family ─────────────────────────────────────────────────────────────────

class PDFFormatter(ReportFormatter):
    def format_header(self, report: Report) -> str:
        return f"<PDF_HEADER>Report: {report.report_type}</PDF_HEADER>\n"

    def format_row(self, row: dict) -> str:
        cells = " | ".join(str(v) for v in row.values())
        return f"<PDF_ROW>{cells}</PDF_ROW>\n"

    def format_footer(self, report: Report) -> str:
        return f"<PDF_FOOTER>Generated: {report._generated_date}</PDF_FOOTER>\n"


class PDFRenderer(ReportRenderer):
    def render(self, content: str) -> str:
        return f"[PDF BINARY START]\n{content}[PDF BINARY END]"

    def get_file_extension(self) -> str:
        return ".pdf"


class PDFReportFactory(ReportExportFactory):
    """Concrete factory producing PDF formatter + PDF renderer."""

    def create_formatter(self) -> ReportFormatter:
        return PDFFormatter()

    def create_renderer(self) -> ReportRenderer:
        return PDFRenderer()


# ── Factory Selector ───────────────────────────────────────────────────────────

def get_export_factory(format_type: str) -> ReportExportFactory:
    formats = {
        "CSV": CSVReportFactory,
        "PDF": PDFReportFactory,
    }
    factory_class = formats.get(format_type.upper())
    if not factory_class:
        raise ValueError(f"Unsupported export format: '{format_type}'")
    return factory_class()


# ── Demo ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    report = Report("rpt_001", "Top 20 Borrowed Resources")
    report.generate({"rows": [
        {"title": "Clean Code", "borrows": 45},
        {"title": "Design Patterns", "borrows": 38},
    ]})

    rows = [
        {"title": "Clean Code", "borrows": 45},
        {"title": "Design Patterns", "borrows": 38},
    ]

    for fmt in ["CSV", "PDF"]:
        factory = get_export_factory(fmt)
        output = factory.export(report, rows)
        print(f"=== {fmt} Export ===")
        print(output)
