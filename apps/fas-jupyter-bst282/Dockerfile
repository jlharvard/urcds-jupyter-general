FROM huitacademictechnology/fas-jupyter-general:sha-a9a13a9

# One-time setup for Bioconda (https://bioconda.github.io/)
RUN conda config --add channels defaults && \
	conda config --add channels bioconda && \
	conda config --add channels conda-forge && \
	conda config --set channel_priority strict

# Packages requested by BST 282 (https://canvas.harvard.edu/courses/113651)
RUN mamba install --quiet --yes rseqc scanpy
RUN pip install higlass-python
