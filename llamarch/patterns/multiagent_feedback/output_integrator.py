# output_integrator.py

class OutputIntegrator:
    @staticmethod
    def integrate_outputs(responses):
        """
        Combines outputs from different agents.
        Customize to define how to merge outputs.
        """
        # Example integration: Concatenate results; customize integration as needed
        integrated_output = " | ".join(
            r.response for r in responses)
        return integrated_output
