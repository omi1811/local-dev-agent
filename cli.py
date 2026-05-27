"""
Command-line interface for your AI coding agent.
Run from anywhere, against any project, without code changes.

Usage:
  python cli.py "Create a function" 
  python cli.py --repo /path/to/project "Add auth module"
  python cli.py -r ~/my-app -o ./src "Build API endpoint"
"""
import sys
import argparse
import logging
from pathlib import Path
from app.agents.coding_agent import CodingAgent

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="🤖 Local AI Coding Agent - Run anywhere, against any project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Create a login function"
  %(prog)s --repo ~/my-project "Add user registration"
  %(prog)s -r /app/backend -o ./api "Build REST endpoint"
  %(prog)s --repo . --output ./generated "Create utility functions"
        """
    )
    
    parser.add_argument(
        "request",
        nargs="?",
        help="What you want the AI to create (in quotes)"
    )
    
    parser.add_argument(
        "-r", "--repo",
        type=str,
        default=".",
        help="Path to the target repository (default: current directory)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output directory for generated files (default: same as --repo)"
    )
    
    parser.add_argument(
        "-m", "--max-iterations",
        type=int,
        default=2,
        help="Max maker-checker loops (default: 2)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate code but don't save to disk"
    )
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    # If no request provided, show help
    if not args.request:
        print("🤖 Local AI Coding Agent")
        print("Usage: python cli.py \"Your request here\" [options]")
        print("\nOptions:")
        print("  -r, --repo PATH       Target repository path (default: .)")
        print("  -o, --output PATH     Output directory (default: repo path)")
        print("  -m, --max-iterations N  Max refinement loops (default: 2)")
        print("  --dry-run             Generate but don't save files")
        print("\nExamples:")
        print('  python cli.py "Create a login function"')
        print('  python cli.py -r ~/my-app "Add user registration"')
        print('  python cli.py --repo /app/backend --output ./api "Build endpoint"')
        sys.exit(0)
    
    # Resolve paths
    repo_path = Path(args.repo).resolve()
    output_dir = Path(args.output).resolve() if args.output else repo_path
    
    print(f"\n🤖 AI Coding Agent")
    print(f"📁 Target repo: {repo_path}")
    print(f"📤 Output dir: {output_dir}")
    print(f"📝 Request: {args.request}")
    print("-" * 60)
    
    # Verify repo exists
    if not repo_path.exists():
        print(f"❌ Error: Repository path not found: {repo_path}")
        sys.exit(1)
    
    # Initialize agent with target repo
    agent = CodingAgent(repo_path=str(repo_path))
    
    # Suggest a filename based on request
    suggested_name = args.request.lower().split()[0].replace("-", "_")
    suggested_file = output_dir / f"{suggested_name}.py"
    
    # Get target file from user (or use suggestion)
    if not args.dry_run:
        target_input = input(f"\nSave to [{suggested_file}]: ").strip()
        target_file = Path(target_input) if target_input else suggested_file
        
        # Make path absolute if relative
        if not target_file.is_absolute():
            target_file = output_dir / target_file
    else:
        target_file = suggested_file
        print(f"\n🔍 Dry run: Would save to {target_file}")
    
    print(f"\n⏳ Generating code (this may take 1-2 minutes)...")
    
    # Run the agent
    if args.dry_run:
        # Just generate, don't save
        result = agent.implement(args.request, max_iterations=args.max_iterations)
        result["file_written"] = False
    else:
        # Generate AND save
        result = agent.implement_and_save(
            request=args.request,
            target_file=str(target_file),
            max_iterations=args.max_iterations
        )
    
    # Show results
    print("\n" + "="*60)
    print(f"Status: {result['status']}")
    print(f"Iterations: {result['iterations']}")
    
    if result.get('file_written'):
        print(f"✅ Code saved to: {target_file}")
        print(f"\n📄 Preview:")
        print("-"*60)
        print(Path(target_file).read_text())
        print("-"*60)
    elif args.dry_run:
        print("🔍 Dry run: Code generated but not saved")
        print("\nGenerated code:")
        print("-"*60)
        print(result.get('code', 'No code generated'))
        print("-"*60)
    else:
        print("❌ Code not saved")
        print("\nGenerated code:")
        print(result.get('code', 'No code generated'))

if __name__ == "__main__":
    main()