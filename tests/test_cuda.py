# test_cuda.py
import sys

try:
    import torch
except ImportError:
    print("ImportError: 'torch' is not installed in this Python environment.")
    print("Install with: pip install torch  # or see https://pytorch.org for CUDA-specific wheels")
    print("Python executable:", sys.executable)
    sys.exit(1)

print("CUDA Available:", torch.cuda.is_available())

if torch.cuda.is_available():
    try:
        print("GPU:", torch.cuda.get_device_name(0))
    except Exception as e:
        print("Failed to get device name:", e)