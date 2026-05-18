"""
File Analysis Tool with GitHub Copilot Integration
Analyzes any file type and provides insights based on user intent.
Functional approach without OOP.
"""

import os
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re


# ============================================================================
# FILE PARSING FUNCTIONS
# ============================================================================

def parse_text(file_path: str) -> str:
    """Parse plain text files."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.read()


def parse_json(file_path: str) -> str:
    """Parse JSON files and convert to readable format."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return json.dumps(data, indent=2)
    except json.JSONDecodeError:
        return parse_text(file_path)


def parse_csv(file_path: str) -> str:
    """Parse CSV files into structured text."""
    try:
        rows = []
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(" | ".join(row))
        return "\n".join(rows)
    except Exception:
        return parse_text(file_path)


def parse_markdown(file_path: str) -> str:
    """Parse Markdown files."""
    return parse_text(file_path)


def parse_code(file_path: str) -> str:
    """Parse code files with language context."""
    content = parse_text(file_path)
    ext = Path(file_path).suffix.lower()
    return f"[{ext.upper()} CODE]\n{content}"


def parse_file(file_path: str) -> str:
    """Universal file parser that delegates to format-specific parsers."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_ext = Path(file_path).suffix.lower()
    
    # Map extensions to parsers
    parser_map = {
        '.json': parse_json,
        '.csv': parse_csv,
        '.md': parse_markdown,
        '.txt': parse_text,
        '.py': parse_code,
        '.js': parse_code,
        '.ts': parse_code,
        '.java': parse_code,
        '.cpp': parse_code,
        '.c': parse_code,
        '.html': parse_text,
        '.xml': parse_text,
        '.yaml': parse_text,
        '.yml': parse_text,
        '.log': parse_text,
    }
    
    parser = parser_map.get(file_ext, parse_text)
    return parser(file_path)


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_summarize(content: str) -> List[str]:
    """Generate summary bullet points."""
    points = []
    
    # Extract key sentences (sentences with important words)
    sentences = re.split(r'[.!?]\s+', content)[:5]
    important_keywords = ['important', 'key', 'critical', 'essential', 'primary', 'main']
    
    for sentence in sentences:
        sentence = sentence.strip()
        if any(keyword in sentence.lower() for keyword in important_keywords):
            if sentence and len(sentence) > 10:
                points.append(sentence[:100] + "...")
    
    if not points:
        # Fallback: use first few lines
        lines = content.split('\n')[:3]
        points = [line.strip() for line in lines if line.strip()]
    
    return points if points else ["Unable to extract summary from content"]


def analyze_key_risks(content: str) -> List[str]:
    """Identify potential risks or issues."""
    risk_keywords = ['error', 'fail', 'issue', 'bug', 'risk', 'warn', 'danger', 
                    'critical', 'alert', 'problem', 'exception', 'todo', 'fixme']
    points = []
    
    lines = content.split('\n')
    for line in lines:
        if any(keyword in line.lower() for keyword in risk_keywords):
            line = line.strip()
            if line and len(line) > 5:
                points.append(f"Potential: {line[:80]}")
    
    return points if points else ["No obvious risks detected"]


def analyze_action_items(content: str) -> List[str]:
    """Extract actionable tasks."""
    action_keywords = ['todo', 'fixme', 'implement', 'add', 'fix', 'update', 
                      'create', 'remove', 'improve', 'refactor', 'optimize']
    points = []
    
    lines = content.split('\n')
    for line in lines:
        if any(keyword in line.lower() for keyword in action_keywords):
            line = line.strip()
            if line and len(line) > 5:
                points.append(f"• {line[:100]}")
    
    return points if points else ["No explicit action items found"]


def analyze_key_insights(content: str) -> List[str]:
    """Extract key insights from content."""
    return analyze_summarize(content)


def analyze_structure(content: str) -> List[str]:
    """Analyze document structure."""
    points = []
    
    # Count sections, headings, code blocks
    lines = content.split('\n')
    headings = [l for l in lines if l.startswith('#')]
    code_blocks = [l for l in lines if l.startswith('```')]
    code_lines = len([l for l in lines if l.strip().startswith('//')])
    
    points.append(f"Total lines: {len(lines)}")
    if headings:
        points.append(f"Headings/Sections: {len(headings)}")
    if code_blocks:
        points.append(f"Code blocks: {len(code_blocks) // 2}")
    if code_lines:
        points.append(f"Commented lines: {code_lines}")
    points.append(f"Average line length: {sum(len(l) for l in lines) // max(len(lines), 1)} chars")
    
    return points


def analyze_keywords(content: str) -> List[str]:
    """Extract key terms and topics."""
    # Remove common words
    common_words = {'the', 'a', 'an', 'and', 'or', 'is', 'are', 'was', 'were', 
                   'be', 'to', 'of', 'in', 'on', 'at', 'for', 'with', 'by', 'from'}
    
    words = re.findall(r'\b[a-z]{4,}\b', content.lower())
    word_freq = {}
    for word in words:
        if word not in common_words:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    return [f"{word} (freq: {count})" for word, count in sorted_words]


def analyze_questions(content: str) -> List[str]:
    """Generate important questions about content."""
    return [
        "What is the main purpose of this document?",
        "Who is the intended audience?",
        "What are the key takeaways?",
        "What action should be taken?",
        "What dependencies or context is needed?",
    ]


def analyze_improvements(content: str) -> List[str]:
    """Suggest improvements."""
    suggestions = []
    
    lines = content.split('\n')
    if len(lines) < 3:
        suggestions.append("Consider adding more detail or context")
    
    if len(content) < 50:
        suggestions.append("Content appears brief - consider elaborating")
    
    if not any(char in content for char in ['!', '?']):
        suggestions.append("Consider using more expressive punctuation")
    
    suggestions.append("Ensure clear structure with sections or headings")
    suggestions.append("Add examples or use cases where applicable")
    
    return suggestions


# Intent mappings
INTENTS = {
    'summarize': (analyze_summarize, 'Provide a concise summary of the main points'),
    'key_risks': (analyze_key_risks, 'Identify potential risks, issues, or problems'),
    'action_items': (analyze_action_items, 'Extract actionable tasks or next steps'),
    'key_insights': (analyze_key_insights, 'Highlight the most important insights'),
    'structure': (analyze_structure, 'Describe the structure and organization'),
    'keywords': (analyze_keywords, 'Extract key terms and topics'),
    'questions': (analyze_questions, 'Generate important questions about the content'),
    'improvements': (analyze_improvements, 'Suggest improvements or optimizations'),
}


def analyze(content: str, intent: str = 'summarize') -> List[str]:
    """
    Analyze content based on user intent and return bullet points.
    
    Args:
        content: The text content to analyze
        intent: The analysis intent (see INTENTS keys)
    
    Returns:
        List of bullet-point insights
    """
    if intent not in INTENTS:
        raise ValueError(f"Unknown intent. Available: {', '.join(INTENTS.keys())}")
    
    analyzer_func, _ = INTENTS[intent]
    return analyzer_func(content)


# ============================================================================
# FORMATTING & OUTPUT FUNCTIONS
# ============================================================================

def format_insights(insights: List[str]) -> List[str]:
    """Return formatted bullet-point insights."""
    return [f"• {insight}" if not insight.startswith('•') else insight 
            for insight in insights]


def save_to_markdown(file_path: str, content: str, insights: List[str], 
                     intent: str = 'summarize', 
                     output_path: Optional[str] = None) -> str:
    """
    Save analysis results to markdown file.
    
    Args:
        file_path: Original file path being analyzed
        content: The analyzed content
        insights: List of insights from analysis
        intent: Analysis intent used
        output_path: Path for output file (optional)
    
    Returns:
        Path to created file
    """
    # Generate output filename
    if output_path is None:
        base_name = Path(file_path).stem
        output_path = f"{base_name}_analysis_{intent}.md"
    
    # Create markdown content
    formatted_insights = format_insights(insights)
    md_content = f"""# File Analysis Report

**Source File:** `{file_path}`  
**Analysis Intent:** `{intent}`  
**Generated:** {Path(__file__).name}

## Insights

"""
    
    for insight in formatted_insights:
        md_content += f"{insight}\n"
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return output_path


# ============================================================================
# MAIN WORKFLOW FUNCTION
# ============================================================================

def analyze_file(file_path: str, intent: str = 'summarize', 
                save_md: bool = False, md_path: Optional[str] = None) -> Tuple[str, List[str]]:
    """
    Main function to analyze a file with specified intent.
    
    Args:
        file_path: Path to file to analyze
        intent: Analysis intent (default: 'summarize')
        save_md: Whether to save results to markdown
        md_path: Path for markdown output (optional)
    
    Returns:
        Tuple of (content, insights)
    """
    # Extract content
    content = parse_file(file_path)
    
    # Analyze
    insights = analyze(content, intent)
    
    # Save if requested
    if save_md:
        save_to_markdown(file_path, content, insights, intent, md_path)
    
    return content, insights


# ============================================================================
# DEMONSTRATION & USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("FILE ANALYSIS TOOL WITH GITHUB COPILOT")
    print("=" * 60)
    
    # Example: Analyze the current Python file
    file_path = __file__
    
    print("\n[1] Extracting content...")
    content = parse_file(file_path)
    print(f"✓ Extracted {len(content)} characters")
    
    print("\n[2] Available analysis intents:")
    for intent, (_, description) in INTENTS.items():
        print(f"   • {intent}: {description}")
    
    print("\n[3] Performing 'summarize' analysis...")
    insights = analyze(content, 'summarize')
    print("\nInsights:")
    for insight in format_insights(insights):
        print(f"  {insight}")
    
    print("\n[4] Performing 'structure' analysis...")
    insights = analyze(content, 'structure')
    print("\nStructure Analysis:")
    for insight in format_insights(insights):
        print(f"  {insight}")
    
    print("\n[5] Saving to markdown...")
    md_file = save_to_markdown(file_path, content, insights, 'summarize')
    print(f"✓ Saved to: {md_file}")
    
    print("\n" + "=" * 60)
    print("USAGE EXAMPLE:")
    print("=" * 60)
    print("""
    # Analyze any file with specific intent
    content, insights = analyze_file('path/to/file.txt', intent='key_risks')
    
    # Format and display insights
    for insight in format_insights(insights):
        print(insight)
    
    # Save analysis to markdown
    analyze_file('path/to/file.txt', intent='action_items', 
                 save_md=True, md_path='output.md')
    """)

