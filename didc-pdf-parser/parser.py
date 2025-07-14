# from docling.document_converter import DocumentConverter 
# from pathlib import Path


# def parse_document(path: Path) -> str:
#     doc = DocumentConverter().convert(path)
#     return doc.document.export_to_markdown()

import logging
from pathlib import Path
from typing import Optional, Dict, Any

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend

logger = logging.getLogger(__name__)

def parse_document(
    path: Path, 
    ocr_enabled: bool = True,
    table_structure_detection: bool = True,
    figure_extraction: bool = True,
    custom_options: Optional[Dict[str, Any]] = None
) -> str:
    """
    Parse a PDF document with enhanced quality settings.
    
    Args:
        path: Path to the PDF file
        ocr_enabled: Enable OCR for scanned documents
        table_structure_detection: Enable table structure detection
        figure_extraction: Enable figure and image extraction
        custom_options: Additional custom options for the converter
    
    Returns:
        Markdown representation of the document
    """
    try:
        logger.info(f"Initializing document converter for: {path}")
        
        # Configure PDF processing options
        pdf_options = PdfPipelineOptions(
            # Enable OCR for better text extraction from scanned PDFs
            do_ocr=ocr_enabled,
            # Enable table structure detection
            do_table_structure=table_structure_detection,
            # Enable figure extraction
            do_picture_extraction=figure_extraction,
            # Improve text extraction quality
            generate_page_images=True,
            # Better handling of complex layouts
            generate_table_images=True,
        )
        
        # Configure format-specific options
        format_options = {
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pdf_options,
                backend=PyPdfiumDocumentBackend
            )
        }
        
        # Apply custom options if provided
        if custom_options:
            format_options.update(custom_options)
        
        # Initialize converter with enhanced options
        converter = DocumentConverter(
            format_options=format_options
        )
        
        logger.info("Starting document conversion...")
        
        # Convert the document
        result = converter.convert(path)
        
        # Log conversion statistics
        if hasattr(result, 'pages'):
            logger.info(f"Successfully processed {len(result.pages)} pages")
        
        # Export to markdown with enhanced formatting
        markdown_content = result.document.export_to_markdown()
        
        logger.info(f"Document conversion completed. Generated {len(markdown_content)} characters of markdown")
        
        return markdown_content
        
    except Exception as e:
        logger.error(f"Failed to parse document {path}: {str(e)}")
        raise


def parse_document_with_metadata(
    path: Path,
    include_page_numbers: bool = True,
    preserve_formatting: bool = True,
    **kwargs
) -> Dict[str, Any]:
    """
    Parse document and return both content and metadata.
    
    Args:
        path: Path to the PDF file
        include_page_numbers: Include page number information
        preserve_formatting: Preserve original formatting as much as possible
        **kwargs: Additional arguments for parse_document
    
    Returns:
        Dictionary containing markdown content, metadata, and statistics
    """
    try:
        # Configure enhanced options
        pdf_options = PdfPipelineOptions(
            do_ocr=kwargs.get('ocr_enabled', True),
            do_table_structure=kwargs.get('table_structure_detection', True),
            do_picture_extraction=kwargs.get('figure_extraction', True),
            generate_page_images=True,
            generate_table_images=True,
        )
        
        format_options = {
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pdf_options,
                backend=PyPdfiumDocumentBackend
            )
        }
        
        converter = DocumentConverter(format_options=format_options)
        result = converter.convert(path)
        
        # Extract comprehensive information
        document_data = {
            'markdown_content': result.document.export_to_markdown(),
            'metadata': {
                'title': getattr(result.document, 'title', None),
                'author': getattr(result.document, 'author', None),
                'creation_date': getattr(result.document, 'creation_date', None),
                'modification_date': getattr(result.document, 'modification_date', None),
                'page_count': len(result.pages) if hasattr(result, 'pages') else 0,
                'file_size': path.stat().st_size if path.exists() else 0,
                'file_name': path.name,
            },
            'statistics': {
                'character_count': len(result.document.export_to_markdown()),
                'tables_detected': len([item for item in result.document.texts if 'table' in str(type(item)).lower()]) if hasattr(result.document, 'texts') else 0,
                'figures_detected': len([item for item in result.document.texts if 'figure' in str(type(item)).lower()]) if hasattr(result.document, 'texts') else 0,
            }
        }
        
        # Add page-level information if requested
        if include_page_numbers and hasattr(result, 'pages'):
            document_data['page_info'] = [
                {
                    'page_number': i + 1,
                    'content_length': len(page.text) if hasattr(page, 'text') else 0
                }
                for i, page in enumerate(result.pages)
            ]
        
        logger.info(f"Enhanced parsing completed: {document_data['statistics']}")
        
        return document_data
        
    except Exception as e:
        logger.error(f"Failed to parse document with metadata {path}: {str(e)}")
        raise


def validate_pdf_file(path: Path) -> bool:
    """
    Validate if the file is a proper PDF that can be processed.
    
    Args:
        path: Path to the PDF file
    
    Returns:
        True if file is valid, False otherwise
    """
    try:
        if not path.exists():
            logger.error(f"File does not exist: {path}")
            return False
        
        if not path.is_file():
            logger.error(f"Path is not a file: {path}")
            return False
        
        if path.suffix.lower() != '.pdf':
            logger.error(f"File is not a PDF: {path}")
            return False
        
        # Check if file is not empty
        if path.stat().st_size == 0:
            logger.error(f"PDF file is empty: {path}")
            return False
        
        # Try to read the first few bytes to check PDF header
        with open(path, 'rb') as f:
            header = f.read(5)
            if not header.startswith(b'%PDF-'):
                logger.error(f"Invalid PDF header: {path}")
                return False
        
        logger.info(f"PDF file validation passed: {path}")
        return True
        
    except Exception as e:
        logger.error(f"Error validating PDF file {path}: {str(e)}")
        return False