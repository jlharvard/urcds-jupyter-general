# Disable sandboxing for headless chromium so that it can run in a containerized environment
# This config changes the behavior for the jupyter notebook interface
c.WebPDFExporter.disable_sandbox = True
