import json
from rules_engine import MLEnhancedRulesEngine

# Initialize the ML-enhanced rules engine
engine = MLEnhancedRulesEngine()

# Start the rules engine container
engine.start_rules_engine_container()

# Process a sample query
query = "Create rules for order validation with maximum order amount of $1000"
result = engine.process_query(query)

print(f"Processing results: {json.dumps(result, indent=2)}")
