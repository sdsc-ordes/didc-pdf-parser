import logging
import os
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, TaskID

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

def detect_analysis_type(filename: str) -> str:
    """Detect analysis type from filename."""
    filename_upper = filename.upper()
    if "IKC_" in filename_upper:
        return "IKC"
    elif "AKH_" in filename_upper:
        return "AKH"
    else:
        logger.warning(f"No analysis type detected in filename '{filename}', defaulting to IKC")
        return "IKC"

def find_pdf_files(path: Path) -> List[Path]:
    """Find all PDF files in a directory or return single file."""
    if path.is_file():
        if path.suffix.lower() == '.pdf':
            return [path]
        else:
            logger.error(f"❌ File '{path}' is not a PDF")
            raise typer.Exit(1)
    elif path.is_dir():
        pdf_files = list(path.glob("*.pdf"))
        if not pdf_files:
            logger.error(f"❌ No PDF files found in directory '{path}'")
            raise typer.Exit(1)
        return sorted(pdf_files)
    else:
        logger.error(f"❌ Path '{path}' does not exist")
        raise typer.Exit(1)

def process_single_pdf(
    pdf_path: Path,
    analysis_type: str,
    output_dir: Path,
    save_txt: bool,
    final_model_name: str,
    final_base_url: str,
    final_api_key: Optional[str]
) -> bool:
    """Process a single PDF file. Returns True if successful, False otherwise."""
    try:
        # Get base filename without extension
        base_name = pdf_path.stem
        
        # Define output paths
        txt_path = output_dir / f"{base_name}.txt"
        json_path = output_dir / f"{base_name}.json"
        
        logger.info(f"📄 Processing: [bold]{pdf_path.name}[/bold] (Analysis: {analysis_type})", extra={"markup": True})
        
        # Step 1: Parse PDF to raw text
        logger.debug("Extracting text from PDF...")
        raw_text = parse_document(str(pdf_path))
        logger.debug(f"Text extraction completed ({len(raw_text)} characters)")
        
        # Step 2: Save raw text if requested
        if save_txt:
            logger.debug(f"Saving raw text to: {txt_path.name}")
            txt_path.write_text(raw_text, encoding='utf-8')
            logger.debug("Raw text saved successfully")
        
        # Step 3: Extract structured data
        logger.debug("Extracting structured data with LLM...")
        structured = extract_structured(raw_text, final_model_name, final_base_url, analysis_type, final_api_key)
        logger.debug("Structured data extraction completed")
        
        # Step 4: Save JSON output
        logger.debug(f"Saving structured data to: {json_path.name}")
        json_path.write_text(structured.model_dump_json(indent=2), encoding='utf-8')
        logger.info(f"✅ [bold green]{pdf_path.name}[/bold green] processed successfully", extra={"markup": True})
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to process [bold red]{pdf_path.name}[/bold red]: {e}", extra={"markup": True})
        return False

@app.command()
def parse(
    input_path: Path = typer.Argument(
        ..., 
        help="Path to PDF file or directory containing PDF files",
        exists=True,
        readable=True
    ),
    analysis_type: Optional[str] = typer.Option(
        None,
        "--analysis-type", "-a",
        help="Force analysis type (IKC or AKH). If not provided, will be auto-detected from filename.",
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output-dir", "-o",
        help="Output directory for generated files. Defaults to input file/directory."
    ),
    save_txt: bool = typer.Option(
        False,
        "--save-txt", "-t",
        help="Save intermediate raw text files"
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
    Parse PDF document(s) and extract structured data.
    
    Can process a single PDF file or all PDF files in a directory.
    Analysis type (IKC/AKH) is auto-detected from filename tags or can be forced with --analysis-type.
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
    
    # Find PDF files to process
    pdf_files = find_pdf_files(input_path)
    logger.info(f"Found {len(pdf_files)} PDF file(s) to process")
    
    # Determine output directory
    if output_dir is None:
        if input_path.is_file():
            output_dir = input_path.parent
        else:
            output_dir = input_path
        logger.debug(f"Using default output directory: {output_dir}")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Using specified output directory: {output_dir}")
    
    # Process files
    successful = 0
    failed = 0
    
    if len(pdf_files) == 1:
        # Single file processing
        pdf_path = pdf_files[0]
        detected_analysis_type = analysis_type or detect_analysis_type(pdf_path.name)
        
        logger.info(f"Starting PDF parsing: [bold]{pdf_path.name}[/bold]", extra={"markup": True})
        
        if process_single_pdf(
            pdf_path, detected_analysis_type, output_dir, save_txt,
            final_model_name, final_base_url, final_api_key
        ):
            successful += 1
        else:
            failed += 1
    else:
        # Multiple files processing with progress bar
        with Progress(console=console) as progress:
            task = progress.add_task("[green]Processing PDFs...", total=len(pdf_files))
            
            for pdf_path in pdf_files:
                detected_analysis_type = analysis_type or detect_analysis_type(pdf_path.name)
                
                if process_single_pdf(
                    pdf_path, detected_analysis_type, output_dir, save_txt,
                    final_model_name, final_base_url, final_api_key
                ):
                    successful += 1
                else:
                    failed += 1
                
                progress.update(task, advance=1)
    
    # Summary
    console.print(f"\n[bold green]✨ Processing completed![/bold green]")
    console.print(f"📊 Results: {successful} successful, {failed} failed")
    console.print(f"📁 Output directory: {output_dir}")
    
    if failed > 0:
        console.print(f"[yellow]⚠️  {failed} file(s) failed to process[/yellow]")
        if not verbose:
            console.print("[dim]Use --verbose flag for detailed error information[/dim]")

if __name__ == "__main__":
    app()