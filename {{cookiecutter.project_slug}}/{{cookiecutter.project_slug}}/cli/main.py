"""Command line interface for GenAI operations."""

import asyncio
import json
import sys
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..client import GenAIClient
from ..models import ChatMessage
from .. import __version__

console = Console()


@click.group()
@click.version_option(version=__version__)
def cli():
    """{{ cookiecutter.project_name }} - Multi-provider GenAI CLI"""
    pass


@cli.command()
@click.option("--provider", "-p", required=True, 
              type=click.Choice(["openai", "bedrock", "gemini"]),
              help="LLM provider to use")
@click.option("--model", "-m", help="Specific model to use")
@click.option("--prompt", required=True, help="Text prompt to generate from")
@click.option("--max-tokens", type=int, help="Maximum tokens to generate")
@click.option("--temperature", type=float, help="Sampling temperature")
@click.option("--top-p", type=float, help="Top-p sampling parameter")
@click.option("--output", "-o", help="Output file path")
def generate(provider: str, model: Optional[str], prompt: str, 
             max_tokens: Optional[int], temperature: Optional[float],
             top_p: Optional[float], output: Optional[str]):
    """Generate text using the specified provider."""
    
    async def _generate():
        client = GenAIClient()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Generating with {provider}...", total=None)
            
            try:
                response = await client.generate(
                    prompt=prompt,
                    provider=provider,
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p
                )
                
                progress.update(task, completed=True)
                
                # Display results
                console.print(f"\n[bold green]Generated Text ({response.provider}/{response.model}):[/bold green]")
                console.print(f"{response.text}\n")
                
                if response.usage:
                    console.print("[bold blue]Usage Information:[/bold blue]")
                    for key, value in response.usage.items():
                        if value is not None:
                            console.print(f"  {key}: {value}")
                
                # Save to file if specified
                if output:
                    Path(output).write_text(response.text)
                    console.print(f"[green]Output saved to {output}[/green]")
                    
            except Exception as e:
                progress.update(task, completed=True)
                console.print(f"[red]Error: {e}[/red]")
                sys.exit(1)
    
    asyncio.run(_generate())


@cli.command()
@click.option("--provider", "-p", required=True,
              type=click.Choice(["openai", "bedrock", "gemini"]),
              help="LLM provider to use")
@click.option("--model", "-m", help="Specific model to use")
@click.option("--system", help="System prompt")
def chat(provider: str, model: Optional[str], system: Optional[str]):
    """Interactive chat with the specified provider."""
    
    async def _chat():
        client = GenAIClient()
        messages = []
        
        if system:
            messages.append(ChatMessage(role="system", content=system))
        
        console.print(f"[bold green]Starting chat with {provider}[/bold green]")
        console.print("[dim]Type 'quit' or 'exit' to end the conversation[/dim]\n")
        
        while True:
            try:
                user_input = console.input("[bold blue]You:[/bold blue] ")
                
                if user_input.lower() in ['quit', 'exit']:
                    break
                
                messages.append(ChatMessage(role="user", content=user_input))
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("Thinking...", total=None)
                    
                    response = await client.chat(
                        messages=messages,
                        provider=provider,
                        model=model
                    )
                    
                    progress.update(task, completed=True)
                
                console.print(f"[bold green]Assistant:[/bold green] {response.text}\n")
                messages.append(ChatMessage(role="assistant", content=response.text))
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
        
        console.print("[dim]Chat ended.[/dim]")
    
    asyncio.run(_chat())


@cli.command()
@click.option("--provider", "-p", required=True,
              type=click.Choice(["openai", "bedrock", "gemini"]),
              help="LLM provider to use")
@click.option("--model", "-m", help="Specific model to use")
@click.option("--input", "-i", required=True, help="Input file with prompts (one per line)")
@click.option("--output", "-o", required=True, help="Output JSON file")
@click.option("--concurrent", "-c", default=5, help="Number of concurrent requests")
@click.option("--max-tokens", type=int, help="Maximum tokens to generate")
@click.option("--temperature", type=float, help="Sampling temperature")
def batch(provider: str, model: Optional[str], input: str, output: str,
          concurrent: int, max_tokens: Optional[int], temperature: Optional[float]):
    """Process multiple prompts in batch."""
    
    async def _batch():
        try:
            # Read prompts from file
            prompts = Path(input).read_text().strip().split('\n')
            prompts = [p.strip() for p in prompts if p.strip()]
            
            if not prompts:
                console.print("[red]No prompts found in input file[/red]")
                sys.exit(1)
            
            client = GenAIClient()
            
            with Progress(console=console) as progress:
                task = progress.add_task(
                    f"Processing {len(prompts)} prompts...", 
                    total=len(prompts)
                )
                
                results = await client.batch_generate(
                    prompts=prompts,
                    provider=provider,
                    model=model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    concurrent_requests=concurrent
                )
                
                progress.update(task, completed=len(prompts))
            
            # Process results
            output_data = []
            errors = []
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    errors.append({"prompt_index": i, "error": str(result)})
                else:
                    output_data.append({
                        "prompt_index": i,
                        "prompt": prompts[i],
                        "response": result.text,
                        "provider": result.provider,
                        "model": result.model,
                        "usage": result.usage
                    })
            
            # Save results
            final_output = {
                "results": output_data,
                "errors": errors,
                "summary": {
                    "total_prompts": len(prompts),
                    "successful": len(output_data),
                    "failed": len(errors)
                }
            }
            
            Path(output).write_text(json.dumps(final_output, indent=2))
            
            console.print(f"[green]Batch processing completed![/green]")
            console.print(f"  Total prompts: {len(prompts)}")
            console.print(f"  Successful: {len(output_data)}")
            console.print(f"  Failed: {len(errors)}")
            console.print(f"  Results saved to: {output}")
            
        except Exception as e:
            console.print(f"[red]Batch processing failed: {e}[/red]")
            sys.exit(1)
    
    asyncio.run(_batch())


@cli.command()
def providers():
    """List available providers and their models."""
    
    async def _providers():
        try:
            client = GenAIClient()
            
            # Get provider info
            provider_info = client.get_provider_info()
            health_status = await client.health_check()
            
            table = Table(title="Available Providers")
            table.add_column("Provider", style="cyan")
            table.add_column("Status", style="green")
            table.add_column("Models", style="yellow")
            
            for provider, info in provider_info.items():
                status = "✅ Healthy" if health_status.get(provider, False) else "❌ Unavailable"
                models = ", ".join(info["models"][:3])  # Show first 3 models
                if len(info["models"]) > 3:
                    models += f" (+{len(info['models']) - 3} more)"
                
                table.add_row(provider, status, models)
            
            console.print(table)
            
        except Exception as e:
            console.print(f"[red]Error getting provider information: {e}[/red]")
            sys.exit(1)
    
    asyncio.run(_providers())


@cli.command()
@click.argument("provider")
def models(provider: str):
    """List available models for a specific provider."""
    
    try:
        client = GenAIClient()
        available_models = client.get_available_models(provider)
        
        console.print(f"[bold cyan]Available models for {provider}:[/bold cyan]")
        for model in available_models:
            console.print(f"  • {model}")
            
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error getting models: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()
