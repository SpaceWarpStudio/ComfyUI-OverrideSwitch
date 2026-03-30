from setuptools import setup, find_packages

setup(
    name="comfyui-override-switch",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "torch",
        "comfyui"
    ],
    author="iXtenda",
    description="A ComfyUI custom node for switching between inputs with override behavior",
    python_requires=">=3.7",
) 