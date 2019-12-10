#!/usr/bin/env python3
from BasicWorld import kernel
import matplotlib.pyplot as plt


kernel[3][3] = 0

plt.imshow(kernel, cmap="gray")
plt.colorbar()
plt.show()
