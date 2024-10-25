import docker
from easyrules import RulesEngine, Rule
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import logging
from typing import List, Dict, Any
import numpy as np


class MLEnhancedRulesEngine:
    def __init__(self, llm_model_name: str = "gpt2"):
        # Initialize the rules engine
        self.rules_engine = RulesEngine()

        # Set up Docker client for rules engine
        self.docker_client = docker.from_env()

        # Initialize the LLM for rule generation
        self.tokenizer = AutoTokenizer.from_pretrained(llm_model_name)
        self.llm_model = AutoModelForCausalLM.from_pretrained(llm_model_name)

        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def start_rules_engine_container(self):
        """Start the rules engine Docker container"""
        try:
            container = self.docker_client.containers.run(
                'easy-rules',  # Docker image name
                detach=True,
                ports={'8080/tcp': 8080},
                environment={
                    'RULES_PATH': '/rules',
                    'LOG_LEVEL': 'INFO'
                }
            )
            self.logger.info(f"Rules engine container started: {container.id}")
            return container
        except docker.errors.DockerException as e:
            self.logger.error(f"Failed to start rules container: {str(e)}")
            raise

    def generate_rules_from_llm(self, context: str) -> List[Dict]:
        """Generate new rules using the LLM"""
        prompt = f"""Generate business rules based on the following context:
        Context: {context}
        Output the rules in JSON format with conditions and actions.
        """

        # Generate rules using the LLM
        inputs = self.tokenizer(
            prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.llm_model.generate(
            **inputs, max_length=200, num_return_sequences=3)
        generated_text = self.tokenizer.batch_decode(
            outputs, skip_special_tokens=True)

        # Parse generated text into rules
        rules = []
        for text in generated_text:
            try:
                rule_dict = json.loads(text)
                rules.append(rule_dict)
            except json.JSONDecodeError:
                self.logger.warning(f"Failed to parse generated rule: {text}")
                continue

        return rules

    def validate_rules(self, rules: List[Dict]) -> Dict[str, List[Dict]]:
        """Validate generated rules"""
        valid_rules = []
        invalid_rules = []

        for rule in rules:
            if self._validate_rule_structure(rule):
                valid_rules.append(rule)
            else:
                invalid_rules.append(rule)
                self.log_feedback(rule, "Invalid rule structure")

        return {
            "valid": valid_rules,
            "invalid": invalid_rules
        }

    def _validate_rule_structure(self, rule: Dict) -> bool:
        """Validate the structure of a generated rule"""
        required_fields = ['name', 'conditions', 'actions']
        return all(field in rule for field in required_fields)

    def register_rules(self, rules: List[Dict]):
        """Register valid rules with the rules engine"""
        for rule_dict in rules:
            rule = Rule(
                name=rule_dict['name'],
                description=rule_dict.get('description', ''),
                priority=rule_dict.get('priority', 0)
            )
            self.rules_engine.register_rule(rule)
            self.logger.info(f"Registered rule: {rule_dict['name']}")

    def log_feedback(self, rule: Dict, feedback: str):
        """Log feedback for rule adjustments"""
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'rule': rule,
            'feedback': feedback
        }
        self.logger.info(f"Feedback logged: {feedback_entry}")

    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query through the entire pipeline"""
        try:
            # Generate rules based on query
            generated_rules = self.generate_rules_from_llm(query)

            # Validate rules
            validated_rules = self.validate_rules(generated_rules)

            # Register valid rules
            self.register_rules(validated_rules['valid'])

            # Execute rules engine
            results = self.rules_engine.fire_rules()

            return {
                'status': 'success',
                'results': results,
                'valid_rules': len(validated_rules['valid']),
                'invalid_rules': len(validated_rules['invalid'])
            }

        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
