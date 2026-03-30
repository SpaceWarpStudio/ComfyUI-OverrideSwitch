from setuptools import setup, find_packages

setup(
    name="comfyui-override-switch",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "torch",
        "comfyui"
    ],
    author="SpaceWarp Studio",
    description="A ComfyUI custom node for switching between inputs with override behavior",
    license="MIT",
    python_requires=">=3.7",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
) 