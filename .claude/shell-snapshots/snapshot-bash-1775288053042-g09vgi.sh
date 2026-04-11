# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
shopt -s expand_aliases
# Check for rg availability
if ! (unalias rg 2>/dev/null; command -v rg) >/dev/null 2>&1; then
  function rg {
  if [[ -n $ZSH_VERSION ]]; then
    ARGV0=rg 'C:\Users\user\.vscode\extensions\anthropic.claude-code-2.1.90-win32-x64\resources\native-binary\claude.exe' "$@"
  elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    ARGV0=rg 'C:\Users\user\.vscode\extensions\anthropic.claude-code-2.1.90-win32-x64\resources\native-binary\claude.exe' "$@"
  elif [[ $BASHPID != $$ ]]; then
    exec -a rg 'C:\Users\user\.vscode\extensions\anthropic.claude-code-2.1.90-win32-x64\resources\native-binary\claude.exe' "$@"
  else
    (exec -a rg 'C:\Users\user\.vscode\extensions\anthropic.claude-code-2.1.90-win32-x64\resources\native-binary\claude.exe' "$@")
  fi
}
fi
export PATH='/c/Users/user/bin:/mingw64/bin:/usr/local/bin:/usr/bin:/bin:/mingw64/bin:/usr/bin:/c/Users/user/bin:/c/Users/user/AppData/Local/Programs/Microsoft VS Code:/c/Python314/Scripts:/c/Python314:/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v13.2/bin/x64:/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v13.2/bin:/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v13.0/bin/x64:/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v13.0/bin:/c/Windows/system32:/c/Windows:/c/Windows/System32/Wbem:/c/Windows/System32/WindowsPowerShell/v1.0:/c/Windows/System32/OpenSSH:/c/Program Files (x86)/NVIDIA Corporation/PhysX/Common:/c/Program Files/dotnet:/c/Program Files/NVIDIA Corporation/NVIDIA App/NvDLISR:/c/Users/user/AppData/Local/Muse Hub/lib:/cmd:/c/Program Files/NVIDIA Corporation/Nsight Compute 2026.1.0:/c/Program Files/nodejs:/c/ProgramData/chocolatey/bin:/c/Users/user/AppData/Local/Microsoft/WindowsApps:/c/Users/user/AppData/Local/Muse Hub/lib:/c/Users/user/AppData/Local/Programs/Antigravity/bin:/c/Users/user/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1-full_build/bin:/c/Users/user/AppData/Roaming/npm:/c/Users/user/AppData/Local/Programs/Microsoft VS Code/bin:/usr/bin/vendor_perl:/usr/bin/core_perl'
