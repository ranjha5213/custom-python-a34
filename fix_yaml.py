import sys
from ruamel.yaml import YAML

def fix_workflow():
    yaml_path = '.github/workflows/main.yml'
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True
    
    try:
        with open(yaml_path, 'r') as f:
            data = yaml.load(f)
        
        with open(yaml_path, 'w') as f:
            yaml.dump(data, f)
        
        print("✅ YAML indentation fixed and comments preserved.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_workflow()
