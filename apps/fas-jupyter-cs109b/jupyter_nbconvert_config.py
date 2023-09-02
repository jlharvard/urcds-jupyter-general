# Disable sandboxing for headless chromium so that it can run in a containerized environment
# This config changes the behavior for the `jupyter nbconvert` terminal command
c.WebPDFExporter.disable_sandbox = True
