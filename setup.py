from setuptools import setup, find_packages

setup(
    name="foosball_vision",  
    version="1.0.0",  
    description="This is a final project aiming to develop an automated foosball table using computer vision and motor control.", 
    author="Sy Viet Dao",
    author_email="syviet@outlook.com", 
    url="https://github.com/Azuki04/FoosballVision",  
    packages=find_packages(where='src'), 
    package_dir={"": "src"},  
    install_requires=[
        "numpy>=1.21.0",  
        "opencv-python>=4.5.3", 
    ],
    classifiers=[
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent", 
    ],
    python_requires='>=3.6',  
)
