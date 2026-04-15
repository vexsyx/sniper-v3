import autoit
import os
autoitdll_path = os.path.join(os.path.dirname(autoit.__file__), "lib", "AutoItX3_x64.dll")
print("DLL path:", autoitdll_path)