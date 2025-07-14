import logging
import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler

from parser import parse_document
from llm import extract_structured

# Set up rich console
console = Console()

# Set up logging with rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console, rich_tracebacks=True)]
)

logger = logging.getLogger("pdf_parser")

app = typer.Typer(
    name="pdf-parser",
    help="Parse PDF documents and extract structured data",
    add_completion=False
)

@app.command()
def parse(
    pdf_path: Path = typer.Argument(
        ..., 
        help="Path to the PDF file to parse",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True
    ),
    analysis_type: str = typer.Option(
        "IKC",
        "--analysis-type", "-a",
        help="IKC or AKH analysis type. Defaults to 'IKC'.",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir", "-o",
        help="Output directory for generated files. Defaults to PDF file's directory."
    ),
    save_txt: bool = typer.Option(
        False,
        "--save-txt", "-t",
        help="Save intermediate raw text file"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Enable verbose logging"
    ),
    model_name: Optional[str] = typer.Option(
        None,
        "--model-name", "-m",
        help="LLM model name to use. Falls back to MODEL_NAME environment variable."
    ),
    base_url: Optional[str] = typer.Option(
        None,
        "--base-url", "-u",
        help="Base URL for the LLM API. Falls back to BASE_URL environment variable."
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key", "-k",
        help="API key for the LLM service. Falls back to API_KEY environment variable."
    )
):
    """
    Parse a PDF document and extract structured data.
    
    The output JSON file will have the same name as the input PDF file.
    """
    # Set logging level based on verbose flag
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    # Get LLM configuration from CLI args or environment variables
    final_model_name = model_name or os.getenv("MODEL_NAME")
    final_base_url = base_url or os.getenv("BASE_URL")
    final_api_key = api_key or os.getenv("API_KEY")
    
    # Validate required parameters
    if not final_model_name:
        logger.error("❌ Model name is required. Provide --model-name or set MODEL_NAME environment variable.")
        raise typer.Exit(1)
    
    if not final_base_url:
        logger.error("❌ Base URL is required. Provide --base-url or set BASE_URL environment variable.")
        raise typer.Exit(1)
    
    logger.debug(f"Using model: {final_model_name}")
    logger.debug(f"Using base URL: {final_base_url}")
    logger.debug(f"API key {'provided' if final_api_key else 'not provided'}")
    
    # Determine output directory
    if output_dir is None:
        output_dir = pdf_path.parent
        logger.debug(f"Using PDF directory as output: {output_dir}")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Using specified output directory: {output_dir}")
    
    # Get base filename without extension
    base_name = pdf_path.stem
    
    # Define output paths
    txt_path = output_dir / f"{base_name}.txt"
    json_path = output_dir / f"{base_name}.json"
    
    logger.info(f"Starting PDF parsing: [bold]{pdf_path.name}[/bold]", extra={"markup": True})
    
    try:
        # Step 1: Parse PDF to raw text
        logger.info("📄 Extracting text from PDF...")
        raw_text = parse_document(str(pdf_path))
        logger.info(f"✅ Text extraction completed ({len(raw_text)} characters)")
        
        # Step 2: Save raw text if requested
        if save_txt:
            logger.info(f"💾 Saving raw text to: [bold]{txt_path.name}[/bold]", extra={"markup": True})
            txt_path.write_text(raw_text, encoding='utf-8')
            logger.info("✅ Raw text saved successfully")
        
        # Step 3: Extract structured data
        logger.info("🧠 Extracting structured data with LLM...")
        structured = extract_structured(raw_text, final_model_name, final_base_url, analysis_type, final_api_key)
        logger.info("✅ Structured data extraction completed")
        
        # Step 4: Save JSON output
        logger.info(f"💾 Saving structured data to: [bold]{json_path.name}[/bold]", extra={"markup": True})
        json_path.write_text(structured.model_dump_json(indent=2), encoding='utf-8')
        logger.info("✅ Structured data saved successfully")
        
        # Summary
        console.print("\n[bold green]✨ Processing completed successfully![/bold green]")
        console.print(f"📁 Output directory: {output_dir}")
        console.print(f"📄 JSON output: {json_path.name}")
        if save_txt:
            console.print(f"📝 Text output: {txt_path.name}")
            
    except FileNotFoundError as e:
        logger.error(f"❌ File not found: {e}")
        raise typer.Exit(1)
    except Exception as e:
        logger.error(f"❌ Processing failed: {e}")
        if verbose:
            logger.exception("Full error details:")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()