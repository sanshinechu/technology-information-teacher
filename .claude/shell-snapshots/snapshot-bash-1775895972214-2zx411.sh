# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
shopt -s expand_aliases
# Check for rg availability
if ! (unalias rg 2>/dev/null; command -v rg) >/dev/null 2>&1; then
  function rg {
  local _cc_bin="${CLAUDE_CODE_EXECPATH:-}"
  [[ -x $_cc_bin ]] || _cc_bin=$(command -v claude 2>/dev/null)
  if [[ ! -x $_cc_bin ]]; then command rg "$@"; return; fi
  if [[ -n $ZSH_VERSION ]]; then
    ARGV0=rg "$_cc_bin" "$@"
  elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    ARGV0=rg "$_cc_bin" "$@"
  elif [[ $BASHPID != $$ ]]; then
    exec -a rg "$_cc_bin" "$@"
  else
    (exec -a rg "$_cc_bin" "$@")
  fi
}
fi
export PATH='/c/Users/user/bin:/mingw64/bin:/usr/local/bin:/usr/bin:/bin:/mingw64/bin:/usr/bin:/c/Users/user/bin:/c/Python314/Scripts:/c/Python314:/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v13.2/bin/x64:/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v13.2/bin:/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v13.0/bin/x64:/c/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v13.0/bin:/c/Windows/system32:/c/Windows:/c/Windows/System32/Wbem:/c/Windows/System32/WindowsPowerShell/v1.0:/c/Windows/System32/OpenSSH:/c/Program Files (x86)/NVIDIA Corporation/PhysX/Common:/c/Program Files/dotnet:/c/Program Files/NVIDIA Corporation/NVIDIA App/NvDLISR:/c/Users/user/AppData/Local/Muse Hub/lib:/cmd:/c/Program Files/NVIDIA Corporation/Nsight Compute 2026.1.0:/c/Program Files/nodejs:/c/ProgramData/chocolatey/bin:/c/Users/user/AppData/Local/Microsoft/WindowsApps:/c/Users/user/AppData/Local/Muse Hub/lib:/c/Users/user/AppData/Local/Programs/Antigravity/bin:/c/Users/user/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1-full_build/bin:/c/Users/user/AppData/Roaming/npm:/c/Users/user/AppData/Local/Programs/Microsoft VS Code/bin:/c/Users/user/AppData/Local/Programs/Python/Python310:/c/Program Files/nodejs:/c/Python314:/mingw64/bin:/usr/bin/vendor_perl:/usr/bin/core_perl:/c/Users/user/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/e8b76c52-4699-41b1-856d-a294418b6d8e/bcc3c25c-7365-40d4-ad44-451694ce4773/bin'
