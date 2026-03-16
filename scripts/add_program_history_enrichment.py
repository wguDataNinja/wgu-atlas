#!/usr/bin/env python3
"""
Script to add importance and site_worthy fields from program_history_enrichment.json
to the corresponding entries in program_history.json
"""

import json
import sys
from pathlib import Path

def load_json_file(filepath):
    """Load JSON data from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        sys.exit(1)

def create_enrichment_lookup(enrichment_data):
    """Create a lookup dictionary for enrichment data based on start_edition and end_edition."""
    lookup = {}
    
    for event in enrichment_data.get('events', []):
        start_edition = event.get('start_edition')
        end_edition = event.get('end_edition')
        importance = event.get('importance')
        site_worthy = event.get('site_worthy')
        
        if start_edition and end_edition:
            key = f"{start_edition}-{end_edition}"
            lookup[key] = {
                'importance': importance,
                'site_worthy': site_worthy
            }
    
    return lookup

def add_enrichment_to_history(program_history_data, enrichment_lookup):
    """Add enrichment data to program history entries."""
    updated_count = 0
    
    for program in program_history_data.get('programs', []):
        program_code = program.get('program_code')
        
        for history_entry in program.get('history', []):
            start_edition = history_entry.get('start_edition')
            end_edition = history_entry.get('end_edition')
            
            if start_edition and end_edition:
                key = f"{start_edition}-{end_edition}"
                
                if key in enrichment_lookup:
                    enrichment = enrichment_lookup[key]
                    
                    # Add importance if not already present
                    if 'importance' not in history_entry:
                        history_entry['importance'] = enrichment['importance']
                        updated_count += 1
                    
                    # Add site_worthy if not already present
                    if 'site_worthy' not in history_entry:
                        history_entry['site_worthy'] = enrichment['site_worthy']
                        updated_count += 1
    
    return updated_count

def main():
    # Define file paths
    script_dir = Path(__file__).parent
    program_history_file = script_dir.parent / 'data' / 'program_history.json'
    enrichment_file = script_dir.parent / 'data' / 'program_history_enrichment.json'
    
    print("Loading program history data...")
    program_history_data = load_json_file(program_history_file)
    
    print("Loading program history enrichment data...")
    enrichment_data = load_json_file(enrichment_file)
    
    print("Creating enrichment lookup...")
    enrichment_lookup = create_enrichment_lookup(enrichment_data)
    
    print(f"Found {len(enrichment_lookup)} enrichment entries")
    
    print("Adding enrichment data to program history...")
    updated_count = add_enrichment_to_history(program_history_data, enrichment_lookup)
    
    print(f"Updated {updated_count} fields in program history")
    
    print("Saving updated program history...")
    with open(program_history_file, 'w', encoding='utf-8') as f:
        json.dump(program_history_data, f, indent=2)
    
    print("Done! Program history has been updated with enrichment data.")

if __name__ == "__main__":
    main()